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
