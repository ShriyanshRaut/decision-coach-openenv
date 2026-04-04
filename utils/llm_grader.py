import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"


def llm_grade(state):
    """
    Uses a HuggingFace LLM to evaluate reasoning quality.
    Returns score between 0 and 1.
    """

    # 🔹 Prepare readable steps
    steps_text = ""
    for step in state.get("conversation_history", []):
        steps_text += f"{step['type']}: {step['content']}\n"

    final_answer = state.get("final_answer", "")

    # 🔥 evaluation prompt
    prompt = f"""
You are a strict evaluator for an AI decision-making system.

Your job is to judge the QUALITY of reasoning.

User Problem:
{state.get("user_problem", "")}

Steps:
{steps_text}

Final Answer:
{final_answer}

Score from 0 to 1.

IMPORTANT:
- Return ONLY a number
- No explanation
"""

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # 🔥 HANDLE ALL HF RESPONSE FORMATS
        if "choices" in result:
            text = result["choices"][0]["message"]["content"]
        elif "generated_text" in result:
            text = result["generated_text"]
        elif isinstance(result, list):
            text = result[0].get("generated_text", "0.5")
        else:
            print("Unknown HF response:", result)
            return 0.5

        # 🔥 SAFE PARSE
        try:
            score = float(text.strip().split()[0])
        except:
            score = 0.5

        # clamp
        score = max(0.0, min(score, 1.0))

        return score

    except Exception as e:
        print("LLM grading error:", e)
        return 0.5