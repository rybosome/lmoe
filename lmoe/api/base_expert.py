from abc import ABC, abstractmethod

from lmoe.utils.templates import read_template


class BaseExpert(ABC):

    @classmethod
    def model_name(cls):
        return f"lmoe_{cls.name().lower()}" if cls.has_modelfile else None

    @classmethod
    def modelfile_name(cls):
        return f"{cls.name().lower()}.modelfile.txt" if cls.has_modelfile else None

    @classmethod
    @abstractmethod
    def name(cls):
        pass

    @classmethod
    @abstractmethod
    def has_modelfile(cls):
        pass

    def modelfile_contents(self):
        return read_template(self.modelfile_name()) if self.has_modelfile else None

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def examples(self):
        pass
