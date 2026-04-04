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
def run_inference(user_problem: str):
    env = DecisionCoachEnv()
    state = env.reset()

    # ✅ inject user input
    state["user_problem"] = user_problem

    done = False
    max_steps = 5

    while not done and state["step"] < max_steps:

        prompt = build_prompt(state)

        if state["step"] == max_steps - 1:
            action = {
                "type": "final_recommendation",
                "content": "Based on your situation, the best next step is to explore your options while building relevant skills and seeking guidance."
            }
        else:
            response = call_llm(prompt)
            action = parse_action(response)

        state, reward, done, _ = env.step(action)

    # ✅ get full score breakdown (IMPORTANT)
    scores = grade(state)   # now returns dict

    return {
        "conversation_history": state["conversation_history"],
        "final_answer": state["final_answer"],
        "scores": scores   # 🔥 not just final_score
    }


# 👇 optional: still allow running directly
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