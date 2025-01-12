from ray import tune
import click
import ray
import os
from random import randint


@click.group()
def cli():
    """A cleaned up implementation of Conservative Objective Models
    for reproducing some of our ICML 2021 rebuttal results.
    """


# CLEANED UP VERSION OF COMS - INTENDED FOR RELEASE POST-ICML 2021


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-dkitty')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def dkitty(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on DKittyMorphology-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "DKittyMorphology-v0",
        "task_kwargs": {"split_percentile": 40, 'num_parallel': 2},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 50,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "train_beta": 0.4,
        "eval_beta": 0.4
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-ant')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def ant(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on AntMorphology-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "AntMorphology-v0",
        "task_kwargs": {"split_percentile": 20, 'num_parallel': 2},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.4,
        "eval_beta": 0.4,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.4,
        "eval_beta": 0.4,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-superconductor')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def superconductor(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on Superconductor-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "Superconductor-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 50,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "train_beta": 0.4,
        "eval_beta": 0.4
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-molecule')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def molecule(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on MoleculeActivity-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "MoleculeActivity-v0",
        "task_kwargs": {'split_percentile': 80},
        "is_discrete": True,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "discrete_clip": 0.6,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 50,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "train_beta": 0.4,
        "eval_beta": 0.4
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-gfp')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
@click.option('--difficulty', type=str, default='medium')
def gfp(local_dir, cpus, gpus, num_parallel, num_samples, difficulty):
    """Evaluate Conservative Objective Models on GFP-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    try:
        difficulty_2_task = {'medium': "GFP-TransformerMedium-v0",
                             "hard": "GFP-TransformerHard-v0",
                             "easy": "GFP-TransformerEasy-v0",
                             "none": "GFP-v0"}
        task_name = difficulty_2_task[difficulty]
    except KeyError:
        raise NotImplementedError(
            f'The currently supported difficulty levels are: {",".join(difficulty_2_task.keys())}')

    tune.run(coms_cleaned, config={
            "logging_dir": "data",
            "task": task_name,
            "task_relabel": False,
            "task_max_samples": None,
            "task_distribution": None,
            "normalize_ys": True,
            "normalize_xs": False,
            "in_latent_space": False,
            "vae_hidden_size": 64,
            "vae_latent_size": 256,
            "vae_activation": "relu",
            "vae_kernel_size": 3,
            "vae_num_blocks": 4,
            "vae_lr": 0.0003,
            "vae_beta": 1.0,
            "vae_batch_size": 128,
            "vae_val_size": 200,
            "vae_epochs": 10,
            "particle_lr": 2.0,
            "particle_train_gradient_steps": 1000,
            "particle_evaluate_gradient_steps": 1000,
            "particle_entropy_coefficient": 0.0,
            "forward_model_activations": ["relu", "relu"],
            "forward_model_hidden_size": 2048,
            "forward_model_final_tanh": False,
            "forward_model_lr": 0.0003,
            "forward_model_alpha": 0.1,
            "forward_model_alpha_lr": 0.01,
            "forward_model_overestimation_limit": 2,
            "forward_model_noise_std": 0.0,
            "forward_model_batch_size": 128,
            "forward_model_val_size": 500,
            "forward_model_epochs": 50,
            "evaluation_samples": 2121,
            "fast": False
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-tfbind8')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def tfbind8(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on TfBind8-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "TfBind8-v0",
        "task_kwargs": {'split_percentile': 20},
        "is_discrete": True,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "discrete_clip": 0.6,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 50,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "train_beta": 0.4,
        "eval_beta": 0.4
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


# studying changes to COMs


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_tanh(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": 0.0,
        "final_tanh": True,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_tanh_no_cons(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 0.0,
        "alpha_lr": 0.0,
        "target_conservatism": 0.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": 0.0,
        "final_tanh": True,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_entropy(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": tune.grid_search([0.0, 0.01, 0.05, 0.1,
                                                 0.5, 1.0, 5.0, 10.0]),
        "final_tanh": False,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_entropy_no_cons(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 0.0,
        "alpha_lr": 0.0,
        "target_conservatism": 0.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": tune.grid_search([0.0, 0.01, 0.05, 0.1,
                                                 0.5, 1.0, 5.0, 10.0]),
        "final_tanh": False,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_tanh_denorm(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": False,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": 0.0,
        "final_tanh": True,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_tanh_no_cons_denorm(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": False,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 0.0,
        "alpha_lr": 0.0,
        "target_conservatism": 0.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": 0.0,
        "final_tanh": True,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_entropy_denorm(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": False,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 1.0,
        "alpha_lr": 0.01,
        "target_conservatism": -2.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": tune.grid_search([0.0, 0.01, 0.05, 0.1,
                                                 0.5, 1.0, 5.0, 10.0]),
        "final_tanh": False,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper_entropy_no_cons_denorm(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate Conservative Objective Models on HopperController-v0
    """

    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    tune.run(coms_cleaned, config={
        "logging_dir": "data",
        "task": "HopperController-v0",
        "task_kwargs": {},
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": False,
        "continuous_noise_std": 0.2,
        "val_size": 500,
        "batch_size": 128,
        "epochs": 20,
        "activations": ['leaky_relu', 'leaky_relu'],
        "hidden": 2048,
        "max_std": 0.2,
        "min_std": 0.1,
        "forward_model_lr": 0.0003,
        "train_beta": 0.0,
        "eval_beta": 0.0,
        "initial_alpha": 0.0,
        "alpha_lr": 0.0,
        "target_conservatism": 0.0,
        "inner_lr": 0.05,
        "outer_lr": 0.05,
        "inner_gradient_steps": 1,
        "outer_gradient_steps": 50,
        "entropy_coefficient": tune.grid_search([0.0, 0.01, 0.05, 0.1,
                                                 0.5, 1.0, 5.0, 10.0]),
        "final_tanh": False,
        },
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-aav')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
@click.option('--difficulty', type=str, default='medium')
def aav(local_dir, cpus, gpus, num_parallel, num_samples, difficulty):
    """Evaluate CoMs on AAV viral viability prediction
    """
    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    try:
        difficulty_2_task = {'medium': "AAV-FixedLength-v0",
                             "hard": "AAV-FixedLengthHard-v0",
                             "easy": "AAV-FixedLengthEasy-v0"}
        task_name = difficulty_2_task[difficulty]
    except KeyError:
        raise NotImplementedError(
            f'The currently supported difficulty levels are: {",".join(difficulty_2_task.keys())}')

    tune.run(coms_cleaned, config={
            "logging_dir": "data",
            "task": task_name,
            "task_relabel": False,
            "task_max_samples": None,
            "task_distribution": None,
            "normalize_ys": True,
            "normalize_xs": False,
            "in_latent_space": False,
            "vae_hidden_size": 64,
            "vae_latent_size": 256,
            "vae_activation": "relu",
            "vae_kernel_size": 3,
            "vae_num_blocks": 4,
            "vae_lr": 0.0003,
            "vae_beta": 1.0,
            "vae_batch_size": 128,
            "vae_val_size": 200,
            "vae_epochs": 10,
            "particle_lr": 2.0,
            "particle_train_gradient_steps": 50,
            "particle_evaluate_gradient_steps": 50,
            "particle_entropy_coefficient": 0.0,
            "forward_model_activations": ["relu", "relu"],
            "forward_model_hidden_size": 2048,
            "forward_model_final_tanh": False,
            "forward_model_lr": 0.0003,
            "forward_model_alpha": 0.1,
            "forward_model_alpha_lr": 0.01,
            "forward_model_overestimation_limit": 2,
            "forward_model_noise_std": 0.0,
            "forward_model_batch_size": 128,
            "forward_model_val_size": 500,
            "forward_model_epochs": 50,
            "evaluation_samples": 2121,
            "fast": False
        },
             num_samples=num_samples,
             local_dir=local_dir,
             resources_per_trial={'cpu': cpus // num_parallel,
                                  'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='coms-cleaned-gb1')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
@click.option('--difficulty', type=str, default='medium')
def gb1(local_dir, cpus, gpus, num_parallel, num_samples, difficulty):
    """Evaluate CoMs on GB1
    """
    from design_baselines.coms_cleaned import coms_cleaned
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             include_dashboard=False,
             _temp_dir=os.path.expanduser('~/tmp'))
    try:
        difficulty_2_task = {'medium': "GB1-FixedLength-v0",
                             "hard": "GB1-FixedLengthHard-v0",
                             "easy": "GB1-FixedLengthEasy-v0"}
        task_name = difficulty_2_task[difficulty]
    except KeyError:
        raise NotImplementedError(
            f'The currently supported difficulty levels are: {",".join(difficulty_2_task.keys())}')

    tune.run(coms_cleaned, config={
            "logging_dir": "data",
            "task": task_name,
            "task_relabel": False,
            "task_max_samples": None,
            "task_distribution": None,
            "normalize_ys": True,
            "normalize_xs": False,
            "in_latent_space": False,
            "vae_hidden_size": 64,
            "vae_latent_size": 256,
            "vae_activation": "relu",
            "vae_kernel_size": 3,
            "vae_num_blocks": 4,
            "vae_lr": 0.0003,
            "vae_beta": 1.0,
            "vae_batch_size": 128,
            "vae_val_size": 200,
            "vae_epochs": 10,
            "particle_lr": 2.0,
            "particle_train_gradient_steps": 50,
            "particle_evaluate_gradient_steps": 50,
            "particle_entropy_coefficient": 0.0,
            "forward_model_activations": ["relu", "relu"],
            "forward_model_hidden_size": 2048,
            "forward_model_final_tanh": False,
            "forward_model_lr": 0.0003,
            "forward_model_alpha": 0.1,
            "forward_model_alpha_lr": 0.01,
            "forward_model_overestimation_limit": 2,
            "forward_model_noise_std": 0.0,
            "forward_model_batch_size": 128,
            "forward_model_val_size": 500,
            "forward_model_epochs": 50,
            "evaluation_samples": 2121,
            "fast": False
        },
             num_samples=num_samples,
             local_dir=local_dir,
             resources_per_trial={'cpu': cpus // num_parallel,
                                  'gpu': gpus / num_parallel - 0.01})