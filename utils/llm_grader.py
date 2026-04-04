import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "mistralai/Mistral-7B-Instruct"  # you can swap later


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

    # 🔥 STRONG evaluation prompt
    prompt = f"""
You are a strict evaluator for an AI decision-making system.

Your job is to judge the QUALITY of reasoning.

--- INPUT ---

User Problem:
{state.get("user_problem", "")}

Steps:
{steps_text}

Final Answer:
{final_answer}

--- EVALUATION CRITERIA ---

Score from 0 to 1 based on:

1. Problem Understanding  
- Did the agent correctly understand the user's situation?

2. Depth of Clarification  
- Are the questions specific and meaningful (not generic)?

3. Quality of Options  
- Are options realistic, diverse, and relevant?

4. Tradeoff Analysis  
- Does it clearly compare pros/cons?

5. Actionability  
- Is the final recommendation practical and useful?

--- IMPORTANT RULES ---

- Be STRICT (average systems should get ~0.6–0.75)
- Penalize vague, generic, or repetitive responses
- Reward structured, thoughtful reasoning
- DO NOT explain anything

Return ONLY a number between 0 and 1.
A perfect system = 0.95+, average = 0.6–0.75, poor = <0.5
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
        "temperature": 0.2  # keep stable
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        text = result["choices"][0]["message"]["content"].strip()

        # 🔥 SAFETY PARSE (very important)
        score = float(text.split()[0])

        # clamp just in case
        score = max(0.0, min(score, 1.0))

        return score

    except Exception as e:
        print("LLM grading error:", e)
        return 0.5  # fallback