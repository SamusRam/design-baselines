from design_baselines.data import StaticGraphTask
from design_baselines.logger import Logger
from design_baselines.utils import spearman
from design_baselines.conservative_ensemble.trainers import ConservativeEnsemble
from design_baselines.conservative_ensemble.nets import ForwardModel
import tensorflow.keras.layers as tfkl
import tensorflow_probability as tfp
import tensorflow as tf
import numpy as np
import os


def conservative_ensemble(config):
    """Train a forward model and perform model based optimization
    using a conservative objective function

    Args:

    config: dict
        a dictionary of hyper parameters such as the learning rate
    """

    # create the training task and logger
    task = StaticGraphTask(config['task'],
                           normalize_x=not config['is_discrete'],
                           normalize_y=True,
                           **config['task_kwargs'])
    train_data, validate_data = task.build(bootstraps=config['bootstraps'],
                                           batch_size=config['batch_size'],
                                           val_size=config['val_size'])
    logger = Logger(config['logging_dir'])

    # make several keras neural networks with two hidden layers
    forward_models = [ForwardModel(
        task.input_shape,
        hidden=config['hidden_size'],
        initial_max_std=config['initial_max_std'],
        initial_min_std=config['initial_min_std'],
        act=tfkl.LeakyReLU) for b in range(config['bootstraps'])]

    # create a trainer for a forward model with a conservative objective
    trainer = ConservativeEnsemble(
        forward_models,
        forward_model_optim=tf.keras.optimizers.Adam,
        forward_model_lr=config['forward_model_lr'],
        target_conservative_gap=config['target_conservative_gap'],
        initial_alpha=config['initial_alpha'],
        alpha_optim=tf.keras.optimizers.Adam,
        alpha_lr=config['alpha_lr'],
        perturbation_lr=config['perturbation_lr'],
        perturbation_steps=config['perturbation_steps'],
        is_discrete=config['is_discrete'])

    # create a manager for saving algorithms state to the disk
    manager = tf.train.CheckpointManager(
        tf.train.Checkpoint(**trainer.get_saveables()),
        os.path.join(config['logging_dir'], 'ckpt'), 1)

    # train the model for an additional number of epochs
    manager.restore_or_initialize()
    trainer.launch(train_data, validate_data, logger, config['epochs'])
    manager.save()

    # select the top k initial designs from the dataset
    indices = tf.math.top_k(task.y[:, 0], k=config['solver_samples'])[1]

    # evaluate the initial design using the oracle and the forward model
    x = tf.gather(task.x, indices, axis=0)

    x = tf.math.log(x) if config['is_discrete'] else x
    solution = tf.math.softmax(x) if config['is_discrete'] else x
    score = task.score(solution)
    prediction = trainer.get_distribution(solution).mean()

    # record the prediction and score to the logger
    logger.record("score", score * task.y_std + task.y_mean, 0)
    logger.record("prediction", prediction * task.y_std + task.y_mean, 0)

    # and keep track of the best design sampled so far
    best_design = None
    best_score = None

    # perform gradient ascent on the score through the forward model
    for i in range(1, config['solver_steps'] + 1):

        # back propagate through the forward model
        with tf.GradientTape() as tape:
            tape.watch(x)
            solution = tf.math.softmax(x) if config['is_discrete'] else x
            score = trainer.get_distribution(solution).mean()
        grads = tape.gradient(score, x)
        x = x + config['solver_lr'] * grads

        # evaluate the design using the oracle and the forward model
        gradient_norm = tf.linalg.norm(grads, axis=1)
        solution = tf.math.softmax(x) if config['is_discrete'] else x
        score = task.score(solution)
        prediction = trainer.get_distribution(solution).mean()

        # record the prediction and score to the logger
        logger.record("gradient_norm", gradient_norm, i)
        logger.record("score", score * task.y_std + task.y_mean, i)
        logger.record("prediction", prediction * task.y_std + task.y_mean, i)

        # update the best design every iteration
        idx = np.argmax(score.numpy())
        if best_design is None or score[idx] > best_score:
            best_score = score[idx]
            best_design = solution[idx]

    # save the best design to the disk
    np.save(os.path.join(
        config['logging_dir'], 'score.npy'), best_score)
    np.save(os.path.join(
        config['logging_dir'], 'design.npy'), best_design)


