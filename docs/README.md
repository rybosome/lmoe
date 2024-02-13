# Introduction

<img src="https://rybosome.github.io/lmoe/assets/lmoe-armadillo.png">

`lmoe` (Layered Mixture of Experts, pronounced "Elmo") is a programmable, multimodal CLI assistant
with a natural language interface.

Running on [Ollama](https://github.com/ollama/ollama) and various [open-weight models](https://ollama.com/library), `lmoe` is a simple, yet powerful way to
interact with highly configurable AI models from the command line.

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

## Overview

`lmoe` is your CLI assistant. It [classifies](https://github.com/rybosome/lmoe/blob/main/lmoe/templates/classifier.modelfile.txt) your query to one of its various [experts](https://github.com/rybosome/lmoe/tree/main/lmoe/experts), which are [specializations](https://github.com/rybosome/lmoe/tree/main/lmoe/templates) of various [open-weight models](https://ollama.com/library).

See [more on the architecture](#architecture) below.

**NOTE**: All examples below are real interactions with `lmoe` except where explicitly noted.

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

## Architecture

`lmoe` is a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of
intelligent agents.

![Legend for an lmoe architecture diagram](https://rybosome.github.io/lmoe/assets/lmoe-architecture-legend.png)

Nodes may be one of three types:

*  **Classifier** - Determines how to route a query to a sub-expert
*  **Action** - Generates a response from a model, or takes some other action
*  **Library** - Uses an underlying model to interpret intent, or generate part of a response

### Current

![Current architecture of lmoe](https://rybosome.github.io/lmoe/assets/lmoe-architecture-current.png)

`lmoe` is currently very basic. A small classifier routes between a few top-level nodes. Additional nodes not pictured:

 * Code: Generates code. Needs to be tuned and hooked to a different code model.
 * Nodes for operational commands like refreshing and listing models

### Future Additions

![Multi level classification](https://rybosome.github.io/lmoe/assets/lmoe-architecture-future.png)

Early testing suggests that single, large classification prompting with lots of examples scales
poorly, but nested levels with small classifiers may scale better. For now, there is only one
classifier at the root. In the future, `lmoe` will support trees of classification.

![Library dependencies](https://rybosome.github.io/lmoe/assets/lmoe-architecture-future-with-deps.png)

More advanced functionality can be enabled with library agents which rely on an underlying model to
deliver part of a response.

For instance, understanding filesystem intent - "/Users/me/Documents/document.text",
"this directory", "somewhere in my downloads folder" - and reading the data can be an intermediate
task which allows other agents to function better.

This would allow simpler usage of, for instance, the image recognition agent. Instead of having to
base64 the contents of an image ourselves, we could do:

```
### THIS IS AN EXAMPLE, NOT A REAL INTERACTION ###
% lmoe what is in the pic at /Users/me/Pictures/picture.png
There is a black and tan dog looking up at the camera with a cute expression on its face. The
background is a colorful blend of autumn leaves.
```

## Extension Model

New capabilities can be added to `lmoe` with low overhead. All capabilities, internal and
user-defined, are implemented with the same programming model.

An `Expert` is implemented and registered with the root classifier, and can respond to user queries
programmatically, through a model, or with a mix of both.

To get started, create a directory structure like this:

```
% mkdir -p "$HOME/lmoe_plugins/lmoe_plugins"
```

### All samples

See the [examples](https://github.com/rybosome/lmoe/main/docs/examples/lmoe_plugins) directory.

Here are some to get started.

### Adding a new expert with a model

Let's add an expert which describes the weather in a random city.

First, create a modelfile under `$HOME/lmoe_plugins/lmoe_plugins/random_weather.modelfile.txt`.

```
FROM mistral
SYSTEM """
Your job is to summarize a JSON object which has information about the current weather in a given
city. You are to give a natural language description of the weather conditions.

Here are the keys of the JSON object.

'temperature_2m': The temperature in farenheit
'relative_humidity_2m': The relative humidity percentage
'cloud_cover': The percentage of cloud coverage
'wind_speed_10m': The wind speed in miles per hour
'rain': Rainfall in millimeters
'showers': Showers in millimeters
'snowfall': Snowfall in millimeters
'name': The name of the city
'country': The name of the country
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
import json
import ollama
import os
import random
import requests

from dataclasses import asdict, dataclass
from enum import Enum
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model import Model
from lmoe.api.model_expert import ModelExpert
from lmoe.api.ollama_client import stream
from lmoe.framework.expert_registry import expert


@dataclass(frozen=True)
class City:
    """Basic information about a city."""

    name: str
    country: str
    latitude: float
    longitude: float

    """URL for a service which returns information on a city at the given index."""
    _RANDOM_CITY_URL_TEMPLATE = "http://geodb-free-service.wirefreethought.com/v1/geo/cities?limit=1&offset={0}&hateoasMode=off"

    """The maximum value returning a city instance for the above service."""
    _MAX_RANDOM_CITY_INDEX = 28177

    @classmethod
    def random(cls) -> "City":
        """Returns information on a random city."""
        random_number = random.randint(1, cls._MAX_RANDOM_CITY_INDEX)
        r = requests.get(cls._RANDOM_CITY_URL_TEMPLATE.format(random_number))
        json = r.json()["data"][0]
        return City(
            name=json["city"],
            country=json["country"],
            latitude=json["latitude"],
            longitude=json["longitude"],
        )


class WMOInterpretationCode(Enum):
    """Partial implementation of World Meteorological Organization codes describing weather conditions.

    https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
    """

    CLEAR_SKY = 0
    MAINLY_CLEAR = 1
    PARTLY_CLOUDY = 2
    OVERCAST = 3
    FOG = 45
    DEPOSITING_RIME_FOG = 48
    LIGHT_DRIZZLE = 51
    MODERATE_DRIZZLE = 53
    DENSE_DRIZZLE = 55
    LIGHT_FREEZING_DRIZZLE = 56
    DENSE_FREEZING_DRIZZLE = 57
    LIGHT_RAIN = 61
    MODERATE_RAIN = 63
    HEAVY_RAIN = 65
    LIGHT_FREEZING_RAIN = 66
    HEAVY_FREEZING_RAIN = 67
    LIGHT_SNOW = 71
    MODERATE_SNOW = 73
    HEAVY_SNOW = 75
    SNOW_GRAINS = 77
    LIGHT_RAIN_SHOWERS = 80
    MODERATE_RAIN_SHOWERS = 81
    HEAVY_RAIN_SHOWERS = 82
    LIGHT_SNOW_SHOWERS = 85
    HEAVY_SNOW_SHOWERS = 86
    THUNDERSTORMS = 95
    THUNDERSTORMS_WITH_SLIGHT_HAIL = 96
    THUNDERSTORMS_WITH_HEAVY_HAIL = 99

    @classmethod
    def describe(cls, code: int) -> str:
        """Gives a title cased description of an int code if it exists, or an empty string."""
        return (
            cls(code).name.replace("_", " ").title() if code in cls.__members__ else ""
        )


@dataclass(frozen=True)
class WeatherReport:
    """A description of weather conditions in a particular moment - (only current supported)."""
    city: City
    temperature_2m: str
    relative_humidity_2m: int
    cloud_cover: int
    wind_speed_10m: float
    rain: float
    showers: float
    snowfall: float
    weather_description: str

    """Base URL of the https://open-meteo.com/ current forecast API."""
    _WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

    def json(self) -> str:
        """Returns a JSON string."""
        partial_dict = asdict(self)
        return json.dumps(partial_dict)

    @classmethod
    def current(cls, city: City) -> "WeatherReport":
        """Current weather conditions for the given city."""
        r = requests.get(
            cls._WEATHER_API_URL,
            params={
                "latitude": city.latitude,
                "longitude": city.longitude,
                "current": "temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m,rain,showers,snowfall,weather_code",
                "temperature_unit": "fahrenheit",
            },
        )
        response = r.json()["current"]
        return WeatherReport(
            city=city,
            temperature_2m=response["temperature_2m"],
            relative_humidity_2m=response["relative_humidity_2m"],
            cloud_cover=response["cloud_cover"],
            wind_speed_10m=response["wind_speed_10m"],
            rain=response["rain"],
            showers=response["showers"],
            snowfall=response["snowfall"],
            weather_description=WMOInterpretationCode.describe(
                response["weather_code"]
            ),
        )

class RandomWeatherModel(Model):
    """A model instructed to summarize JSON blobs about weather in natural language."""

    def __init__(self):
        super(RandomWeatherModel, self).__init__("RANDOM_WEATHER")

    @classmethod
    def modelfile_name(cls):
        home_dir = os.environ.get("HOME")
        return f"{home_dir}/lmoe_plugins/lmoe_plugins/random_weather.modelfile.txt"

    def modelfile_contents(self):
        with open(self.modelfile_name(), "r") as file:
            return file.read()


@expert
class RandomWeather(ModelExpert):
    """An expert which retrieves a random weather report in JSON and summarizes it."""

    def __init__(self):
        super(RandomWeather, self).__init__(RandomWeatherModel())

    @classmethod
    def name(cls):
        return "RANDOM_WEATHER"

    def description(self):
        return "Describes the weather in a random city."

    def example_queries(self):
        return [
            "tell me the weather in a random city",
            "random weather",
            "give me a random weather report",
            "random weather report",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        weather_report = WeatherReport.current(City.random())

        for chunk in stream(model=self.model, prompt=weather_report.json()):
            print(chunk, end="", flush=True)
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
    def has_model(cls):
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
    def has_model(cls):
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

Version 0.3.12

Supports the following core experts:

 * general
 * image recognition
 * project initialization
 * code

Tuning of each is needed.

This is currently a very basic implementation, but may be useful to others.

The extension model is working, but is not guaranteed to be a stable API.

### Upcoming features

* error handling
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* configurability
* tests
* further tuning of classification, code generation, and project initialization
* dry-run for mutating actions, ability to execute mutating actions
* RAG agent
* many more commands
  * filesystem interaction
    * finding file contents from various queries (specific file path, fuzzy description, "this directory", etc.)
  * executors for existing bash commands
    * awk
    * curl
  * API clients
    * weather
    * wikipedia
* openAI API integration

## Lmoe Armadillo

The avatar of `lmoe` is Lmoe Armadillo, a cybernetic [Cingulata](https://en.wikipedia.org/wiki/Cingulata)
who is ready to dig soil and execute toil.

Lmoe Armadillo is a curious critter who assumes many different manifestations.

![Lmoe's default avatar against a lit background](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt4-380px.jpg)
![An alternative Lmoe with a cute face](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt1-380px.jpg)
![A blue-nosed Lmoe Armadillo](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt3-380px.jpg)
![A realistic Lmoe Armadillo against a surrealist backdrop](https://rybosome.github.io/lmoe/assets/lmoe-armadillo-alt2-380px.jpg)
