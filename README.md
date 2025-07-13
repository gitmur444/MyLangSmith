# MyLangChain Example

This repository contains a minimal example that demonstrates how to run a simple LangChain chain.

## Requirements

Install dependencies using `pip`:

```bash
pip install langchain openai
```

Alternatively, you can spin up a Codespace and the `.devcontainer` configuration
will install the dependencies automatically. Credentials must still be provided
through environment variables.

Set the following environment variable with your credentials:

- `OPENAI_API_KEY`

## Running the example

Execute `scripts/main.py` to run a simple `LLMChain` that greets the user.

```bash
python scripts/main.py
```

## FIPA ACL Demo

The repository also includes a minimal skeleton that demonstrates how multiple agents
can communicate using the FIPA ACL protocol. Run `fipa_demo.py` to see two agents
exchange `request` and `inform` messages via a simple in-memory message bus.

```bash
python fipa_demo.py
```

## Commander/Executor WebSocket Demo

Two additional agents showcase communication over websockets with LLM-powered
reasoning. The Commander sends human language instructions, while the Executor
converts them to shell commands using OpenAI, runs them, and summarizes the
output back to the Commander.

Run the original WebSocket-based demo with:

```bash
python scripts/commander_executor.py
```

### Direct Bus Version

Agents can also communicate directly via an in-memory bus without websockets.
Run this version with:

```bash
python scripts/direct_commander_executor.py
```

Ensure the `OPENAI_API_KEY` environment variable is set for the agents to call
the OpenAI API.

