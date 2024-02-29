import pytest

from lmoe.experts.classifier import Classifier
from tests.util.real_injector import real_injector


@pytest.fixture
def test_classifier(real_injector):
    yield real_injector.get(Classifier)


class TestClassification:

    def test_general(self, test_classifier: Classifier):
        assert "GENERAL" == test_classifier.classify("What is the ionosphere")

    def test_random_weather_plugin(self, test_classifier: Classifier):
        assert "RANDOM_WEATHER" == test_classifier.classify("random weather")
