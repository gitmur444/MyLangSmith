from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    """Run a minimal chain that greets the user."""
    prompt = PromptTemplate(template="Say hi to {name}", input_variables=["name"])
    llm = OpenAI(temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run(name="world")
    print(result)


if __name__ == "__main__":
    main()
