from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
from inference import run_inference

# ---------------- FASTAPI ---------------- #
app = FastAPI()

class DecisionRequest(BaseModel):
    user_problem: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/decision")
def decision(request: DecisionRequest):
    try:
        result = run_inference(request.user_problem)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------------- GRADIO ---------------- #
def solve(problem):
    result = run_inference(problem)

    steps = ""
    for step in result["state"]["conversation_history"]:
        steps += f"{step['type']}: {step['content']}\n\n"

    final = result["state"].get("final_answer", "")

    return steps, final


demo = gr.Interface(
    fn=solve,
    inputs=gr.Textbox(label="Enter your problem"),
    outputs=[
        gr.Textbox(label="Reasoning Steps"),
        gr.Textbox(label="Final Answer"),
    ],
    title="Decision Coach AI",
)


# ✅ RUN UI (not FastAPI server)
if __name__ == "__main__":
    demo.launch()