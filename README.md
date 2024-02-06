# Introduction

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

`lmoe` (Layered Mixture of Experts, pronounced "Elmo") is a programmable, multimodal CLI assistant
with a natural language interface.

Running on Ollama and various open-weight models, `lmoe` is a simple, yet powerful way to
interact with highly configurable AI models from the command line.

## Lmoe Armadillo

The avatar of `lmoe` is Lmoe Armadillo, a cybernetic [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and execute toil.

## Setup

You may wish to install `lmoe` in a virtual environment.

```
% pip install lmoe
```

Ensure that an Ollama server is running, then manually initialize the root classification model.

```
% lmoe --classifier_modelfile > temp-classifier-modelfile.txt
% ollama create lmoe_classifier -f temp-classifier-modelfile.txt
```

Finally, refresh the rest of the models.

```
% lmoe refresh
```

Further interaction wtih `lmoe` may cause Ollama to pull any models not present on your local machine.

## Overview

### Natural language querying
```
% lmoe who was matisse

 Henri Matisse was a French painter, sculptor, and printmaker, known for his influential role in
 modern art. He was born on December 31, 1869, in Le Cateau-Cambrésis, France, and died on
 November 3, 1954. Matisse is recognized for his use of color and his fluid and expressive
 brushstrokes. His works include iconic paintings such as "The Joy of Life" and "Woman with a Hat."
```

### Piping context

```
% cat projects/lmoe/lmoe/main.py | lmoe what does this code do

 The provided code defines a Python script named 'lmoe' which includes an argument parser, the
 ability to read context from both STDIN and the clipboard, and a 'classifier' module for
 determining which expert should respond to a query without actually responding. It does not contain
 any functionality for executing queries or providing responses itself. Instead, it sets up the
 infrastructure for interfacing with external experts through their 'generate' methods.
```

```
% ls -la $HOME | lmoe how big is my zsh history

 The size of your Zsh history file is 16084 bytes.
```

### Pasting context

```
% print -x 'hello'
print: positive integer expected after -x: hello
```

Copy this to the clipboard, then:

```
% lmoe --paste how do I fix this error
 To use the `-x` option with the `print` command in Bash, you need to provide a positional argument that is a file descriptor. Instead, you provided a string 'hello'. Here's how you can correctly use it:

1. Create or have a file with the name 'hello' and make sure it exists in your working directory.
2. Run the following command instead: `print -r -- < hello`. This reads the contents of the file 'hello' as input for print, which displays its output to stdout.
```

## Capabilities

`lmoe` supports a number of specific functions beyond general LLM querying and instruction. All of
these are implemented using the same extension model available to external developers.

Capabilities with multiple inputs listed are examples of different ways to activate it.

#### Refresh

*Update local Ollama modelfiles.*

This should be run any time you add a new expert, modelfile, or
alter a modelfile template.

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

#### Project Generation

*Generate a new programming project from an ascii or textual description.*

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

Copy this to the clipboard, and then:

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

...for a list of runnable shell commands.

Coming soon: `lmoe` will offer to run them for you, open them in an editor, or stop.

#### Model Listing

*List Ollama metadata on models used internally by `lmoe`.*

```
% lmoe list
% lmoe what are your models
% lmoe list your models

{'name': 'lmoe_classifier:latest', 'model': 'lmoe_classifier:latest', 'modified_at': '2024-02-05T13:46:49.983916538-08:00', 'size': 4109868691, 'digest': '576c04e5f9c9e82b2ca14cfd5754ca56610619cddb737a6ca968d064c86bcb68', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_code:latest', 'model': 'lmoe_code:latest', 'modified_at': '2024-02-05T13:46:49.988112317-08:00', 'size': 4109866128, 'digest': 'f387ef329bc0ebd9df25dcc8c4f014bbbe127e6a543c8dfa992a805d71fbbb1e', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_general:latest', 'model': 'lmoe_general:latest', 'modified_at': '2024-02-05T13:46:49.996594585-08:00', 'size': 4109867476, 'digest': '657788601d06890ac136d61bdecec9e3a8ebff4e9139c5cc0fbfa56377625d25', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_project_initialization:latest', 'model': 'lmoe_project_initialization:latest', 'modified_at': '2024-02-05T13:46:49.991328433-08:00', 'size': 4109868075, 'digest': '9af2d395e8883910952bee2668d18131206fb5c612bc5d4a207b6637e1bc6907', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
```

## Sequencing

`lmoe` can be piped into itself. This allows scriptable composition of primitives into more advanced
functionality.

```
% lmoe what is the recommended layout for a python project with poetry |
lmoe "make a project like this for a module called 'alexandria' with 3 sub modules: 'auth', 'util', and 'io'"

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
 touch alexandria/src/alexandria/util/
 touch alexandria/src/alexandria/util/__init__.py
 touch alexandria/src/alexandria/io/
 touch alexandria/src/alexandria/io/__init__.py
```

## Extension Model

New capabilities can be added to `lmoe` with low overhead. Just implement
`lmoe.api.base_expert.BaseExpert` and add your new expert to the registry in
`lmoe/experts/__init__.py`. See existing experts for examples.

More to come soon as API finalizes.

## Status

Version 0.1.2

This is currently a very basic implementation which mostly supports a general expert, offers no
configuration, has limited automation for environment setup, and does not have persistence.

This is not yet ready for others' use.

### Upcoming features

* error handling
* self-setup of models and ollama context after installation
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
* tests
* stable programmable interface
* further tuning of classification, code generation, and project initialization
* dry-run for mutating actions, ability to execute mutating actions
* many more commands
  * filesystem interaction
    * fuzzy finding
    * pulling out context
  * helpers for existing bash commands
    * awk
    * curl
  * API clients
    * weather
    * wikipedia
