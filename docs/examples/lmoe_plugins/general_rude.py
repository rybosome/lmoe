from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.general import General
from lmoe.framework.expert_registry import expert


class GeneralRude(General):

    @classmethod
    def has_modelfile(cls):
        return False

    def generate(self, lmoe_query: LmoeQuery):
        print("I'm not going to dignify that with a response.")
