from utils.llm_grader import llm_grade

def rule_based_score(state):
    score = 0.0

    if state.get("final_answer"):
        score += 0.3
    if len(state.get("collected_info", [])) >= 2:
        score += 0.2
    if len(state.get("options", [])) >= 2:
        score += 0.2
    if state.get("tradeoffs"):
        score += 0.15
    if state.get("step", 0) <= 5:
        score += 0.15

    return min(score, 1.0)


def grade(state):
    rule_score = rule_based_score(state)
    llm_score = llm_grade(state)

    final_score = 0.6 * rule_score + 0.4 * llm_score

    return {
        "final_score": round(final_score, 2),
        "rule_score": round(rule_score, 2),
        "llm_score": round(llm_score, 2)
    }