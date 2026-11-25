from langgraph.graph import StateGraph , START , END
from langchain_openai import ChatOpenAI
from typing import TypedDict
import dotenv


dotenv.load_dotenv()

llm = ChatOpenAI()

class LLMState(TypedDict):
    question: str
    answer: str

def llm_qa(state: LLMState) -> LLMState:
    # extract the question from the state
    question = state["question"]

    # Form A Prompt
    prompt = f"Answer the following question: {question}"

    # Ask the question to the LLM
    answer = llm.invoke(prompt).content

    # update the state with the answer
    state["answer"] = answer

    return state
    

# create our graph
graph = StateGraph(LLMState)
# add node
graph.add_node("llm_qa",llm_qa)
# add edges
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

# compile
workflow = graph.compile()


# initial state
initial_state = {"question": "What is the capital of France?", "answer": ""}

# run the workflow
final_state = workflow.invoke(initial_state)

print(final_state["answer"])





