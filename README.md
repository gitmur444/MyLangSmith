# MyLangSmith

This repository contains a minimal example that demonstrates how to log LangChain runs to LangSmith.

## Requirements

Install dependencies using `pip`:

```bash
pip install langchain langsmith openai
```

Alternatively, you can use the included `codex.yaml` to configure the
environment automatically. The setup step installs the dependencies from
`requirements.txt`, while credentials must be supplied through environment
variables.

Set the following environment variables with your credentials:

- `OPENAI_API_KEY`
- `LANGCHAIN_API_KEY`

You may also set `LANGCHAIN_ENDPOINT` if you use a self-hosted LangSmith instance.

## Running the example

Execute `main.py` to run a simple `LLMChain` that greets the user. The run is recorded in LangSmith and the resulting trace URL is printed at the end.

```bash
python main.py
```

