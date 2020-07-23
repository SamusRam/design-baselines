import tensorflow as tf
import numpy as np
import tensorflow.keras.layers as tfkl
import gym
import os


class PolicyWeightsDataset(object):

    def load_resources(self,
                       seed=0,
                       x_file='hopper_controller_X.txt',
                       y_file='hopper_controller_y.txt'):
        """Load static datasets of weights and their corresponding
        expected returns from the disk
        """

        np.random.seed(seed)

        basedir = os.path.dirname(os.path.abspath(__file__))
        x = np.loadtxt(os.path.join(basedir, x_file))
        y = np.loadtxt(os.path.join(basedir, y_file))

        x = x.astype(np.float32)
        y = y.astype(np.float32).reshape([-1, 1])

        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)

        self.x = x[indices]
        self.y = y[indices]

    def build(self):
        """Load static datasets of weights and their corresponding
        expected returns from the disk
        """

        train = tf.data.Dataset.from_tensor_slices((
            self.x[self.val_size:], self.y[self.val_size:]))
        val = tf.data.Dataset.from_tensor_slices((
            self.x[:self.val_size], self.y[:self.val_size]))

        train = train.shuffle(self.x.shape[0] - self.val_size)
        val = val.shuffle(self.val_size)

        train = train.batch(self.batch_size)
        val = val.batch(self.batch_size)

        self.train = train.prefetch(tf.data.experimental.AUTOTUNE)
        self.val = val.prefetch(tf.data.experimental.AUTOTUNE)

    def __init__(self,
                 obs_dim=11,
                 action_dim=3,
                 hidden_dim=64,
                 val_size=200,
                 batch_size=32,
                 env_name='Hopper-v2',
                 seed=0,
                 x_file='hopper_controller_X.txt',
                 y_file='hopper_controller_y.txt'):
        """Load static datasets of weights and their corresponding
        expected returns from the disk
        """

        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.val_size = val_size
        self.batch_size = batch_size
        self.env_name = env_name

        self.x = None
        self.y = None
        self.train = None
        self.val = None

        self.load_resources(seed=seed, x_file=x_file, y_file=y_file)
        self.build()

    @property
    def input_shape(self):
        """Return the number of weights and biases in the design
        space of the policy

        Returns:

        n: int
            the number of weights in a single data point
        """

        return self.x.shape[1],

    def score(self, x):
        """Assign a score to a large set of wrights provided by
        performing a rollout in an environment

        Args:

        x: tf.Tensor
            a batch of designs that will be evaluated using an oracle

        Returns:

        score: tf.Tensor
            a vector of returns for policies whose weights are x[i]
        """

        y = tf.map_fn(self.score_backend_tf, x)
        y.set_shape(x.get_shape()[:1])
        return y

    def score_backend_tf(self, x):
        """Assign a score to a single set of weights provided by
        performing a rollout in an environment

        Args:

        x: np.ndarray
            a single design that will be evaluated using an oracle

        Returns:

        score: np.ndarray
            a return for a policy whose weights are x
        """

        return tf.numpy_function(self.score_backend_np, [x], tf.float32)

    def score_backend_np(self, x) -> np.ndarray:
        """Assign a score to a single set of wrights provided by
        performing a rollout in an environment

        Args:

        x: np.ndarray
            a single design that will be evaluated using an oracle

        Returns:

        score: np.ndarray
            a return for a policy whose weights are x
        """

        # make a copy of the policy and the environment
        env = gym.make(self.env_name)
        policy = tf.keras.Sequential([
            tfkl.Dense(self.hidden_dim, use_bias=True, input_shape=(self.obs_dim,)),
            tfkl.Activation('tanh'),
            tfkl.Dense(self.hidden_dim, use_bias=True),
            tfkl.Activation('tanh'),
            tfkl.Dense(self.action_dim, use_bias=True)])

        # extract weights from the vector design
        weights = []
        for s in [(self.obs_dim, self.hidden_dim),
                  (self.hidden_dim,),
                  (self.hidden_dim, self.hidden_dim),
                  (self.hidden_dim,),
                  (self.hidden_dim, self.action_dim),
                  (self.action_dim,),
                  (1, self.action_dim)]:
            weights.append(x[0:np.prod(s)].reshape(s))
            x = x[np.prod(s):]

        # the final weight is logstd and is not used
        weights.pop(-1)

        # set the policy weights to those provided
        policy.set_weights(weights)

        # perform a single rollout for quick evaluation
        obs, done = env.reset(), False
        path_returns = 0.0
        while not done:
            act = policy(obs[np.newaxis])[0]
            obs, rew, done, info = env.step(act)
            path_returns += rew
        return np.array(path_returns).astype(np.float32)
