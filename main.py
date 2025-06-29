import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langsmith import Client


def main():
    """Run a minimal chain and log the run to LangSmith."""
    client = Client()
    prompt = PromptTemplate(template="Say hi to {name}", input_variables=["name"])
    llm = OpenAI(temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)

    with client.start_trace(run_type="chain") as run:
        result = chain.run(name="world")
        print(result)
    print("Trace URL:", run.url)


if __name__ == "__main__":
    main()
