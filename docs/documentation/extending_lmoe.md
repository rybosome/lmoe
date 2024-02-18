# Extension Model

New capabilities can be added to `lmoe` with low overhead. All capabilities, internal and
user-defined, are implemented with the same programming model.

An `Expert` is implemented and registered with the root classifier, and can respond to user queries
programmatically, through a model, or with a mix of both.

These examples assume the following [configuration](https://rybosome.github.io/lmoe/documentation/configuring_lmoe.html):

```
plugins = [
    {path = "/Users/me/docs/examples", package_name = "lmoe_plugins"}
]
```

## All samples

See the [examples](https://github.com/rybosome/lmoe/tree/main/docs/examples/lmoe_plugins) directory.

Here are some to get started.

## Adding a new expert with a model

Let's add an expert which describes the weather in a random city.

First, create a modelfile: `random_weather.modelfile.txt`

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

Then, let's create an API class to handle fetching random weather JSON like this, `random_weather_api.py`.

```
import json
import random
import requests

from dataclasses import asdict, dataclass
from enum import Enum


def clean_dict(d, keys_to_keep):
    """Returns the dict passed in, with only the keys in keys_to_keep.

    Useful for instantiating dataclasses from JSON objects via kwargs, where the JSON objects may
    have properties not part of the dataclass.
    """
    return {key: value for key, value in d.items() if key in keys_to_keep}


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
            name=json["city"], **clean_dict(json, ["country", "latitude", "longitude"])
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
        return json.dumps(asdict(self))

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
            weather_description=WMOInterpretationCode.describe(
                response["weather_code"]
            ),
            **clean_dict(
                response,
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "cloud_cover",
                    "wind_speed_10m",
                    "rain",
                    "showers",
                    "snowfall",
                ],
            )
        )

    @classmethod
    def random(cls) -> "WeatherReport":
        city = City.random()
        return cls.current(city)
```

Finally, an expert class to generate this JSON object and pass it to the summarizer at `lmoe_plugins/random_weather.py`.

```python
import os

from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model import Model
from lmoe.api.model_expert import ModelExpert
from lmoe.framework.expert_registry import expert
from lmoe.framework.ollama_client import OllamaClient
from lmoe_plugins.random_weather_api import WeatherReport


class RandomWeatherModel(Model):
    """A model instructed to summarize JSON blobs about weather in natural language."""

    def __init__(self):
        super(RandomWeatherModel, self).__init__("RANDOM_WEATHER")

    @classmethod
    def modelfile_name(cls):
        home_dir = os.environ.get("HOME")
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "random_weather.modelfile.txt"
        )

    def modelfile_contents(self):
        with open(self.modelfile_name(), "r") as file:
            return file.read()


@expert
class RandomWeather(ModelExpert):
    """An expert which retrieves a random weather report in JSON and summarizes it."""

    @inject
    def __init__(self, ollama_client: OllamaClient):
        self._ollama_client = ollama_client
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
        weather_report = WeatherReport.random()
        self._ollama_client.stream(model=self.model(), prompt=weather_report.json())
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

## Overriding a native expert

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

Start by creating your new expert under `lmoe_plugins/general_rude.py`, and
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

## Depending on natively provided dependencies

If you'd like to add commands which depend on existing experts or other core elements of the `lmoe`
framework, you can do so.

This relies on the [injector](https://pypi.org/project/injector/) framework.

First, create a new expert under `lmoe_plugins/print_args.py`.

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

Then, create a [Module](https://injector.readthedocs.io/en/latest/api.html#injector.Module) under `lmoe_plugins/lmoe_plugin_module.py`.

```python
from injector import Module, provider, singleton
from lmoe.framework.plugin_module_registry import plugin_module
from example_plugins.print_args import PrintArgs

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

