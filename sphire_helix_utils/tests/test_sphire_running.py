from sphire_helix_utils import ms_helix_fundamental as mhf
import shutil


def test_sphire_plot_deg_running():
    plot = True
    typ = 'sphire'
    name = 'bdb:stack'
    index = 'index.txt'
    params = 'params.txt'
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'deg'
    prior_method = 'running'
    node = 0

    shutil.copy2('index_raw.txt', 'index.txt')
    shutil.copy2('params_raw.txt', 'params.txt')

    mhf.calculate_priors(
        plot=plot,
        typ=typ,
        tracker=name,
        index_file=index,
        params_file=params,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        tol_mean=tol_mean,
        window_size=window_size,
        plot_lim=plot_lim,
        outlier_method=method,
        prior_method=prior_method,
        node=node
        )


def test_sphire_no_plot_deg_running():
    plot = False
    typ = 'sphire'
    name = 'bdb:stack'
    index = 'index.txt'
    params = 'params.txt'
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'deg'
    prior_method = 'running'
    node = 0

    shutil.copy2('index_raw.txt', 'index.txt')
    shutil.copy2('params_raw.txt', 'params.txt')

    mhf.calculate_priors(
        plot=plot,
        typ=typ,
        tracker=name,
        index_file=index,
        params_file=params,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        tol_mean=tol_mean,
        window_size=window_size,
        plot_lim=plot_lim,
        outlier_method=method,
        prior_method=prior_method,
        node=node
        )


def test_sphire_plot_std_running():
    plot = True
    typ = 'sphire'
    name = 'bdb:stack'
    index = 'index.txt'
    params = 'params.txt'
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'std'
    prior_method = 'running'
    node = 0

    shutil.copy2('index_raw.txt', 'index.txt')
    shutil.copy2('params_raw.txt', 'params.txt')

    mhf.calculate_priors(
        plot=plot,
        typ=typ,
        tracker=name,
        index_file=index,
        params_file=params,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        tol_mean=tol_mean,
        window_size=window_size,
        plot_lim=plot_lim,
        outlier_method=method,
        prior_method=prior_method,
        node=node
        )


def test_sphire_no_plot_std_running():
    plot = False
    typ = 'sphire'
    name = 'bdb:stack'
    index = 'index.txt'
    params = 'params.txt'
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'std'
    prior_method = 'running'
    node = 0

    shutil.copy2('index_raw.txt', 'index.txt')
    shutil.copy2('params_raw.txt', 'params.txt')

    mhf.calculate_priors(
        plot=plot,
        typ=typ,
        tracker=name,
        index_file=index,
        params_file=params,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        tol_mean=tol_mean,
        window_size=window_size,
        plot_lim=plot_lim,
        outlier_method=method,
        prior_method=prior_method,
        node=node
        )


if __name__ == '__main__':
    try:
        import ms_helix_fundamental as mhf
    except:
        pass
    test_sphire_plot_deg_running()
    test_sphire_no_plot_deg_running()
    test_sphire_plot_std_running()
    test_sphire_no_plot_std_running()

