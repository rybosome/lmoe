# Utilities

Capabilities with multiple inputs listed are examples of different ways to activate it.

## Refresh

*Update local Ollama modelfiles.*

This should be run any time you add a new expert, modelfile, or
alter a modelfile template.

```
% lmoe refresh
% lmoe update your models
% lmoe refresh the models
% lmoe update models

Deleting existing lmoe_classifier...
Updating lmoe_classifier...
Deleting existing lmoe_code...
Updating lmoe_code...
Deleting existing lmoe_project_initialization...
Updating lmoe_project_initialization...
Deleting existing lmoe_general...
Updating lmoe_general...
```

## Model Listing

*List Ollama metadata on models used internally by `lmoe`.*

```
% lmoe list
% lmoe what are your models
% lmoe list your models

{'name': 'lmoe_classifier:latest', 'model': 'lmoe_classifier:latest', 'modified_at': '2024-02-05T13:46:49.983916538-08:00', 'size': 4109868691, 'digest': '576c04e5f9c9e82b2ca14cfd5754ca56610619cddb737a6ca968d064c86bcb68', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_code:latest', 'model': 'lmoe_code:latest', 'modified_at': '2024-02-05T13:46:49.988112317-08:00', 'size': 4109866128, 'digest': 'f387ef329bc0ebd9df25dcc8c4f014bbbe127e6a543c8dfa992a805d71fbbb1e', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_general:latest', 'model': 'lmoe_general:latest', 'modified_at': '2024-02-05T13:46:49.996594585-08:00', 'size': 4109867476, 'digest': '657788601d06890ac136d61bdecec9e3a8ebff4e9139c5cc0fbfa56377625d25', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
{'name': 'lmoe_project_initialization:latest', 'model': 'lmoe_project_initialization:latest', 'modified_at': '2024-02-05T13:46:49.991328433-08:00', 'size': 4109868075, 'digest': '9af2d395e8883910952bee2668d18131206fb5c612bc5d4a207b6637e1bc6907', 'details': {'parent_model': '', 'format': 'gguf', 'family': 'llama', 'families': ['llama'], 'parameter_size': '7B', 'quantization_level': 'Q4_0'}}
```

