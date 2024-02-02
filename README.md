# lmoe

lmoe (pronounced "Elmo") is a multimodal CLI assistant which interacts with natural language. It is a local Mixture of Experts (MoE), hence the name LMoE (or lmoe).

Running on Ollama and various open-weight models, lmoe is intended to be a convenient, low overhead, low configuration way to interact with AI models from the command line.

## Status

Version 0.1.0

This is currently a very basic implementation which only supports a general expert, no configuration, does not automate environment setup, and does not have persistence.

In the words of many a developer, "it runs fine on my machine" but is currently not intended for general use.

### Upcoming features

* pip integration
* self-setup (after installing with pip)
* configurability
* integration with code and image models
* persisted context (i.e. memory, chat-like experience without a formal chat interface)
