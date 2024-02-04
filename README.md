# Introduction

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

lmoe (pronounced "Elmo", a local Mixture of Experts) is a multimodal CLI assistant with a natural
language interface.

Running on Ollama and various open-weight models, lmoe is intended to be a convenient, low-overhead,
low-configuration way to interact with AI models from the command line.

## Lmoe Armadillo

The mascot and avatar for the project is Lmoe Armadillo, a Cyborg [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and do toil.

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
% ls -la | lmoe how big is my zsh history

 The size of your Zsh history file is 16084 bytes.
```

#### Pasting context

Get an error message and copy it to the clipboard, then ask about it.

```
% print -x 'hello'
print: positive integer expected after -x: hello

% lmoe --paste how do I fix this error
 To use the `-x` option with the `print` command in Bash, you need to provide a positional argument that is a file descriptor. Instead, you provided a string 'hello'. Here's how you can correctly use it:

1. Create or have a file with the name 'hello' and make sure it exists in your working directory.
2. Run the following command instead: `print -r -- < hello`. This reads the contents of the file 'hello' as input for print, which displays its output to stdout.
```

### Code Generation

Coming soon.

### Images

Coming soon.

## Status

Version 0.1.1

This is currently a very basic implementation which only supports a general expert, no
configuration, does not automate environment setup, and does not have persistence.

In the words of many a developer, "it runs fine on my machine" but is currently not intended for
others' use.

### Upcoming features

* error handling
* integration with code and image models
* support for command-like interface
* self-setup of models and ollama context after installation
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
* tests
* plugin interface
