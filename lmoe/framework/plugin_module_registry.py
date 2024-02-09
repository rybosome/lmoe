def plugin_module(cls):
    """A decorator for plugin modules which should be installed."""
    PluginModuleRegistry.register(cls)
    return cls


class PluginModuleRegistry:
    """A registry of all of the modules which need to be installed by plugins."""

    _module_registry = []

    @classmethod
    def register(cls, *args) -> None:
        """Register one or more modules - does not instantiate or install them."""
        cls._module_registry.extend(args)

    @classmethod
    def modules(cls):
        return cls._module_registry
