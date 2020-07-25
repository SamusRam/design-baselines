from forward_model.utils import spearman
import tensorflow as tf


class Conservative(tf.Module):

    def __init__(self,
                 forward_model,
                 perturbation_distribution,
                 conservative_weight=1.0,
                 optim=tf.keras.optimizers.Adam,
                 **optimizer_kwargs):
        """Build a trainer for a conservative forward model with negatives
        sampled from a perturbation distribution

        Args:

        forward_model: tf.keras.Model
            a keras model that accepts vectorized inputs and returns scores
        perturbation_distribution: Perturbation
            a distribution that returns new samples conditioned on an X
        conservative_weight: float
            the weight of the conservative loss terms
        optim: __class__
            the optimizer class to use such as tf.keras.optimizers.SGD
        **optimizer_kwargs: dict
            additional keyword arguments passed to optim
        """

        super().__init__()
        self.forward_model = forward_model
        self.perturbation_distribution = perturbation_distribution
        self.conservative_weight = conservative_weight
        self.optim = optim(**optimizer_kwargs)
        self.optimizer_kwargs = optimizer_kwargs

    def train(self,
              dataset,
              **kwargs):
        """Train a conservative forward model and collect negative
        samples using a perturbation distribution

        Args:

        dataset: tf.data.Dataset
            the training dataset already batched and prefetched

        Returns:

        loss_dict: dict
            a dictionary mapping names to loss values for logging
        """

        total_loss = tf.zeros([0])
        rank = tf.zeros([0])
        for X, y in dataset:

            with tf.GradientTape() as tape:
                pred = self.forward_model(X)
                loss = tf.keras.losses.mse(y, pred)
                total_loss = tf.concat([total_loss, loss], 0)
                rank = tf.concat([rank, spearman(y[:, 0], pred[:, 0])], 0)

                perturb = tf.stop_gradient(
                    self.perturbation_distribution(X, **kwargs))
                loss = tf.reduce_mean(
                    loss + self.conservative_weight * (
                        self.forward_model(perturb)[:, 0] -
                        self.forward_model(X)[:, 0]))

            grads = tape.gradient(
                loss, self.forward_model.trainable_variables)
            self.optim.apply_gradients(
                zip(grads, self.forward_model.trainable_variables))

        return {"loss_train": total_loss,
                "rank_correlation_train": rank}

    def validate(self,
                 dataset):
        """Validate a conservative forward model using a validation dataset
        and return the average validation loss

        Args:

        dataset: tf.data.Dataset
            the training dataset already batched and prefetched

        Returns:

        loss_dict: dict
            a dictionary mapping names to loss values for logging
        """

        total_loss = tf.zeros([0])
        rank = tf.zeros([0])
        for X, y in dataset:

            pred = self.forward_model(X)
            loss = tf.keras.losses.mse(y, pred)
            total_loss = tf.concat([total_loss, loss], 0)
            rank = tf.concat([rank, spearman(y[:, 0], pred[:, 0])], 0)

        return {"loss_validate": total_loss,
                "rank_correlation_validate": rank}


