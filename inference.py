"""
Inference Script Example
===================================
MANDATORY
- Before submitting, ensure the following variables are defined in your environment configuration:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.
    LOCAL_IMAGE_NAME The name of the local image to use for the environment if you are using from_docker_image()
                     method

- Defaults are set only for API_BASE_URL and MODEL_NAME 
    (and should reflect your active inference setup):
    API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-endpoint>")
    MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model>")
    
- The inference script must be named `inference.py` and placed in the root directory of the project
- Participants must use OpenAI Client for all LLM calls using above variables

STDOUT FORMAT
- The script must emit exactly three line types to stdout, in this order:

    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

  Rules:
    - One [START] line at episode begin.
    - One [STEP] line per step, immediately after env.step() returns.
    - One [END] line after env.close(), always emitted (even on exception).
    - reward and rewards are formatted to 2 decimal places.
    - done and success are lowercase booleans: true or false.
    - error is the raw last_action_error string, or null if none.
    - All fields on a single line with no newlines within a line.
    - Each tasks should return score in [0, 1]

  Example:
    [START] task=click-test env=miniwob model=Qwen3-VL-30B
    [STEP] step=1 action=click('123') reward=0.00 done=false error=null
    [STEP] step=2 action=fill('456','text') reward=0.00 done=false error=null
    [STEP] step=3 action=click('789') reward=1.00 done=true error=null
    [END] success=true steps=3 score=1.00 rewards=0.00,0.00,1.00
"""

import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from env.environment import DecisionCoachEnv
from utils.prompt_builder import build_prompt
from utils.action_parser import parse_action
from env.grader import grade

# 🔑 ENV CONFIG
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

TASK_NAME = "decision_task"
BENCHMARK = "decision_coach_env"

MAX_STEPS = 5
TEMPERATURE = 0.3

# 🔥 OpenAI-compatible client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


# ================= LOGGING =================

def log_start(task: str, env: str, model: str):
      print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ================= LLM CALL =================

def call_llm(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Respond ONLY in valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
        )

        return (completion.choices[0].message.content or "").strip()

    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)
        return "{}"

def run_inference(user_problem: str):
    env = DecisionCoachEnv()
    state = env.reset(user_problem)

    done = False

    while not done and state["step"] < MAX_STEPS:
        prompt = build_prompt(state)

        # 🔥 FORCE FINAL STEP (CRITICAL)
        if state["step"] >= 4:
            action = {
                "type": "final_recommendation",
                "content": generate_final_answer(state)
            }
        else:
            response = call_llm(prompt)
            action = parse_action(response)

        state, _, done, _ = env.step(action)

    scores = grade(state)

    return {
        "state": state,
        "scores": scores
    }

# ================= MAIN =================

def main():

    env = DecisionCoachEnv()
    state = env.reset("I am confused about my career")

    rewards = []
    steps_taken = 0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    done = False

    try:
        while not done and state["step"] < MAX_STEPS:

            prompt = build_prompt(state)

            if state["step"] >= 4:
             action = {
        "type": "final_recommendation",
        "content": generate_final_answer(state)
    }
            else:
                response = call_llm(prompt)
                action = parse_action(response)

            state, reward, done, _ = env.step(action)

            rewards.append(reward)
            steps_taken += 1

            log_step(
                step=steps_taken,
                action=str(action),
                reward=reward,
                done=done,
                error=None
            )

        # ✅ scoring
        scores = grade(state)
        score = scores.get("final_score", 0.0)

        success = score >= 0.6

    except Exception as e:
        print(f"[DEBUG] Runtime error: {e}", flush=True)
        success = False
        score = 0.0

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


def generate_final_answer(state):
    options = state.get("options", [])

    if not options:
        return "Based on your situation, choose one direction and take a small step this week to reduce uncertainty."

    # pick first 1–2 options and make it actionable
    selected = options[:2]

    answer = "Based on your situation, here’s a practical way forward:\n\n"

    for i, opt in enumerate(selected, 1):
        answer += f"{i}. {opt}\n"

    answer += "\nStart with one option this week and take a small actionable step to test it."

    return answer

if __name__ == "__main__":
    main()