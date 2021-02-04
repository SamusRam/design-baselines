from design_baselines.data import StaticGraphTask
from design_baselines.logger import Logger
from design_baselines.utils import spearman
from design_baselines.utils import soft_noise
from design_baselines.online.trainers import ConservativeMaximumLikelihood
from design_baselines.online.trainers import Ensemble
from design_baselines.online.nets import ForwardModel
from collections import defaultdict
import tensorflow as tf
import numpy as np
import glob
import os


def online(config):
    """Train a forward model and perform model based optimization
    using a conservative objective function

    Args:

    config: dict
        a dictionary of hyper parameters such as the learning rate
    """

    # create the training task and logger
    logger = Logger(config['logging_dir'])
    task = StaticGraphTask(config['task'], **config['task_kwargs'])

    # save the initial dataset statistics for safe keeping
    x = task.x
    y = task.y

    if config['normalize_ys']:
        # compute normalization statistics for the score
        mu_y = np.mean(y, axis=0, keepdims=True).astype(np.float32)
        y = y - mu_y
        st_y = np.std(y, axis=0, keepdims=True).astype(np.float32)
        st_y = np.where(np.equal(st_y, 0), 1, st_y)
        y = y / st_y
    else:
        # compute normalization statistics for the score
        mu_y = np.zeros_like(y[:1])
        st_y = np.ones_like(y[:1])

    if config['normalize_xs'] and not config['is_discrete']:
        # compute normalization statistics for the data vectors
        mu_x = np.mean(x, axis=0, keepdims=True).astype(np.float32)
        x = x - mu_x
        st_x = np.std(x, axis=0, keepdims=True).astype(np.float32)
        st_x = np.where(np.equal(st_x, 0), 1, st_x)
        x = x / st_x
    else:
        # compute normalization statistics for the score
        mu_x = np.zeros_like(x[:1])
        st_x = np.ones_like(x[:1])

    input_shape = list(task.input_shape)
    if config['is_discrete']:
        input_shape[-1] = input_shape[-1] - 1

    solver_lr = config['solver_lr'] * np.sqrt(np.prod(input_shape))
    solver_interval = int(config['solver_interval'] * (
        x.shape[0] - config['val_size']) / config['batch_size'])
    solver_warmup = int(config['solver_warmup'] * (
        x.shape[0] - config['val_size']) / config['batch_size'])

    # make a neural network to predict scores
    forward_model = ForwardModel(
        input_shape,
        activations=config['activations'],
        hidden=config['hidden_size'],
        initial_max_std=config['initial_max_std'],
        initial_min_std=config['initial_min_std'])

    # create a trainer for a forward model with a conservative objective
    trainer = ConservativeMaximumLikelihood(
        forward_model, forward_model_opt=tf.keras.optimizers.Adam,
        forward_model_lr=config['forward_model_lr'],
        initial_alpha=config['initial_alpha'],
        alpha_opt=tf.keras.optimizers.Adam,
        alpha_lr=config['alpha_lr'],
        target_conservatism=config['target_conservatism'],
        negatives_fraction=config['negatives_fraction'],
        lookahead_steps=config['lookahead_steps'],
        lookahead_backprop=config['lookahead_backprop'],
        solver_beta=config['solver_beta'],
        solver_lr=solver_lr,
        solver_interval=solver_interval,
        solver_warmup=solver_warmup,
        solver_steps=config['solver_steps'],
        is_discrete=config['is_discrete'],
        constraint_type=config['constraint_type'],
        continuous_noise_std=config.get('continuous_noise_std', 0.0),
        discrete_clip=config.get('discrete_clip', 5.0))

    # create a data set
    train_data, validate_data = task.build(
        x=x, y=y,
        batch_size=config['batch_size'],
        val_size=config['val_size'])

    # select the top k initial designs from the dataset
    indices = tf.math.top_k(y[:, 0], k=config['batch_size'])[1]
    initial_x = tf.gather(x, indices, axis=0)
    if config['is_discrete']:
        p = tf.fill(tf.shape(initial_x), 1 / tf.cast(tf.shape(initial_x)[-1], tf.float32))
        initial_x = trainer.discrete_clip * initial_x + (1.0 - trainer.discrete_clip) * p
        initial_x = tf.math.log(initial_x)
        initial_x = initial_x[:, :, 1:] - initial_x[:, :, :1]

    # create the starting point for the optimizer
    evaluations = 0
    score = None
    trainer.solution = tf.Variable(initial_x)
    trainer.previous_solution = tf.Variable(initial_x)
    trainer.done = tf.Variable(tf.fill(
        [config['batch_size']] + [1 for _ in x.shape[1:]], False))

    def evaluate_solution(xt):
        nonlocal evaluations, score

        # evaluate the design using the oracle and the forward model
        with tf.GradientTape() as tape:
            tape.watch(xt)
            model = forward_model.get_distribution(xt).mean()

        # evaluate the predictions and gradient norm
        evaluations += 1
        grads = tape.gradient(model, xt)
        model = model * st_y + mu_y

        # record the prediction and score to the logger
        logger.record("distance/travelled",
                      tf.linalg.norm(xt - initial_x), evaluations)
        logger.record(f"oracle/prediction",
                      model, evaluations)
        logger.record(f"oracle/grad_norm", tf.linalg.norm(
            tf.reshape(grads, [grads.shape[0], -1]), axis=-1), evaluations)

        if evaluations in config['evaluate_steps'] \
                or len(config['evaluate_steps']) == 0 or score is None:
            solution = xt
            if config['is_discrete']:
                solution = tf.math.softmax(tf.pad(xt, [[0, 0], [0, 0], [1, 0]]) / 0.001)
            score = task.score(solution * st_x + mu_x)
            logger.record("score",
                          score, evaluations, percentile=True)
            logger.record(f"rank_corr/model_to_real",
                          spearman(model[:, 0], score[:, 0]), evaluations)

        return score

    # keep track of when to record performance
    interval = trainer.solver_interval
    warmup = trainer.solver_warmup

    scores = []
    predictions = []

    # train model for many epochs with conservatism
    for e in range(config['epochs']):

        statistics = defaultdict(list)
        for x, y in train_data:
            for name, tensor in trainer.train_step(x, y).items():
                statistics[name].append(tensor)

            # evaluate the current solution
            if tf.logical_and(
                    tf.equal(tf.math.mod(trainer.step, interval), 0),
                    tf.math.greater_equal(trainer.step, warmup)):
                scores.append(evaluate_solution(trainer.solution))
                predictions.append(trainer.particle_prediction.numpy())

        for name in statistics.keys():
            logger.record(
                name, tf.concat(statistics[name], axis=0), e)

        statistics = defaultdict(list)
        for x, y in validate_data:
            for name, tensor in trainer.validate_step(x, y).items():
                statistics[name].append(tensor)

        for name in statistics.keys():
            logger.record(
                name, tf.concat(statistics[name], axis=0), e)

        if tf.reduce_all(trainer.done):
            break

    # save the model predictions and scores to be aggregated later
    np.save(os.path.join(config['logging_dir'], "scores.npy"),
            np.concatenate(scores, axis=1))
    np.save(os.path.join(config['logging_dir'], "predictions.npy"),
            np.stack(predictions, axis=1))
