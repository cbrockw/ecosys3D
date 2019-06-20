import abc

from loguru import logger

from ecosys3D import (
                   settings, time, handlers, logs, distributed, progress,
                   runtime_settings as rs, runtime_state as rst
                   )
from ecosys3D.state import ecoState
from ecosys3D.timer import Timer
from ecosys3D.core import (
                        numerics, advection, utilities, ecosystem
                        )

class ecoSetup(metaclass=abc.ABCMeta):
    """Main class for Ecosys3D, used for building a model and running it.
    
    Note:
    This class is meant to be subclassed. Subclasses need to implement the
    methods :meth:`set_parameter`, :meth:`set_topography`, :meth:`set_grid`,
    :meth:`set_coriolis`, :meth:`set_initial_conditions`, :meth:`set_forcing`,
    and :meth:`set_diagnostics`.
    
    Arguments:
    backend (:obj:`bool`, optional): Backend to use for array operations.
    Possible values are ``numpy`` and ``bohrium``. Defaults to ``None``, which
    tries to read the backend from the command line (set via a flag
    ``-b``/``--backend``), and uses ``numpy`` if no command line argument is given.
    loglevel (one of {debug, info, warning, error, critical}, optional): Verbosity
    of the model. Tries to read value from command line if not given
    (``-v``/``--loglevel``). Defaults to ``info``.
    
    Example:
    >>> import matplotlib.pyplot as plt
    >>> from veros import VerosSetup
    >>>
    >>> class MyModel(VerosSetup):
    >>>     ...
    >>>
    >>> simulation = MyModel(backend='bohrium')
    >>> simulation.run()
    >>> plt.imshow(simulation.state.psi[..., 0])
    >>> plt.show()
    
    """
    
    def __init__(self, state=None, override=None):
        self.override_settings = override or {}
        logs.setup_logging(loglevel=rs.loglevel)
        
        if state is None:
            self.state = ecoState()
        
        self.state.timers = {k: Timer(k) for k in (
                                                   'setup', 'main'
                                                   )}
    @abc.abstractmethod
    def set_parameter(self, vs):
        """To be implemented by subclass.
        
        First function to be called during setup.
        Use this to modify the model settings.
        
        Example:
        >>> def set_parameter(self, vs):
        >>>     vs.nx, vs.ny, vs.nz = (360, 120, 50)
        >>>     vs.coord_degree = True
        >>>     vs.enable_cyclic = True
        """
        pass

    def setup(self):
        vs = self.state

        with vs.timers['setup']:
            logger.info('Setting up everything')
    
#            self.set_parameter(vs)
#
#            for setting, value in self.override_settings.items():
#                setattr(vs, setting, value)
#
#            settings.check_setting_conflicts(vs)
#            distributed.validate_decomposition(vs)
#            vs.allocate_variables()
#
#            self.set_grid(vs)
#            numerics.calc_grid(vs)
#
#            self.set_coriolis(vs)
#            numerics.calc_beta(vs)
#
#            self.set_topography(vs)
#            numerics.calc_topo(vs)
#
#            self.set_initial_conditions(vs)
#            numerics.calc_initial_conditions(vs)
#            streamfunction.streamfunction_init(vs)
#            eke.init_eke(vs)
#
#            vs.diagnostics = diagnostics.create_diagnostics(vs)
#            self.set_diagnostics(vs)
#            diagnostics.initialize(vs)
#            diagnostics.read_restart(vs)
#
#            self.set_forcing(vs)
#            isoneutral.check_isoneutral_slope_crit(vs)

    def run(self, show_progress_bar=None):
        """Main routine of the simulation.
        
        Note:
        Make sure to call :meth:`setup` prior to this function.
        
        Arguments:
        show_progress_bar (:obj:`bool`, optional): Whether to show fancy progress bar via tqdm.
        By default, only show if stdout is a terminal and Veros is running on a single process.
        """
        vs = self.state
                
        logger.info('\nStarting integration for {0[0]:.1f} {0[1]}'.format(time.format_time(vs.runlen)))
                
        start_time, start_iteration = vs.time, vs.itt
        profiler = None
                        
        pbar = progress.get_progress_bar(vs, use_tqdm=show_progress_bar)
                        
        with handlers.signals_to_exception():
            try:
                with pbar:
                    while vs.time - start_time < vs.runlen:
                        with vs.timers['diagnostics']:
                            diagnostics.write_restart(vs)
                    
                        if vs.itt - start_iteration == 3 and rs.profile_mode and rst.proc_rank == 0:
                        # when using bohrium, most kernels should be pre-compiled by now
                            profiler = diagnostics.start_profiler()
                        
                        with vs.timers['main']:
                            self.set_forcing(vs)
                            
                            utilities.enforce_boundaries(vs, vs.u[:, :, :, vs.taup1])
                            utilities.enforce_boundaries(vs, vs.v[:, :, :, vs.taup1])

                        vs.itt += 1
                        vs.time += vs.dt_tracer
                        pbar.advance_time(vs.dt_tracer)

                        self.after_timestep(vs)

                        with vs.timers['diagnostics']:
                            if not diagnostics.sanity_check(vs):
                                raise RuntimeError('solution diverged at iteration {}'.format(vs.itt))

                            if vs.enable_neutral_diffusion and vs.enable_skew_diffusion:
                                isoneutral.isoneutral_diag_streamfunction(vs)

                            diagnostics.diagnose(vs)
                            diagnostics.output(vs)
                                
                        # NOTE: benchmarks parse this, do not change / remove
                        logger.debug(' Time step took {:.2f}s', vs.timers['main'].get_last_time())

                        # permutate time indices
                        vs.taum1, vs.tau, vs.taup1 = vs.tau, vs.taup1, vs.taum1

            except:
                logger.critical('Stopping integration at iteration {}', vs.itt)
                raise
            else:
                logger.success('Integration done\n')
            finally:
                #diagnostics.write_restart(vs, force=True)
                logger.debug('\n'.join([
                    '',
                    'Timing summary:',
                    ' setup time               = {:.2f}s'.format(vs.timers['setup'].get_time()),
                    ' main loop time           = {:.2f}s'.format(vs.timers['main'].get_time()),
                ]))

                if profiler is not None:
                    diagnostics.stop_profiler(profiler)
