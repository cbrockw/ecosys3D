"""Ecosys3D a marine ecosystem simulator"""
import sys
import types

class _PublicAPI(types.ModuleType):
    @property
    def __version__(self):
        from ecosys3D._version import get_versions
        return get_versions()['version']
    
    @property
    def runtime_settings(self):
        if not hasattr(self, '_runtime_settings'):
            from ecosys3D.runtime import RuntimeSettings
            self._runtime_settings = RuntimeSettings()
        return self._runtime_settings
    
    @property
    def runtime_state(self):
        if not hasattr(self, '_runtime_state'):
            from ecosys3D.runtime import RuntimeState
            self._runtime_state = RuntimeState()
        return self._runtime_state
    
    @property
    def eco_method(self):
        from ecosys3D.decorators import eco_method
        return eco_method
    
    @property
    def ecoSetup(self):
        from ecosys3D.ecosys3D import ecoSetup
        return ecoSetup
    
    @property
    def ecoState(self):
        from ecosys3D.state import ecoState
        return ecoState
    
    @property
    def eco3DLegacy(self):
        from ecosys3D.ecosys3D_legacy import ecosys3DLegacy
        return ecosys3DLegacy

sys.modules[__name__].__class__ = _PublicAPI

del sys
del types
del _PublicAPI
