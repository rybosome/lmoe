# Introduction

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

lmoe (layered mixture of experts, pronounced "Elmo") is a multimodal CLI assistant with a natural
language interface.

Running on Ollama and various open-weight models, lmoe is a convenient, low-overhead,
low-configuration way to interact with programmable AI models from the command line.

## Lmoe Armadillo

The mascot and avatar for the project is Lmoe Armadillo, a Cyborg [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and do toil.

## Capabilities

lmoe has a natural language interface.

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

### Project Generation

Copying the above advice from `lmoe` on creating a Python Poetry project...

```
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

```
% lmoe --paste "make a project like this for a module called 'alexandria' with 3 sub modules: 'auth', 'util', and 'io'"
mkdir alexandria/
touch alexandria/pyproject.toml
touch alexandria/README.rst
touch alexandria/requirements.in
mkdir alexandria/src/
touch alexandria/src/__init__.py
mkdir alexandria/src/alexandria/
touch alexandria/src/alexandria/__init__.py
mkdir alexandria/src/alexandria/auth/
touch alexandria/src/alexandria/auth/__init__.py
mkdir alexandria/src/alexandria/util/
touch alexandria/src/alexandria/util/__init__.py
mkdir alexandria/src/alexandria/io/
touch alexandria/src/alexandria/io/__init__.py
```

Coming soon: the ability to dry-run this, see the intended commands, then execute it.

## Extension Model

New capabilities can be added to `lmoe` with low overhead. Just implement
`lmoe.api.base_expert.BaseExpert` and add your new expert to the registry in
`lmoe/experts/__init__.py`. See existing experts for examples.

## Commands

`lmoe` supports command-like behavior (i.e. executing actions for and against itself).

All of these are supported using the same extension model available to external developers.

### Refresh

Update local Ollama modelfiles. This should be run any time you add a new expert and modelfile, or
alter a modelfile template.

Note that all queries are examples of receiving the same output.

```
% lmoe refresh
% lmoe update your models
% lmoe refresh the models
% lmoe update models

Deleting existing lmoe_classifier...
Updating lmoe_classifier...
Deleting existing lmoe_code...
Updating lmoe_code...
Deleting existing lmoe_project_initialization...
Updating lmoe_project_initialization...
Deleting existing lmoe_general...
Updating lmoe_general...
```

## Status

Version 0.1.2

This is currently a very basic implementation which primarily supports a general expert, offers no
configuration, has limited automation for environment setup, and does not have persistence.

This is not yet ready for others' use.

### Upcoming features

* error handling
* self-setup of models and ollama context after installation
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
* tests
* programmable interface
