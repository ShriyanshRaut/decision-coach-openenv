def compute_reward(action, state):
    if action["type"] == "ask_clarifying_question":
        return 0.1
    elif action["type"] == "generate_options":
        return 0.3
    elif action["type"] == "evaluate_tradeoffs":
        return 0.5
    elif action["type"] == "final_recommendation":
        return 1.0
    return 0.0