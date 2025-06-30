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

Execute `main.py` to run a simple `LLMChain` that greets the user.

```bash
python main.py
```

## FIPA ACL Demo

The repository also includes a minimal skeleton that demonstrates how multiple agents
can communicate using the FIPA ACL protocol. Run `fipa_demo.py` to see two agents
exchange `request` and `inform` messages via a simple in-memory message bus.

```bash
python fipa_demo.py
```

