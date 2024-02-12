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
