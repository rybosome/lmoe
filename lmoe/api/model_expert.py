from lmoe.api.base_expert import BaseExpert
from lmoe.api.model import Model
from lmoe.api.lmoe_query import LmoeQuery
from typing import Optional

import ollama


class ModelExpert(BaseExpert):
    """A basic expert which is backed by a model with the same name as the expert."""

    def __init__(self, model: Optional[Model] = None):
        if model is None:
            self._model = Model(self.name())
        else:
            self._model = model

    @classmethod
    def has_model(cls):
        return True

    def model(self) -> Model:
        """ "The underlying model, if this is model-backed."""
        return self._model
