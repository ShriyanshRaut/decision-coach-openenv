def build_prompt(state):

    step = state["step"]

    # 🎯 STEP-AWARE INSTRUCTIONS
    if step == 0:
        instruction = (
            "Ask ONE clear and specific clarifying question about the user's problem. "
            "Avoid generic questions. Focus on understanding their situation deeply."
        )

    elif step == 1:
        instruction = (
            "Ask ONE deeper follow-up question based on previous context. "
            "Do NOT repeat earlier questions. Do NOT generate options."
        )

    elif step == 2:
        instruction = (
            "Generate 3-5 DISTINCT and SPECIFIC options as a JSON LIST of strings. "
            "Each option must be realistic and tailored to the user's situation. "
            "Avoid vague advice."
        )

    elif step == 3:
        instruction = (
            "Evaluate tradeoffs between the options. "
            "Compare them using pros, cons, risks, and benefits. "
            "Be specific and practical. DO NOT generate new options."
        )

    else:
        instruction = (
            "Provide a FINAL recommendation. "
            "It MUST be specific, actionable, and realistic. "
            "Include concrete next steps the user can take immediately."
        )

    return f"""
You are a highly capable decision-making AI agent.

STRICT RULES:
- Follow ONLY the instruction for the current step
- Do NOT mix multiple actions
- Do NOT ask questions unless instructed
- Avoid generic advice
- Be specific and practical

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

IMPORTANT:
- Output MUST be STRICTLY valid JSON
- NO text before or after JSON
- Use double quotes properly
- Ensure commas are correct
- If content is a list → return valid JSON list

Example:
{{
  "type": "generate_options",
  "content": ["Option 1", "Option 2", "Option 3"]
}}

Respond ONLY in JSON:
{{
  "type": "...",
  "content": ...
}}
"""