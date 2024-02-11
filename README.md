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

*Describe the contents of an image*

This is `lmoe`'s first attempt to describe its default avatar.

**Note**: currently this is raw, unparsed JSON output. Edited by hand for readability.

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

To get started, create a directory structure like this:

```
% mkdir -p "$HOME/lmoe_plugins/lmoe_plugins"
```

### Adding a new expert

Create a new file under `$HOME/lmoe_plugins/lmoe_plugins/say_hi.py`.

```python
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert


@expert
class SayHi(BaseExpert):

    @classmethod
    def name(cls):
        return "SAY_HI"

    @classmethod
    def has_modelfile(cls):
        return False

    def description(self):
        return "Returns a friendly greeting from lmoe."

    def example_queries(self):
        return [
            "say hello",
            "introduce yourself",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        print("Hello from a plugin!")
```

Refresh `lmoe` and try your new command out!

```
% lmoe refresh
...
% lmoe say hi
Hello from a plugin!
```

### Adding a new expert with a model

Experts with models can have much more intelligent capabilities. Let's add one which describes the weather in a random city.

First, let's create a modelfile under `$HOME/lmoe_plugins/lmoe_plugins/random_weather.modelfile.txt`.

```
FROM mistral
SYSTEM """
Your job is to summarize a JSON object which has information about the current weather in a given city. You are to give a natural language description of the weather conditions.

Here are the keys of the JSON object.

'temperature_2m': The temperature in farenheit
'relative_humidity_2m': The relative humidity percentage
'cloud_cover': The percentage of cloud coverage
'wind_speed_10m': The wind speed in miles per hour
'rain': Rainfall in millimeters
'showers': Showers in millimeters
'snowfall': Snowfall in millimeters
'city': The city
'country': The country
'description': A short description of the weather conditions

I'll share some examples.

Example 1)

user: {'temperature_2m': 90.1, 'relative_humidity_2m': 64, 'cloud_cover': 46, 'wind_speed_10m': 12.4, 'rain': 0.0, 'showers': 0.0, 'snowfall': 0.0, 'city': 'Chigorodó', 'country': 'Colombia', 'description': 'Partly cloudy'}
agent: It is currently 90 degrees and partly cloudy in Chigorodó, Colombia, with no recent precipitation.

Example 2)
user: {'temperature_2m': 74.0, 'relative_humidity_2m': 79, 'cloud_cover': 42, 'wind_speed_10m': 4.1, 'rain': 0.0, 'showers': 0.0, 'snowfall': 0.0, 'city': 'Boa Esperança', 'country': 'Brazil', 'description': 'Mainly clear'}
agent: The weather in Boa Esperança, Brazil is mainly clear. It is 74 degrees, with winds around 4 miles per hour.

Example 3)
user: {'temperature_2m': 65.2, 'relative_humidity_2m': 50, 'cloud_cover': 67, 'wind_speed_10m': 4.9, 'rain': 0.0, 'showers': 0.0, 'snowfall': 0.0, 'city': 'Sánchez Carrión Province', 'country': 'Peru', 'description': 'Partly cloudy'}
agent: It is a partly cloudy day in Sánchez Carrión Province, Peru, with 67% cloud coverage. It is currently 65 degrees, with winds around 5 miles per hour.

Example 4)
user: {'temperature_2m': 75.1, 'relative_humidity_2m': 71, 'cloud_cover': 83, 'wind_speed_10m': 6.2, 'rain': 0.0, 'showers': 0.0, 'snowfall': 0.0, 'city': 'Ribeirão das Neves', 'country': 'Brazil', 'description': 'Overcast'}
agent: Ribeirão das Neves, Brazil is currently 75 degrees and overcast. There has been no recent precipitation.
"""
```

Then, let's create an expert class to generate this JSON object and pass it to the summarizer at `$HOME/lmoe_plugins/lmoe_plugins/random_weather.py`.

```python
import ollama
import os
import random
import requests


from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert


_RANDOM_CITY_URL_TEMPLATE = "http://geodb-free-service.wirefreethought.com/v1/geo/cities?limit=1&offset={0}&hateoasMode=off"

_MAX_RANDOM_CITY_INDEX = 28177

_WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

_WMO_INTERPRETATION_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorms",
    96: "Thunderstorms with slight hail",
    99: "Thunderstorms with heavy hail",
}


def get_random_city():
    random_number = random.randint(1, _MAX_RANDOM_CITY_INDEX)
    r = requests.get(_RANDOM_CITY_URL_TEMPLATE.format(random_number))
    return r.json()["data"][0]


def get_weather_json(city_json):
    r = requests.get(
        _WEATHER_API_URL,
        params={
            "latitude": city_json["latitude"],
            "longitude": city_json["longitude"],
            "current": "temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m,rain,showers,snowfall,weather_code",
            "temperature_unit": "fahrenheit",
        },
    )
    return r.json()["current"]


@expert
class RandomWeather(BaseExpert):

    @classmethod
    def name(cls):
        return "RANDOM_WEATHER"

    @classmethod
    def has_modelfile(cls):
        return True

    @classmethod
    def modelfile_name(cls):
        home_dir = os.environ.get('HOME')
        return f"{home_dir}/lmoe_plugins/lmoe_plugins/random_weather.modelfile.txt"

    def modelfile_contents(self):
        with open(self.modelfile_name(), "r") as file:
            return file.read()

    def description(self):
        return "Describes the weather in a random city."

    def example_queries(self):
        return [
            "tell me the weather in a random city",
            "random weather",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        city_json = get_random_city()
        weather_json = get_weather_json(city_json)
        weather_json["city"] = city_json["city"]
        weather_json["country"] = city_json["country"]
        weather_code = weather_json["weather_code"]
        weather_json["description"] = (
            _WMO_INTERPRETATION_CODES[weather_code]
            if weather_code in _WMO_INTERPRETATION_CODES
            else ""
        )
        del weather_json["weather_code"]
        del weather_json["time"]
        del weather_json["interval"]
        stream = ollama.generate(
            model="lmoe_random_weather",
            prompt=str(weather_json),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
```

