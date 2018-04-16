from sphire_helix_utils import ms_helix_fundamental as mhf
import ms_helix_fundamental as mhf


def test_relion_plot():
    plot = True
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    window_size = 3
    plot_lim = 4
    method = 'deg'


    mhf.calculate_priors(
        tracker=name,
        params_file=params,
        index_file=index,
        typ=typ,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        plot=plot,
        plot_lim=plot_lim,
        method=method,
        window_size=window_size
        )


def test_relion_no_plot():
    plot = False
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    window_size = 3
    plot_lim = 4
    method = 'deg'


    mhf.calculate_priors(
        tracker=name,
        params_file=params,
        index_file=index,
        typ=typ,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        plot=plot,
        plot_lim=plot_lim,
        method=method,
        window_size=window_size
        )


def test_relion_std_plot():
    plot = True
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    window_size = 3
    plot_lim = 4
    method='std'
    tol_std = 1


    mhf.calculate_priors(
        tracker=name,
        params_file=params,
        index_file=index,
        typ=typ,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        plot=plot,
        plot_lim=plot_lim,
        method=method,
        window_size=window_size
        )


def test_relion_std_no_plot():
    plot = False
    typ = 'relion'
    name = 'data_test.star'
    index = None
    params = None
    tol_psi = 30
    tol_theta = 15
    tol_filament = 0.2
    window_size = 3
    plot_lim = 4
    method='std'
    tol_std = 1


    mhf.calculate_priors(
        tracker=name,
        params_file=params,
        index_file=index,
        typ=typ,
        tol_psi=tol_psi,
        tol_theta=tol_theta,
        tol_filament=tol_filament,
        tol_std=tol_std,
        plot=plot,
        plot_lim=plot_lim,
        method=method,
        window_size=window_size
        )


if __name__ == '__main__':
    test_relion_plot()
    test_relion_no_plot()
    test_relion_std_plot()
    test_relion_std_no_plot()

