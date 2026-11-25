# We make components executable through a standard interface called Runnable, 
# so we can connect multiple components and execute them together as a chain.
# A Runnable is a standard interface that makes components executable 
# and allows us to connect them into a chain that can run as one workflow.
# One small detail: each component can also execute independently. 
# You don't need to connect multiple components to use a Runnable

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence

load_dotenv()

prompt1 = PromptTemplate(
    template='Write a joke about {topic}',
    input_variables=['topic']
)

model = ChatOpenAI()

parser = StrOutputParser()

prompt2 = PromptTemplate(
    template='Explain the following joke - {text}',
    input_variables=['text']
)

chain = RunnableSequence(prompt1, model, parser, prompt2, model, parser)

print(chain.invoke({'topic':'AI'}))



