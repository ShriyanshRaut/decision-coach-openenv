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
def gradio_interface(user_input):
    result = run_inference(user_input)

    steps = []
    for step in result["conversation_history"]:
        step_type = step["type"].replace("_", " ").title()
        step_content = step["content"]
        steps.append(f"### {step_type}\n{step_content}")

    final = result["final_answer"]
    scores = result["scores"]

    formatted_steps = "\n\n".join(steps)

    score_block = f"""
---
## 📊 Evaluation Scores

- 🧠 Final Score: **{scores['final_score']}**
- ⚙️ Rule Score: **{scores['rule_score']}**
- 🤖 LLM Judge Score: **{scores['llm_score']}**
"""

    return f"""
## 🧠 Decision Process

{formatted_steps}

---

## ✅ Final Recommendation
{final}

{score_block}
"""

gradio_app = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(
    label="Enter your problem",
    placeholder="e.g., I am confused about my career path..." ),
    outputs=gr.Markdown(),  # ✅ FIXED
    title="🧠 Decision Coach AI",
    description="Get step-by-step decision help"
)
# ---------------- COMBINE ---------------- #
# Mount Gradio inside FastAPI
app = gr.mount_gradio_app(app, gradio_app, path="/ui")