def conservative_ensemble_predictions(config):
    """Train a forward model and perform model based optimization
    using a conservative objective function

    Args:

    config: dict
        a dictionary of hyper parameters such as the learning rate
    """

    # create the training task and logger
    task = StaticGraphTask(config['task'],
                           normalize_x=not config['is_discrete'],
                           normalize_y=True,
                           **config['task_kwargs'])
    train_data, validate_data = task.build(bootstraps=config['bootstraps'],
                                           batch_size=config['batch_size'],
                                           val_size=config['val_size'])
    logger = Logger(config['logging_dir'])

    # make several keras neural networks with two hidden layers
    conservative_forward_models = [ForwardModel(
        task.input_shape,
        hidden=config['hidden_size'],
        initial_max_std=config['initial_max_std'],
        initial_min_std=config['initial_min_std'],
        act=lambda: tfkl.LeakyReLU(alpha=0.3)) for b in range(config['bootstraps'])]

    # create a trainer for a forward model with a conservative objective
    conservative_trainer = ConservativeEnsemble(
        conservative_forward_models,
        forward_model_optim=tf.keras.optimizers.Adam,
        forward_model_lr=config['forward_model_lr'],
        target_conservative_gap=config['target_conservative_gap'],
        initial_alpha=config['initial_alpha'],
        alpha_optim=tf.keras.optimizers.Adam,
        alpha_lr=config['alpha_lr'],
        perturbation_lr=config['perturbation_lr'],
        perturbation_steps=config['perturbation_steps'],
        is_discrete=config['is_discrete'])

    # create a manager for saving algorithms state to the disk
    conservative_manager = tf.train.CheckpointManager(
        tf.train.Checkpoint(**conservative_trainer.get_saveables()),
        os.path.join(config['logging_dir'], 'conservative'), 1)

    # train the model for an additional number of epochs
    conservative_manager.restore_or_initialize()
    conservative_trainer.launch(train_data, validate_data, logger,
                                config['epochs'], header='conservative/')
    conservative_manager.save()

    # make several keras neural networks with two hidden layers
    vanilla_forward_models = [ForwardModel(
        task.input_shape,
        hidden=config['hidden_size'],
        initial_max_std=config['initial_max_std'],
        initial_min_std=config['initial_min_std'],
        act=lambda: tfkl.LeakyReLU(alpha=0.7)) for b in range(config['bootstraps'])]

    # create a trainer for a forward model with a conservative objective
    vanilla_trainer = ConservativeEnsemble(
        vanilla_forward_models,
        forward_model_optim=tf.keras.optimizers.Adam,
        forward_model_lr=config['forward_model_lr'],
        target_conservative_gap=0.0,
        initial_alpha=0.0,
        alpha_optim=tf.keras.optimizers.Adam,
        alpha_lr=0.0,
        perturbation_lr=0.0,
        perturbation_steps=0,
        is_discrete=config['is_discrete'])

    # create a manager for saving algorithms state to the disk
    vanilla_manager = tf.train.CheckpointManager(
        tf.train.Checkpoint(**vanilla_trainer.get_saveables()),
        os.path.join(config['logging_dir'], 'vanilla'), 1)

    # train the model for an additional number of epochs
    vanilla_manager.restore_or_initialize()
    vanilla_trainer.launch(train_data, validate_data, logger,
                           config['epochs'], header='vanilla/')
    vanilla_manager.save()

    # select the top k initial designs from the dataset
    indices = tf.math.top_k(task.y[:, 0], k=config['solver_samples'])[1]

    # evaluate the initial design using the oracle and the forward model
    x = tf.gather(task.x, indices, axis=0)

    x = tf.math.log(x) if config['is_discrete'] else x
    solution = tf.math.softmax(x) if config['is_discrete'] else x
    score = task.score(solution)
    prediction0 = conservative_trainer.get_distribution(solution).mean()
    prediction1 = vanilla_trainer.get_distribution(solution).mean()

    # record the prediction and score to the logger
    logger.record("score", score * task.y_std + task.y_mean, 0)
    logger.record("conservative/prediction", prediction0 * task.y_std + task.y_mean, 0)
    logger.record("vanilla/prediction", prediction1 * task.y_std + task.y_mean, 0)
    logger.record("rank_corr/conservative_to_vanilla",
                  spearman(prediction0[:, 0], prediction1[:, 0]), 0)
    logger.record("rank_corr/conservative_to_real",
                  spearman(prediction0[:, 0], score[:, 0]), 0)
    logger.record("rank_corr/real_to_vanilla",
                  spearman(score[:, 0], prediction1[:, 0]), 0)

    # perform gradient ascent on the score through the forward model
    for i in range(1, config['solver_steps'] + 1):

        # back propagate through the conservative model
        with tf.GradientTape() as tape:
            tape.watch(x)
            solution = tf.math.softmax(x) if config['is_discrete'] else x
            score = conservative_trainer.get_distribution(solution).mean()
        conservative_grads = tape.gradient(score, solution)

        # back propagate through the vanilla model
        with tf.GradientTape() as tape:
            tape.watch(x)
            solution = tf.math.softmax(x) if config['is_discrete'] else x
            score = vanilla_trainer.get_distribution(solution).mean()
        vanilla_grads = tape.gradient(score, solution)

        # use the conservative optimizer to update the solution
        x = x + config['solver_lr'] * conservative_grads
        solution = tf.math.softmax(x) if config['is_discrete'] else x

        # calculate the element-wise gradient correlation
        gradient_corr = tfp.stats.correlation(
            conservative_grads, vanilla_grads,
            sample_axis=0, event_axis=None)

        # evaluate the design using the oracle and the forward model
        gradient_norm = tf.linalg.norm(conservative_grads, axis=1)
        score = task.score(solution)
        prediction0 = conservative_trainer.get_distribution(solution).mean()
        prediction1 = vanilla_trainer.get_distribution(solution).mean()

        # record the prediction and score to the logger
        logger.record("gradient_corr", gradient_corr, i)
        logger.record("gradient_norm", gradient_norm, i)
        logger.record("score", score * task.y_std + task.y_mean, i)
        logger.record("conservative/prediction", prediction0 * task.y_std + task.y_mean, i)
        logger.record("vanilla/prediction", prediction1 * task.y_std + task.y_mean, i)
        logger.record("rank_corr/conservative_to_vanilla",
                      spearman(prediction0[:, 0], prediction1[:, 0]), i)
        logger.record("rank_corr/conservative_to_real",
                      spearman(prediction0[:, 0], score[:, 0]), i)
        logger.record("rank_corr/real_to_vanilla",
                      spearman(score[:, 0], prediction1[:, 0]), i)