class ModelInversion(tf.Module):

    def __init__(self,
                 generator,
                 discriminator,
                 latent_size=32,
                 optim=tf.keras.optimizers.Adam,
                 **optimizer_kwargs):
        """Build a trainer for a conservative forward model with negatives
        sampled from a perturbation distribution

        Args:

        generator: tf.keras.Model
            a model that accepts scores and returns designs x
        discriminator: tf.keras.Model
            a model that predicts which design and score pairs are real
        optim: __class__
            the optimizer class to use such as tf.keras.optimizers.SGD
        **optimizer_kwargs: dict
            additional keyword arguments passed to optim
        """

        super().__init__()
        self.generator = generator
        self.discriminator = discriminator
        self.latent_size = latent_size
        self.generator_optim = optim(**optimizer_kwargs)
        self.discriminator_optim = optim(**optimizer_kwargs)
        self.optimizer_kwargs = optimizer_kwargs

    def train(self,
              dataset):
        """Train a conservative forward model and collect negative
        samples using a perturbation distribution

        Args:

        dataset: tf.data.Dataset
            the training dataset already batched and prefetched

        Returns:

        loss_dict: dict
            a dictionary mapping names to loss values for logging
        """

        d_loss = tf.zeros([0])
        real_accuracy = tf.zeros([0])
        g_loss = tf.zeros([0])
        fake_accuracy = tf.zeros([0])
        for X, y, w in dataset:

            with tf.GradientTape() as tape:
                real_p = self.discriminator(tf.concat([X, y], 1))
                real_loss = w * tf.keras.losses.mse(tf.ones_like(y), real_p)
                X_fake = self.generator(tf.concat([
                    tf.random.normal([X.shape[0], self.latent_size]), y], 1))
                fake_p = self.discriminator(tf.concat([X_fake, y], 1))
                fake_loss = w * tf.keras.losses.mse(tf.zeros_like(y), fake_p)
                loss = real_loss + fake_loss
                d_loss = tf.concat([d_loss, loss], 0)
                real_accuracy = tf.concat([
                    real_accuracy, tf.cast(real_p[:, 0] > 0.5, tf.float32)], 0)
                fake_accuracy = tf.concat([
                    fake_accuracy, tf.cast(fake_p[:, 0] < 0.5, tf.float32)], 0)
                loss = tf.reduce_mean(loss)

            grads = tape.gradient(
                loss, self.discriminator.trainable_variables)
            self.discriminator_optim.apply_gradients(
                zip(grads, self.discriminator.trainable_variables))

            with tf.GradientTape() as tape:
                X_fake = self.generator(tf.concat([
                    tf.random.normal([X.shape[0], self.latent_size]), y], 1))
                fake_loss = w * tf.keras.losses.mse(
                    tf.ones_like(y),
                    self.discriminator(tf.concat([X_fake, y], 1)))
                loss = fake_loss
                g_loss = tf.concat([g_loss, loss], 0)
                loss = tf.reduce_mean(loss)

            grads = tape.gradient(
                loss, self.generator.trainable_variables)
            self.generator_optim.apply_gradients(
                zip(grads, self.generator.trainable_variables))

        return {"discriminator_train": d_loss,
                "generator_train": g_loss,
                "real_accuracy": real_accuracy,
                "fake_accuracy": fake_accuracy}

    def validate(self,
                 dataset):
        """Validate a conservative forward model using a validation dataset
        and return the average validation loss

        Args:

        dataset: tf.data.Dataset
            the training dataset already batched and prefetched

        Returns:

        loss_dict: dict
            a dictionary mapping names to loss values for logging
        """

        d_loss = tf.zeros([0])
        real_accuracy = tf.zeros([0])
        g_loss = tf.zeros([0])
        fake_accuracy = tf.zeros([0])
        for X, y, w in dataset:

            real_p = self.discriminator(tf.concat([X, y], 1))
            real_loss = w * tf.keras.losses.mse(tf.ones_like(y), real_p)
            X_fake = self.generator(tf.concat([
                tf.random.normal([X.shape[0], self.latent_size]), y], 1))
            fake_p = self.discriminator(tf.concat([X_fake, y], 1))
            fake_loss = w * tf.keras.losses.mse(tf.zeros_like(y), fake_p)
            loss = real_loss + fake_loss
            d_loss = tf.concat([d_loss, loss], 0)
            real_accuracy = tf.concat([
                real_accuracy, tf.cast(real_p[:, 0] > 0.5, tf.float32)], 0)
            fake_accuracy = tf.concat([
                fake_accuracy, tf.cast(fake_p[:, 0] < 0.5, tf.float32)], 0)

            X_fake = self.generator(tf.concat([
                tf.random.normal([X.shape[0], self.latent_size]), y], 1))
            fake_loss = w * tf.keras.losses.mse(
                tf.ones_like(y),
                self.discriminator(tf.concat([X_fake, y], 1)))
            loss = fake_loss
            g_loss = tf.concat([g_loss, loss], 0)

        return {"discriminator_train": d_loss,
                "generator_train": g_loss,
                "real_accuracy": real_accuracy,
                "fake_accuracy": fake_accuracy}
