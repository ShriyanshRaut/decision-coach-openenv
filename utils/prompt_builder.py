def build_prompt(state):

    step = state["step"]

    # 🎯 STEP-AWARE INSTRUCTIONS (CRITICAL)
    if step == 0:
        instruction = "Ask ONE clear clarifying question about the user's problem."

    elif step == 1:
        instruction = "Ask ONE deeper clarifying question. Do NOT generate options."

    elif step == 2:
        instruction = (
            "Generate 3-5 distinct options as a LIST. "
            "Do NOT ask questions. Each option should be concise."
        )

    elif step == 3:
        instruction = (
        "Evaluate tradeoffs between the previously generated options. "
        "You MUST compare options using pros, cons, risks, and benefits. "
        "DO NOT generate new options. DO NOT ask questions. "
        "ONLY analyze and compare."
    )

    else:
        instruction = (
            "Provide a final recommendation based on the previous reasoning. "
            "Be specific and actionable."
        )

    return f"""
You are a decision-making AI agent.

STRICT RULES:
- Follow the instruction EXACTLY for the current step
- Do NOT mix multiple actions
- Do NOT ask questions unless explicitly told
- Stay concise and structured

Allowed types:
ask_clarifying_question
generate_options
evaluate_tradeoffs
final_recommendation

User Problem:
{state['user_problem']}

Conversation History:
{state['conversation_history']}

Current Step:
{step}

Instruction:
{instruction}

Respond ONLY in JSON format:
{{
  "type": "...",
  "content": ...
}}
"""