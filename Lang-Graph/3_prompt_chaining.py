# prompt chaining: 
# what is prompt chaining:
# Prompt chaining is the process of linking multiple prompts together in a sequence to achieve a more complex task. In this example,
# we first generate an outline and then generate content based on that outline.

# Below Work Flow is Sequential 

from langgraph.graph import StateGraph , START , END
from langchain_openai import ChatOpenAI
from typing import TypedDict
import dotenv

dotenv.load_dotenv()

model = ChatOpenAI()


class BlogState(TypedDict):
    topic: str
    outline: str
    Content: str



def generate_outline(state: BlogState) -> BlogState:

    topic = state["topic"]

    prompt = f"Create an outline for a blog post about: {topic}"

    outline = model.invoke(prompt).content

    state["outline"] = outline

    return state


def generate_content(state: BlogState) -> BlogState:

    topic = state["topic"]
    outline = state["outline"]

    prompt = f"Write a blog post about: {topic} based on the following outline: {outline}"

    content = model.invoke(prompt).content

    state["Content"] = content

    return state



# create our graph
graph = StateGraph(BlogState)
# add nodes
graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_content", generate_content)
# add edges
graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline", "generate_content")
graph.add_edge("generate_content", END)

# compile
workflow = graph.compile()

# initial state
initial_state = {"topic": "The Future of AI", "outline": "", "Content": ""}

# run the workflow
final_state = workflow.invoke(initial_state)

print(final_state["Content"])