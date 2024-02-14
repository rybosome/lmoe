# Roadmap

This is an overview of the work planned for `lmoe`. It is not ranked, and does not necessarily
reflect the order in which the work will be executed.

## Project improvements

Work which is necessary to make the project successful and reach a minimum level of stability
which is appropriate for publicly released software.

* error handling
* logging
* performance measurement
* configurability
* unit tests
* agent testing
* dev pypi branch
* release testing

## Upcoming features

* persisted context (i.e. memory, chat-like experience without a formal chat interface)
* further tuning of classification, code generation, and project initialization
* dry-run for mutating actions, ability to execute mutating actions
* RAG agent
* many more commands
  * filesystem interaction
    * finding file contents from various queries (specific file path, fuzzy description, "this directory", etc.)
  * executors for existing bash commands
    * awk
    * curl
  * API clients
    * weather
    * wikipedia
* openAI API integration

## Long-term architecture

See [future architecture plans](https://rybosome.github.io/lmoe/documentation/architecture.html#future-architectures).
