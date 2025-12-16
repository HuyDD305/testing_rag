from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal


class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str

def analyze_job_description(state):
    print("Analyzing job description...")
    return {"is_suitable": len(state["job_description"]) > 100}

def generate_application(state):
    print("Generating job application...")
    return {"application": "some_fake_application_based_on_description"}

def is_suitable(state) -> Literal["generate_application", "__end__"]:
    if state.get("is_suitable"):
        return "generate_application"
    return "__end__"

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable)
builder.add_edge("generate_application", END)

graph = builder.compile()

res = graph.invoke({"job_description": "This is a sample job description that is definitely longer than 100 characters to test the suitability analysis."})
print(res)