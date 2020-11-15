from ray import tune
import click
import ray
import os


@click.group()
def cli():
    """A group of experiments for training Conservative Score Models
    and reproducing our ICLR 2021 results.
    """


#############


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-dkitty')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def dkitty(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on DKittyMorphology-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "task": "DKittyMorphology-v0",
        "task_kwargs": {"split_percentile": 40, 'num_parallel': 2},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-ant')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def ant(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on AntMorphology-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "task": "AntMorphology-v0",
        "task_kwargs": {"split_percentile": 20, 'num_parallel': 2},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-hopper')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def hopper(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on HopperController-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "task": "HopperController-v0",
        "task_kwargs": {'split_percentile': 100},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-superconductor')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def superconductor(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on Superconductor-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": False,
        "normalize_ys": True,
        "normalize_xs": True,
        "task": "Superconductor-v0",
        "task_kwargs": {'split_percentile': 80},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-molecule')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def molecule(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on MoleculeActivity-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": True,
        "normalize_ys": True,
        "normalize_xs": False,
        "task": "MoleculeActivity-v0",
        "task_kwargs": {'split_percentile': 80},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})


@cli.command()
@click.option('--local-dir', type=str, default='cma-es-gfp')
@click.option('--cpus', type=int, default=24)
@click.option('--gpus', type=int, default=1)
@click.option('--num-parallel', type=int, default=1)
@click.option('--num-samples', type=int, default=1)
def gfp(local_dir, cpus, gpus, num_parallel, num_samples):
    """Evaluate CMA-ES on GFP-v0
    """

    # Final Version

    from design_baselines.cma_es import cma_es
    ray.init(num_cpus=cpus,
             num_gpus=gpus,
             temp_dir=os.path.expanduser('~/tmp'))
    tune.run(cma_es, config={
        "logging_dir": "data",
        "is_discrete": True,
        "normalize_ys": True,
        "normalize_xs": False,
        "task": "GFP-v0",
        "task_kwargs": {'seed': tune.randint(1000), 'split_percentile': 100},
        "bootstraps": 5,
        "val_size": 200,
        "ensemble_batch_size": 100,
        "hidden_size": 256,
        "initial_max_std": 0.2,
        "initial_min_std": 0.1,
        "ensemble_lr": 0.001,
        "ensemble_epochs": 100,
        "cma_sigma": 0.5,
        "solver_samples": 128},
        num_samples=num_samples,
        local_dir=local_dir,
        resources_per_trial={'cpu': cpus // num_parallel,
                             'gpu': gpus / num_parallel - 0.01})
