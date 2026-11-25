from langgraph.graph import StateGraph , START , END
from langchain_openai import ChatOpenAI
from typing import TypedDict
import dotenv

dotenv.load_dotenv()

model = ChatOpenAI()

class CricketState(TypedDict):
    run: int
    ball: int
    four: int
    six: int

    strike_rate: float
    bpb: float
    boundry_percentage: float
    summmary: str


def calculate_strike_rate(state: CricketState) -> CricketState:

    strike_rate = (state["run"] / state["ball"]) * 100
    return {"strike_rate": strike_rate} # this is parttial  update to the state which we use while working with parallel workflows

def calculate_bpb(state: CricketState) -> CricketState:

    bpb = state["ball"] / state["run"]
    return {"bpb": bpb} # partial update for parallel workflow

def calculate_boundry_percentage(state: CricketState) -> CricketState:

    boundry_percentage = ((state["four"] * 4 + state["six"] * 6) / state["run"]) * 100
    return {"boundry_percentage": boundry_percentage} # partial update for parallel workflow

def calculate_summary(state: CricketState) -> CricketState:

    summary = f"strike_rate: {state.get('strike_rate', 0)}, bpb: {state.get('bpb', 0)}, boundry_percentage: {state.get('boundry_percentage', 0)}"
    return {"summmary": summary} # partial update for parallel workflow


# Define the state graph for the cricket workflow
graph = StateGraph(CricketState)


# Add nodes for each calculation step in the workflow
graph.add_node("calculate_strike_rate", calculate_strike_rate)
graph.add_node("calculate_bpb", calculate_bpb)
graph.add_node("calculate_boundry_percentage", calculate_boundry_percentage)
graph.add_node("calculate_summary", calculate_summary)


# Add edges to define the workflow sequence
graph.add_edge(START, "calculate_strike_rate")
graph.add_edge(START, "calculate_bpb")
graph.add_edge(START, "calculate_boundry_percentage")
graph.add_edge("calculate_summary", END)

# Add edges from calculation nodes to the summary node
graph.add_edge("calculate_strike_rate", "calculate_summary")
graph.add_edge("calculate_bpb", "calculate_summary")
graph.add_edge("calculate_boundry_percentage", "calculate_summary")


graph.add_edge("calculate_summary", END)

# Compile the workflow into an executable form
workflow = graph.compile()

# Define the initial state for the workflow
initial_state = CricketState(
    run=50,
    ball=30,
    four=4,
    six=2,
    strike_rate=0.0,
    bpb=0.0,
    boundry_percentage=0.0,
    summmary=""
)

# Run the workflow with the initial state and print the result
result = workflow.invoke(initial_state)
print(result)

