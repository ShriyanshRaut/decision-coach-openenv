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

An AI-powered system that helps users make better decisions through structured reasoning and actionable recommendations.
🌐 Live Demo

👉 https://huggingface.co/spaces/Shriyansh56/decision-coach-ai
🧠 What It Does

    Breaks down user problems step-by-step

    Asks clarifying questions

    Generates possible options

    Evaluates trade-offs

    Provides a clear final recommendation

🔄 Workflow

User Input → Reasoning Steps → Options → Final Decision

📌 Key Features

    Multi-step decision reasoning

    Context-aware suggestions

    Evaluation scoring system

    Live deployed Gradio interface

    Handles easy, medium, and complex scenarios

⚙️ Tech Stack

    Python

    Gradio (UI)

    FastAPI (Backend)

    OpenAI-compatible LLM

    Hugging Face Spaces (Deployment)

    Docker

🧩 Environment Details

    State:

        user_problem

        conversation_history

        options

        final_answer

    Actions:

        ask_question

        generate_options

        final_recommendation

    Observations:

        Updated state after each step

👉 See openenv.yaml for full specification
🔐 Environment Variables

Set in Hugging Face Secrets:

HF_TOKEN=your_token_here

📁 Project Structure

├── app.py              # Gradio UI
├── inference.py        # Agent logic
├── env/                # Environment
├── utils/              # Prompts + parsing
├── evaluation/         # Scoring
├── openenv.yaml        # Environment spec
├── Dockerfile
├── requirements.txt

🐳 Docker

docker build -t decision-coach .
docker run -p 7860:7860 decision-coach

🎯 Example Input

I want to pursue art as a career, but my family wants me to take a stable job.

🏁 Hackathon Focus

    Real-world decision simulation

    Structured AI reasoning

    End-to-end system design

    Live deployment

⚡ Tagline

    AI that helps you think, not just answer.