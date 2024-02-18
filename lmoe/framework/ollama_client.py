from dataclasses import asdict, dataclass
from injector import inject
from lmoe.api.model import Model
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.lmoe_logger import LogFactory
from typing import Iterator, Optional, Union

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


class OllamaClient:

    @inject
    def __init__(self, log_factory: LogFactory):
        self._logger = log_factory.logger(__name__)
        self._model_call_reports = []

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
                    context=chunk["context"],
                    total_duration=chunk["total_duration"],
                    load_duration=chunk["load_duration"],
                    prompt_eval_count=chunk["prompt_eval_count"],
                    prompt_eval_duration=chunk["prompt_eval_duration"],
                    eval_count=chunk["eval_count"],
                    eval_duration=chunk["eval_duration"],
                )
                self._logger.debug(latest_call_report.diagnostic_info())
                self._model_call_reports.append(latest_call_report)
