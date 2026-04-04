import json
import re

VALID_TYPES = [
    "ask_clarifying_question",
    "generate_options",
    "evaluate_tradeoffs",
    "final_recommendation"
]

def parse_action(response_text):
    try:
        # ✅ Ensure string (fixes list/dict error)
        if not isinstance(response_text, str):
            response_text = json.dumps(response_text)

        # ✅ Extract JSON safely (non-greedy)
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)

        if not match:
            raise ValueError("No JSON found")

        action = json.loads(match.group())

        # ✅ Validate type
        if action.get("type") not in VALID_TYPES:
            action["type"] = "ask_clarifying_question"

        # ✅ Validate content
        content = action.get("content", "")

        if not content or len(str(content).strip()) < 10:
            content = "Please provide more specific details about your situation."

        # ✅ Block lazy responses
        if isinstance(content, str) and "clarify more" in content.lower():
            content = "Can you describe a specific situation where you felt uncertain about your career?"

        action["content"] = content

        return action

    except Exception as e:
        print("Parse error:", e)

        # 🚨 Always-safe fallback
        return {
            "type": "ask_clarifying_question",
            "content": "Can you describe a specific issue you're facing instead of general confusion?"
        }