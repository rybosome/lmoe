_REGISTRY = {}


def register_experts(*args):
    for arg in args:
        _REGISTRY[arg.name()] = arg


def keys():
    return _REGISTRY.keys()


def values():
    return _REGISTRY.values()


def get_all_modelfile_names():
    return [e.modelfile_name() for e in values() if e.has_modelfile()]


def get_registered_names():
    return [name for name in _REGISTRY.keys()]


def get_expert(expert_name):
    return _REGISTRY[expert_name]
