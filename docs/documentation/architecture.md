# lmoe architecture

`lmoe` is a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of
intelligent agents.

Nodes may be one of three types:

*  **Classifier** - Determines how to route a query to a sub-expert
*  **Action** - Generates a response from a model, or takes some other action
*  **Library** - Uses an underlying model to interpret intent, or generate part of a response

![Legend for an lmoe architecture diagram](https://rybosome.github.io/lmoe/assets/lmoe-architecture-legend.png)

### Current architecture

`lmoe` is currently very basic. A small classifier routes between a few top-level nodes. Additional nodes not pictured:

 * Code: Generates code. Needs to be tuned and hooked to a different code model.
 * Nodes for operational commands like refreshing and listing models

![Current architecture of lmoe](https://rybosome.github.io/lmoe/assets/lmoe-architecture-current.png)

### Future architectures

#### Multi-level classification

For now, there is only one classifier at the root. In the future, `lmoe` will support trees of
classification.

![Multi level classification](https://rybosome.github.io/lmoe/assets/lmoe-architecture-future.png)

Early testing suggests that single, large classification prompting with lots of examples scales
poorly, but nested levels with small classifiers may scale better.

#### Library agents

More advanced functionality can be enabled with library agents which rely on an underlying model to
deliver part of a response.

![Library dependencies](https://rybosome.github.io/lmoe/assets/lmoe-architecture-future-with-deps.png)

For instance, understanding filesystem intent - `"/Users/me/Documents/document.text"`,
`"this directory"`, `"somewhere in my downloads folder"` - and reading the data can be an
intermediate task which allows other agents to function better.

This would allow simpler usage of, for instance, the image recognition agent. Instead of having to
base64 the contents of an image ourselves, we could do:

```
### THIS IS AN EXAMPLE, NOT A REAL INTERACTION ###
% lmoe what is in the pic at /Users/me/Pictures/picture.png
There is a black and tan dog looking up at the camera with a cute expression on its face. The
background is a colorful blend of autumn leaves.
```

