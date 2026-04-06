---
title: Decision Coach AI
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.11.0
app_file: app.py
pinned: false
---
🚀 Decision Coach AI

An RL-inspired decision-making environment that simulates real-world human decision processes using structured reasoning, reward signals, and step-based interaction.

🌐 Live Demo
👉 https://huggingface.co/spaces/Shriyansh56/decision-coach-ai
🧠 Overview & Motivation

Making decisions is a real-world cognitive task involving:

    uncertainty

    trade-offs

    incomplete information

This project models decision-making as an environment, where an agent:

    gathers context

    generates options

    evaluates trade-offs

    produces actionable recommendations

👉 Designed for agent evaluation and optimization, not just answering queries.
🔄 Environment Workflow

User Input → Clarification → Options → Tradeoffs → Final Decision

🧩 OpenEnv Specification

This environment follows the OpenEnv interface:
Core Methods

reset() → returns initial state
step(action) → returns (state, reward, done, info)
state() → returns current state

🧠 Action Space

The agent can perform:

    ask_clarifying_question → Gather missing context

    generate_options → Produce multiple decision paths

    evaluate_tradeoffs → Compare pros/cons

    final_recommendation → Deliver actionable answer

👁️ Observation Space

The environment state includes:

    user_problem → Initial input

    conversation_history → Action trajectory

    collected_info → Clarifications gathered

    options → Generated solutions

    final_answer → Final output

🎯 Tasks & Difficulty Levels

We define 3 tasks with increasing difficulty:
🟢 Easy

    Binary decisions

    Example: study vs relax

    Expected: fast convergence (2–3 steps)

🟡 Medium

    Multi-factor trade-offs

    Example: internship (money vs learning)

    Expected: structured reasoning (3–5 steps)

🔴 Hard

    Ambiguous real-life decisions

    Example: career confusion

    Expected: deeper reasoning + tradeoffs

🧪 Graders & Rewards

Each task includes a deterministic grader:

    Score range: 0.0 – 1.0

    Evaluates:

        completeness

        reasoning quality

        action sequence

💰 Reward Function

Reward is dense (not sparse):
Behavior	Reward
Useful step	+0.1 to +0.3
Progress toward solution	+0.5
Final correct decision	+1.0
Redundant / weak step	penalized

👉 Encourages:

    fewer steps

    meaningful reasoning

    no looping

📊 Baseline Performance

Example run:

[END] success=true steps=5 score=0.75 rewards=0.10,0.10,0.30,0.50,1.00

Metrics:

    Average Score: ~0.7–0.8

    Steps: 4–5

    Behavior: stable convergence

⚙️ Tech Stack

    Python

    Gradio (UI)

    FastAPI (backend logic)

    OpenAI-compatible LLM

    Hugging Face Spaces (deployment)

    Docker

## Project Structure

```
.
├── app.py              # Gradio / Streamlit UI entry point
├── inference.py        # Agent logic (submission file)
├── env/                # Environment definition
├── utils/              # Prompt construction + output parsing
├── evaluation/         # Reward functions + grading logic
├── openenv.yaml        # Task / environment spec config
├── Dockerfile          # Container build definition
└── requirements.txt    # Python dependencies
```

🔐 Environment Variables

Set in HF Secrets:

API_BASE_URL = https://router.huggingface.co/v1
MODEL_NAME = meta-llama/Meta-Llama-3-8B-Instruct
HF_TOKEN = your_token_here

🐳 Docker

docker build -t decision-coach .
docker run -p 7860:7860 decision-coach

🧪 Inference Script

    File: inference.py

    Uses OpenAI client

    Outputs structured logs:

[START]
[STEP]
[END]

👉 Required for evaluation
🎯 Real-World Utility

This environment simulates:

    career decisions

    productivity trade-offs

    life planning

👉 Useful for:

    evaluating LLM agents

    decision-support systems

    RL-style reasoning research

⚡ Creativity & Novelty

    Decision-making as environment (not Q&A)

    Step-based reasoning optimization

    Reward shaping for human-like thinking

    RL-inspired structure without heavy training

🏁 Hackathon Focus

    Real-world problem simulation

    Structured reasoning agent

    Full OpenEnv compliance

    End-to-end deployable system

⚡ Tagline

    An RL-inspired AI that helps you think, not just answer.
