from enum import Enum

import re


class ExpertType(Enum):
    GENERAL = "GENERAL"
    CODE = "CODE"
    IMAGE = "IMAGE"

    @staticmethod
    def parse(input_string):
        for enum_value in ExpertType:
            match = re.match(f"^[\s]*{enum_value.name}.*", input_string)
            if match:
                return enum_value
        return ExpertType.GENERAL
