# lmoe

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

## Table of Contents

* [**__Overview__**](#overview)
* [**__Setup__**](#setup)
* [**__Basics__**](#basics)
* [**__Capabilities__**](#capabilities)
* [**__Documentation__**](#documentation)
* [**__Status__**](#status)
* [**__Lmoe Armadillo__**](#lmoe-armadillo)

## Overview

Open a terminal and talk to `lmoe`(Layered Mixture of Experts, pronounced "Elmo").

`lmoe` is a programmable, multimodal CLI assistant with a natural language interface.

```
% lmoe who was matisse
 Henri Matisse was a French painter, sculptor, and printmaker, known for his influential role in
 modern art. He was born on December 31, 1869, in Le Cateau-Cambrésis, France, and died on
 November 3, 1954. Matisse is recognized for his use of color and his fluid and expressive
 brushstrokes. His works include iconic paintings such as "The Joy of Life" and "Woman with a Hat."
```

Running on [Ollama](https://github.com/ollama/ollama) and various [open-weight models](https://ollama.com/library), `lmoe` is a simple, yet powerful way to
interact with highly configurable AI models from the command line.

`lmoe` [classifies](https://github.com/rybosome/lmoe/blob/main/lmoe/templates/classifier.modelfile.txt) your query to one of its various [experts](https://github.com/rybosome/lmoe/tree/main/lmoe/experts), which are [specializations](https://github.com/rybosome/lmoe/tree/main/lmoe/templates) of Ollama models.

![Current architecture of lmoe](https://rybosome.github.io/lmoe/assets/lmoe-architecture-current.png)

Learn more about `lmoe`'s [architecture](https://rybosome.github.io/lmoe/documentation/architecture.html) and [programming model](https://rybosome.github.io/lmoe/documentation/extending_lmoe.html).

## Setup

### Dependencies

#### Virtual environment

It is recommended to install `lmoe` in a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

I use [this script](https://github.com/rybosome/lmoe/blob/main/docs/scripts/venv.txt) to make them simpler to manage.

```
% venv mkdir lmoe
% venv activate lmoe
(lmoe) % 
```

#### Ollama

Ensure that an [Ollama](https://github.com/ollama/ollama) server is running.

### Installation & Initialization

```
% pip install lmoe
% lmoe --initialize
```

This will download any base Ollama models not present on your machine and create `lmoe`-internal models.

`lmoe` is now ready to use!

## Basics

### Piping context

```
% cat lmoe/main.py | lmoe what does this code do
 This code sets up and runs an instance of `lmoe` (Layered Mixture of Experts), a Python
 application. It imports various modules, including the native experts and plugin experts for
 `lmoe`. The `run()` function is then called to instantiate the app and defer execution to the
 command runner.
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

*Describe the contents of an image*

This is `lmoe`'s first attempt to describe its default avatar.

**Note**: currently this is raw, unparsed JSON output. Edited by hand for readability.

```
% curl -sS 'https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png' |
base64 -i - |
lmoe what is in this picture
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

## Documentation

* [Architecture](https://rybosome.github.io/lmoe/documentation/architecture.html)
* [Programming model](https://rybosome.github.io/lmoe/documentation/extending_lmoe.html)
* [Roadmap](https://rybosome.github.io/lmoe/documentation/roadmap.html)
* [Utilities](https://rybosome.github.io/lmoe/documentation/utilities.html)

## Status

**Version 0.3.13**

Supports the following core experts:

 * general
 * image recognition
 * project initialization
 * code

Tuning of each is needed.

This is currently a very basic implementation, but may be useful to others.

The extension model is working, but is not guaranteed to be a stable API.


## Lmoe Armadillo

The avatar of `lmoe` is Lmoe Armadillo, a cybernetic [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and execute toil.

Lmoe Armadillo is a curious critter who assumes many different manifestations.

![Lmoe's default avatar against a lit background](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt4-380px.jpg)
![An alternative Lmoe with a cute face](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt1-380px.jpg)
![A blue-nosed Lmoe Armadillo](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt3-380px.jpg)
![A realistic Lmoe Armadillo against a surrealist backdrop](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt2-380px.jpg)
