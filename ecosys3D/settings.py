from collections import namedtuple, OrderedDict

Setting = namedtuple('setting', ('default', 'type', 'description'))

SETTINGS = OrderedDict([
    ('identifier', Setting('UNNAMED', str, 'Identifier of the current simulation')),

    # Model parameters
    ('nx', Setting(0, int, 'Grid points in zonal (x) direction')),
    ('ny', Setting(0, int, 'Grid points in meridional (y,j) direction')),
    ('nz', Setting(0, int, 'Grid points in vertical (z,k) direction')),
    ('dt', Setting(0., float, 'Time step')),
    ('runlen', Setting(0., float, 'Length of simulation in seconds')),
    ('AB_eps', Setting(0.1, float, 'Deviation from Adam-Bashforth weighting')),

#    # Logical switches for general model setup
#    ('coord_degree', Setting(False, bool, 'either spherical (True) or cartesian (False) coordinates')),
#    ('enable_cyclic_x', Setting(False, bool, 'enable cyclic boundary conditions'))
#    ('enable_superbee_advection', Setting(False, bool, 'enable advection scheme with implicit mixing')),
#   
#    ('enable_noslip_lateral', Setting(False, bool, 'enable lateral no-slip boundary conditions in harmonic- and biharmonic friction.')),
#
#    # External mode
#    ('congr_epsilon', Setting(1e-12, float, 'convergence criteria for Poisson solver')),
#    ('congr_max_iterations', Setting(1000, int, 'maximum number of Poisson solver iterations')),

    # New
    ('use_io_threads', Setting(False, bool, 'Start extra threads for disk writes')),
    ('io_timeout', Setting(20, float, 'Timeout in seconds while waiting for IO locks to be released')),
    ('enable_netcdf_zlib_compression', Setting(True, bool, 'Use netCDF4\'s native zlib interface, which leads to smaller output files (but carries some computational overhead).')),
    ('enable_hdf5_gzip_compression', Setting(True, bool, 'Use h5py\'s native gzip interface, which leads to smaller restart files (but carries some computational overhead).')),
    ('restart_input_filename', Setting('', str, 'File name of restart input. If not given, no restart data will be read.')),
    ('restart_output_filename', Setting('{identifier}_{itt:0>4d}.restart.h5', str, 'File name of restart output. May contain Python format syntax that is substituted with Veros attributes.')),
    ('restart_frequency', Setting(0, float, 'Frequency (in seconds) to write restart data')),
    ('force_overwrite', Setting(False, bool, 'Overwrite existing output files')),
    ('pyom_compatibility_mode', Setting(False, bool, 'Force compatibility to pyOM2 (even reproducing bugs and other quirks). For testing purposes only.')),
    ('diskless_mode', Setting(False, bool, 'Suppress all output to disk. Mainly used for testing purposes.')),
    ('default_float_type', Setting('float64', str, 'Default type to use for floating point arrays (e.g. ``float32`` or ``float64``).')),
])


def set_default_settings(vs):
    for key, setting in SETTINGS.items():
        setattr(vs, key, setting.type(setting.default))


def check_setting_conflicts(vs):
    if vs.enable_tke and not vs.enable_implicit_vert_friction:
        raise RuntimeError('use TKE model only with implicit vertical friction'
                           '(set enable_implicit_vert_fricton)')