Refresh, and try out your new capability.

```
% lmoe refresh
...

% lmoe random weather
It is currently a chilly 19 degrees in Konkovo District, Russia, with overcast conditions and high
relative humidity of 90%. Winds are blowing around 9.2 miles per hour.

% lmoe random weather
In Arbon District, Switzerland, the weather is currently overcast with a temperature of 43.5
degrees Fahrenheit and a relative humidity of 75%. The winds are blowing at a speed of 7.4 miles
per hour. There has been no recent precipitation reported.
```

### Overriding a native expert

Let's override the `GENERAL` expert with a less helpful variant.

```
% lmoe --classify why is the sky blue
GENERAL
% lmoe why is the sky blue
The scattering of sunlight in the atmosphere causes the sky to appear blue. This occurs because
shorter wavelengths of light, such as blue and violet, are more likely to be scattered than longer
wavelengths, like red or orange. As a result, the sky predominantly reflects and scatters blue
light, making it appear blue during a clear day.
```

Start by creating your new expert under `$HOME/lmoe_plugins/lmoe_plugins/general_rude.py`, and
inherit from the base expert you wish to override.

```python
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.general import General
from lmoe.framework.expert_registry import expert


@expert
class GeneralRude(General):

    @classmethod
    def has_modelfile(cls):
        return False

    def generate(self, lmoe_query: LmoeQuery):
        print("I'm not going to dignify that with a response.")
```

Refresh `lmoe` and try it out!

```
% lmoe refresh
...
% lmoe --classify why is the sky blue
GENERAL
% lmoe why is the sky blue
I'm not going to dignify that with a response.
```

### Depending on natively provided dependencies

If you'd like to add commands which depend on existing experts or other core elements of the `lmoe`
framework, you can do so.

This relies on the [injector](https://pypi.org/project/injector/) framework.

First, create a new expert under `$HOME/lmoe_plugins/lmoe_plugins/print_args.py`.

```python
from injector import inject
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert

import argparse


@expert
class PrintArgs(BaseExpert):

    def __init__(self, parsed_args: argparse.Namespace):
        self.parsed_args = parsed_args

    @classmethod
    def name(cls):
        return "PRINT_ARGS"

    @classmethod
    def has_modelfile(cls):
        return False

    def description(self):
        return "Prints the commandline arguments that were used to invoke lmoe."

    def example_queries(self):
        return [
            "print args",
            "print the commandline args",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        print("These are the arguments that were passed to me:")
        print(self.parsed_args)
```

Then, create a [Module](https://injector.readthedocs.io/en/latest/api.html#injector.Module) under `$HOME/lmoe_plugins/lmoe_plugins/lmoe_plugin_module.py`.

```python
from injector import Module, provider, singleton
from lmoe.framework.plugin_module_registry import plugin_module
from lmoe_plugins.print_args import PrintArgs

import argparse


@plugin_module
class LmoePluginModule(Module):

    @singleton
    @provider
    def provide_print_args(self, parsed_args: argparse.Namespace) -> PrintArgs:
        return PrintArgs(parsed_args)
```

Refresh `lmoe` and try your new capability.

```
% lmoe refresh
...
% lmoe print args
These are the arguments that were passed to me:
Namespace(query=['print', 'args'], paste=False, classify=False, classifier_modelfile=False, refresh=False)
```

## Status

Version 0.3.6

Supports a general expert and image recognition. Limited automation for environment setup, no
persistence.

This is currently a very basic implementation, but may be useful to others.

The extension model is working, but is not guaranteed to be a stable API.

### Upcoming features

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

## Lmoe Armadillo

The avatar of `lmoe` is Lmoe Armadillo, a cybernetic [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and execute toil.

Lmoe Armadillo is a curious critter who assumes many different manifestations.

![Lmoe's default avatar against a lit background](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt4-380px.jpg)
![An alternative Lmoe with a cute face](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt1-380px.jpg)
![A blue-nosed Lmoe Armadillo](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt3-380px.jpg)
![A realistic Lmoe Armadillo against a surrealist backdrop](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt2-380px.jpg)
