from langgraph.graph import StateGraph , START , END
from typing import TypedDict



class BMIState(TypedDict):
    height: float
    weight: float
    bmi: float
    category: str



def calculate_bmi(state: BMIState) -> BMIState:
    height = state["height"]
    weight = state["weight"]
    bmi = round(weight / (height ** 2), 2)

    state["bmi"] = bmi

    return state

def categorize_bmi(state: BMIState) -> BMIState:
    bmi = state["bmi"]
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"
    state["category"] = category
    return state


# define graph

graph = StateGraph(BMIState)


# add Nodes to the graph
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("categorize_bmi", categorize_bmi)

# add edges to the graph
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "categorize_bmi")
graph.add_edge("categorize_bmi", END)

# compile the graph
workflow = graph.compile()

# Execute the graph
initial_state = BMIState(height=1.75, weight=70, bmi=0, category="")
final_state = workflow.invoke(initial_state)
print(final_state)
    