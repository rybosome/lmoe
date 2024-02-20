from dataclasses import asdict, dataclass
from injector import inject
from lmoe.api.model import Model
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.lmoe_logger import LogFactory
from lmoe.utils.dict_utils import filter_dict
from typing import Iterator, List, Optional, Union

import logging
import ollama


@dataclass
class ModelCallReport:

    response: str
    context: Optional[Iterator[int]]
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int

    def diagnostic_info(self):
        d = asdict(self)
        del d["response"]
        return d


@dataclass
class OllamaModel:

    @dataclass
    class Details:
        parent_model: str
        format: str
        families: Iterator[str]
        parameter_size: str
        quantization_level: str

    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: Details

    @classmethod
    def from_dict(cls, d) -> "OllamaModel":
        return OllamaModel(
            details=OllamaModel.Details(
                **filter_dict(
                    d["details"],
                    [
                        "parent_model",
                        "format",
                        "families",
                        "parameter_size",
                        "quantization_level",
                    ],
                )
            ),
            **filter_dict(d, ["name", "model", "modified_at", "size", "digest"]),
        )


class OllamaClient:

    @inject
    def __init__(self, log_factory: LogFactory):
        self._logger = log_factory.logger(__name__)
        self._model_call_reports = []

    def installed_models(self) -> List[OllamaModel]:
        """List all installed ollama models."""
        self._logger.debug("Listing ollama models")
        response = ollama.list()
        self._logger.debug(f"{response}")
        return [OllamaModel.from_dict(model_dict) for model_dict in response["models"]]

    def install_ollama_model(self, base_model):
        stream = ollama.pull(base_model, stream=True)
        last_message = ""
        for chunk in stream:
            # dedupe identical messages from stream
            current_message = chunk["status"]
            if current_message != last_message:
                yield current_message
            last_message = current_message

    def stream(self, model: Model, prompt: Union[LmoeQuery, str]) -> None:
        """Stream a response from Ollama and save metadata associated with the call."""
        self._logger.debug(f"Sending message to {model.ollama_name()}")
        stream = ollama.generate(
            model=model.ollama_name(),
            prompt=str(prompt),
            stream=True,
        )
        response = ""
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
                response += chunk["response"]
            if chunk["done"]:
                print("")
                latest_call_report = ModelCallReport(
                    response=response,
                    **filter_dict(
                        chunk,
                        [
                            "context",
                            "total_duration",
                            "load_duration",
                            "prompt_eval_count",
                            "prompt_eval_duration",
                            "eval_count",
                            "eval_duration",
                        ],
                    ),
                )
                self._logger.debug(latest_call_report.diagnostic_info())
                self._model_call_reports.append(latest_call_report)
