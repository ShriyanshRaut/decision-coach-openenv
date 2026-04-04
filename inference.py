from env.environment import DecisionCoachEnv
from utils.prompt_builder import build_prompt
from utils.action_parser import parse_action

from dotenv import load_dotenv
load_dotenv()

import requests
import os
from env.grader import grade

# 🔑 HF TOKEN
HF_TOKEN = os.getenv("HF_TOKEN")

# 🤖 LLM call (HuggingFace)
def call_llm(prompt):
    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "system", "content": "Respond ONLY in strict valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        return result.get("choices", [{}])[0].get("message", {}).get("content", "{}")

    except Exception as e:
        print("LLM error:", e)
        return "{}"  # safe fallback


# ✅ MAIN FUNCTION
def run_inference(user_problem: str):
    env = DecisionCoachEnv()
    state = env.reset()

    # inject user input
    state["user_problem"] = user_problem

    done = False
    max_steps = 5

    while not done and state["step"] < max_steps:

        prompt = build_prompt(state)

        if state["step"] == max_steps - 1:
            action = {
                "type": "final_recommendation",
                "content": "Start by exploring 1–2 concrete options this week, talk to someone in that field, and take a small actionable step."
            }
        else:
            response = call_llm(prompt)
            action = parse_action(response)

        state, reward, done, _ = env.step(action)

    # ✅ scoring
    scores = grade(state)

    return {
        "conversation_history": state["conversation_history"],
        "final_answer": state["final_answer"],
        "scores": scores
    }


# ✅ local test
if __name__ == "__main__":
    test_input = "I am confused about my career path"

    result = run_inference(test_input)

    print("\n--- Conversation ---\n")
    for step in result["conversation_history"]:
        print(f"{step['type']} → {step['content']}")

    print("\n--- Final Answer ---\n")
    print(result["final_answer"])

    print("\n--- Scores ---\n")
    print(result["scores"])