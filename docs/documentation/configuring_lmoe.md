# Configuring lmoe

To get started, create an `lmoe` config file in your `$HOME` directory.

```
% touch "$HOME/.lmoeconfig"
```

## Plugins

The `plugins` entry allows `lmoe` to dynamically load your plugin package at runtime. Multiple
plugin packages can be loaded.

```
plugins = [
    {path = "<path to a directory containing {package_name}>", package_name="<name of your package.>"}
]
```

For example, if I have the following directory structure:

```
/Users/me/lmoe_plugins
|  | /example_plugins
|  |  | __init__.py
|  |  | example_expert_1.py
|  |  | example_expert_2.py
|  | /personal_plugins
|  |  | __init__.py
|  |  | personal_expert_1.py
```

Then I'd have the following `.lmoeconfig`:

```
plugins = [
    {path = "/Users/me/lmoe_plugins", package_name = "example_plugins"},
    {path = "/Users/me/lmoe_plugins", package_name = "personal_plugins"}
]
```

