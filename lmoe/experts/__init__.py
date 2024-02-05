from lmoe.experts.classifier import Classifier
from lmoe.experts.code import Code
from lmoe.experts.refresh import Refresh
from lmoe.experts.project_initialization import ProjectInitialization
from lmoe.experts.general import General
from lmoe.framework.expert_registry import register_experts


register_experts(
    Classifier(),
    Code(),
    Refresh(),
    ProjectInitialization(),
    General(),
)
