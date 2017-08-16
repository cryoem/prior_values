from sphire_helix_utils import ms_helix_fundamental as mhf


def test_relion_plot_deg_linear():
    plot = True
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'deg'
    prior_method = 'linear'
    node = 0
    print(mhf.__file__)

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
        method=method,
        prior_method=prior_method,
        node=node
        )


def test_relion_no_plot_deg_linear():
    plot = False
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'deg'
    prior_method = 'linear'
    node = 0


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
        method=method,
        prior_method=prior_method,
        node=node
        )


def test_relion_plot_std_linear():
    plot = True
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'std'
    prior_method = 'linear'
    node = 0


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
        method=method,
        prior_method=prior_method,
        node=node
        )


def test_relion_no_plot_std_linear():
    plot = False
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    tol_std = 1
    tol_mean = 30
    window_size = 3
    plot_lim = 4
    method = 'std'
    prior_method = 'linear'
    node = 0


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
        method=method,
        prior_method=prior_method,
        node=node
        )


if __name__ == '__main__':
    try:
        import ms_helix_fundamental as mhf
    except:
        pass
    test_relion_plot_deg_linear()
    test_relion_no_plot_deg_linear()
    test_relion_plot_std_linear()
    test_relion_no_plot_std_linear()

