# Introduction

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

`lmoe` (Layered Mixture of Experts, pronounced "Elmo") is a programmable, multimodal CLI assistant
with a natural language interface.

Running on Ollama and various open-weight models, `lmoe` is a simple, yet powerful way to
interact with highly configurable AI models from the command line.

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

### Sequencing

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

## Capabilities

`lmoe` supports a number of specific functions beyond general LLM querying and instruction.

More coming soon.

### Image Recognition

**Note**: currently this is raw, unparsed JSON output. Edited by hand for clarity in reading.

This is `lmoe`'s first attempt to describe its default [avatar](#lmoe-armadillo).

```
% curl -sS 'https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png' | base64 -i - | lmoe what is in this picture
{
    "model":"llava",
    "created_at":"2024-02-08T07:09:28.827507Z",
    "response":" The image features a stylized, colorful creature that appears to be a combination
                 of different animals. It has the body of a rat, with a prominent tail and ears,
                 which is also typical of rats. The head resembles a cat, with pointy ears and what
                 seems to be cat whiskers. The creature has eyes like those of a cat, and it's
                 wearing a helmet or headgear that looks like an advanced robot with digital
                 readouts on the forehead, giving it a cyberpunk aesthetic. The background is
                 colorful with a rainbow pattern, enhancing the fantastical nature of the creature.
                 This image is likely a piece of digital art designed to showcase imaginative and
                 creative concepts. ",
    "done":true,
    "context":[733,16289,28793,767,349,297,456,5754,733,28748,16289,28793,415,3469,4190,264,341,2951,1332,28725,3181,1007,15287,369,8045,298,347,264,9470,302,1581,8222,28723,661,659,272,2187,302,264,6172,28725,395,264,15574,8675,304,12446,28725,690,349,835,10842,302,408,1449,28723,415,1335,312,5650,867,264,5255,28725,395,1305,28724,12446,304,767,3969,298,347,5255,26898,404,28723,415,15287,659,2282,737,1395,302,264,5255,28725,304,378,28742,28713,8192,264,26371,442,1335,490,283,369,4674,737,396,10023,18401,395,7153,1220,8508,356,272,18522,28725,5239,378,264,23449,28720,2060,27974,28723,415,5414,349,3181,1007,395,264,7296,11809,5340,28725,8050,7161,272,7399,529,745,4735,302,272,15287,28723,851,3469,349,3917,264,5511,302,7153,1524,5682,298,1347,2210,26671,1197,304,9811,16582,28723,28705],"total_duration":7148311208,"load_duration":2687336958,
    "prompt_eval_count":1,
    "prompt_eval_duration":1313448000,
    "eval_count":151,
    "eval_duration":3111945000}
```

### Project Generation

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

### Utilities

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

## Extension Model

New capabilities can be added to `lmoe` with low overhead. All capabilities, internal and
user-defined, are implemented with the same programming model.

Just implement [lmoe.api.base_expert.BaseExpert](https://github.com/rybosome/lmoe/blob/main/lmoe/api/base_expert.py) and add your new expert to the registry in
`lmoe/experts/__init__.py`. See existing experts for examples.

More to come as API finalizes - moving to dependency injection in the next update.

## Status

Version 0.2.0

This is currently a very basic implementation.

Supports a general expert and image recognition.

Not configurable, limited automation for environment setup, and does not have persistence.

This is not yet ready for others' use.

### Upcoming features

* dependency injection
* error handling
* self-setup of models and ollama context after installation
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
* tests
* further tuning of classification, code generation, and project initialization
* dry-run for mutating actions, ability to execute mutating actions
* many more commands
  * filesystem interaction
    * finding file contents from various queries (specific file path, fuzzy description, "this directory", etc.)
  * executors for existing bash commands
    * awk
    * curl
  * API clients
    * weather
    * wikipedia

<a id="lmoe-armadillo">

## Lmoe Armadillo

The avatar of `lmoe` is Lmoe Armadillo, a cybernetic [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and execute toil.

Lmoe Armadillo is a curious critter who assumes many different manifestations.

![Lmoe's default avatar against a lit background](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt4-400px.jpg)
![An alternative Lmoe with a cute face](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt1-400px.jpg)
![A blue-nosed Lmoe Armadillo](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt3-400px.jpg)
![A realistic Lmoe Armadillo against a surrealist backdrop](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt2-400px.jpg)
