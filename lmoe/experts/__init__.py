from lmoe.experts.classifier import Classifier
from lmoe.experts.code import Code
from lmoe.experts.general import General
from lmoe.experts.project_initialization import ProjectInitialization
from lmoe.experts.refresh import Refresh
from lmoe.framework.expert_registry import add

add(Classifier())
add(Code())
add(Refresh())
add(ProjectInitialization())
add(General())
