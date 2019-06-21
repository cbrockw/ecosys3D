#!/usr/bin/env python

from ecosys3D import ecoSetup, eco_method
import ecosys3D.tools

class testSetup(ecoSetup):
    """A test model"""
    @eco_method
    def set_parameter(self, vs):
        vs.identifier = 'test'
        
        vs.nx, vs.ny, vs.nz = 30, 42, 15
        vs.dt = 86400 / 2.
        vs.runlen = 86400 * 30
        
        vs.coord_degree = True
        vs.enable_cyclic_x = True
    
    @eco_method
    def read_grid(self, vs):
        ddz = np.array([50., 70., 100., 140., 190., 240., 290., 340.,
                        390., 440., 490., 540., 590., 640., 690.])
        vs.dxt[...] = 2.0
        vs.dyt[...] = 2.0
        vs.x_origin = 0.0
        vs.y_origin = -40.0
        vs.dzt[...] = ddz[::-1] / 2.5
        
    @eco_method
    def read_topography(self, vs):
        x, y = np.meshgrid(vs.xt, vs.yt, indexing='ij')
    
    @eco_method
    def read_initial_conditions(self, vs):
        vs.test=1
    
    @eco_method
    def set_forcing(self, vs):
        vs.test=1
    
    @eco_method
    def set_diagnostics(self, vs):
        vs.diagnostics['snapshot'].output_frequency = 86400 * 10
        vs.diagnostics['averages'].output_variables = ('salt', 'temp', 'u', 'v', 'w', 'psi', 'rho', 'surface_taux', 'surface_tauy')
        vs.diagnostics['averages'].output_frequency = 10 * 86400.
        vs.diagnostics['averages'].sampling_frequency = vs.dt * 10
 

    @eco_method
    def after_timestep(self, vs):
        pass

@ecosys3D.tools.cli
def run(*args, **kwargs):
    simulation = testSetup(*args, **kwargs)
    simulation.setup()
    simulation.run()


if __name__ == '__main__':
    run()
