from lmoe.experts.classifier import Classifier
from lmoe.experts.code import Code
from lmoe.experts.image import Image
from lmoe.experts.list_models import ListModels
from lmoe.experts.refresh import Refresh
from lmoe.experts.project_initialization import ProjectInitialization
from lmoe.experts.general import General
from lmoe.framework.expert_registry import register_experts


register_experts(
    Classifier(),
    Code(),
    ListModels(),
    Refresh(),
    ProjectInitialization(),
    Image(),
    General(),
)
