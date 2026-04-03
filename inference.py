from env.environment import DecisionCoachEnv
from utils.prompt_builder import build_prompt
from utils.action_parser import parse_action

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os
from env.grader import grade

# 🔑 LLM client
client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# 🤖 LLM call
def call_llm(prompt):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a decision-making agent. Respond ONLY in JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


# ✅ MAIN FUNCTION (IMPORTANT)
def run_inference():
    env = DecisionCoachEnv()
    state = env.reset()

    done = False
    max_steps = 5

    logs = []  # store steps

    while not done and state["step"] < max_steps:

        prompt = build_prompt(state)

        if state["step"] == max_steps - 1:
            action = {
                "type": "final_recommendation",
                "content": "Based on available information, this is the best decision."
            }
            logs.append("[FORCED FINAL STEP]")
        else:
            response = call_llm(prompt)
            logs.append(f"RAW RESPONSE: {response}")

            action = parse_action(response)

        state, reward, done, _ = env.step(action)

        logs.append(f"[STEP {state['step']}] {action['type']} | reward={reward}")

    final_score = grade(state)
    logs.append(f"[FINAL SCORE]: {final_score}")
    logs.append("[END]")

    return {
        "logs": logs,
        "final_score": final_score,
        "final_state": state
    }


# 👇 optional: still allow running directly
if __name__ == "__main__":
    result = run_inference()
    for line in result["logs"]:
        print(line)