def filter_dict(d, keys_to_keep):
    """Returns the dict passed in, with only the keys in keys_to_keep.

    Useful for instantiating dataclasses from JSON objects via kwargs, where the JSON objects may
    have properties not part of the dataclass.
    """
    return {key: value for key, value in d.items() if key in keys_to_keep}
