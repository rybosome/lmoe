# lmoe

lmoe (pronounced "Elmo", a local Mixture of Experts) is a multimodal CLI assistant with a natural
language interface.

Running on Ollama and various open-weight models, lmoe is intended to be a convenient, low-overhead,
low-configuration way to interact with AI models from the command line.

## Examples

lmoe has a natural language interface and no syntactic overhead or commands to remember.

You will need to quote your strings if you want to use characters that are significant to your shell
(like `?`).

### Querying
```
% lmoe who was matisse

 Henri Matisse was a French painter, sculptor, and printmaker, known for his influential role in
 modern art. He was born on December 31, 1869, in Le Cateau-Cambrésis, France, and died on
 November 3, 1954. Matisse is recognized for his use of color and his fluid and expressive
 brushstrokes. His works include iconic paintings such as "The Joy of Life" and "Woman with a Hat."
```

```
% lmoe what is the recommended layout for a python project with poetry

 With Poetry, a Python packaging and project management tool, a recommended layout for a Python
 project could include the following structure:

 myproject/
 ├── pyproject.toml
 ├── README.rst
 ├── requirements.in
 └── src/
     ├── __init__.py
     └── mypackage/
         ├── __init__.py
         ├── module1.py
         └── module2.py

In this layout, the `myproject/` directory contains the root-level project files. The
`pyproject.toml` file is used for managing dependencies and building your Python package. The
`README.rst` file is optional, but common, to include documentation about your project. The
`requirements.in` file lists the external packages required by your project.

The `src/` directory contains your source code for the project. In this example, there's a package
named `mypackage`, which includes an `__init__.py` file and two modules: `module1.py` and
`module2.py`.

This is just one suggested layout using Poetry. Depending on your specific project requirements and
preferences, the layout might vary. Always refer to the [Poetry documentation](https://python-poetry.org/)
for more detailed information.
```

### Querying your context

#### Piping context

Pipe it information from your computer and ask questions about it.

```
% cat projects/lmoe/lmoe/main.py | lmoe what does this code do

 The provided code defines a Python script named 'lmoe' which includes an argument parser, the
 ability to read context from both STDIN and the clipboard, and a 'classifier' module for
 determining which expert should respond to a query without actually responding. It does not contain
 any functionality for executing queries or providing responses itself. Instead, it sets up the
 infrastructure for interfacing with external experts through their 'generate' methods.
```

```
% print -x 'hello'

print: positive integer expected after -x: hello

% echo 'print: positive integer expected after -x: hello' | lmoe 'why am I getting this error with the `print` shell command?'

 The `print` command in a Unix-like shell expects a positive integer as its argument to print that
 value to the console. You provided the string 'hello' instead, which is causing the error message
 you're seeing.
```

```
% ls -la | lmoe how big is my zsh history

 The size of your Zsh history file is 16084 bytes.
```

#### Pasting context

Let's copy the following code to the clipboard.

```shell
# Define the base directory for virtual environments
VENVS_DIR="$HOME/.venvs"

# Helper for manipulating Python virtual environments
venv() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: venv <command> [args]"
        exit 1
    fi

    command="$1"
    shift

    case "$command" in
        mkdir)
            if [[ $# -lt 1 ]]; then
                echo "Usage: venv mkdir <env_name>"
                exit 1
            fi
            python3 -m venv "$VENVS_DIR/$1"
            ;;
        ls)
            ls "$VENVS_DIR"
            ;;
        rm)
            if [[ $# -lt 1 ]]; then
                echo "Usage: venv rm <env_name>"
                exit 1
            fi
            echo "Do you want to remove $1? (y/n): \c"
            read confirm
            if [[ $confirm == "y" ]]; then
                rm -rf "$VENVS_DIR/$1"
            fi
            ;;
        activate)
            if [ -z "$1" ]; then
            . "$VENVS_DIR/default/bin/activate"
            else
            . "$VENVS_DIR/$1/bin/activate"
            fi
            ;;
        *)
            echo "Unknown command. Available commands: mkdir, ls, rm, activate"
            exit 1
            ;;
    esac
}
```

```
% lmoe --paste what does this zsh script do

 This zsh script defines a function named `venv` that assists in managing Python virtual
 environments. It provides several subcommands: "mkdir" for creating new environments, "ls" for
 listing existing environments, "rm" for removing environments, and "activate" for activating an
 environment. The base directory for all virtual environments is set to `$HOME/.venvs`.
```

### Code Generation

Coming soon.

### Images

Coming soon.

## Status

Version 0.1.01

This is currently a very basic implementation which only supports a general expert, no
configuration, does not automate environment setup, and does not have persistence.

In the words of many a developer, "it runs fine on my machine" but is currently not intended for
others' use.

### Upcoming features

* integration with code and image models
* self-setup (after installing with pip)
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
