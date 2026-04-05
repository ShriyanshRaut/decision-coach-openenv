class AgentState:
    def __init__(self, user_problem: str):
        self.user_problem = user_problem
        self.step = 0
        self.conversation_history = []
        self.options = []
        self.final_answer = ""

    def add_step(self, action_type: str, content):
        self.conversation_history.append({
            "type": action_type,
            "content": content
        })
        self.step += 1

    def set_options(self, options):
        self.options = options

    def set_final_answer(self, answer):
        self.final_answer = answer

    def to_dict(self):
        return {
            "user_problem": self.user_problem,
            "step": self.step,
            "conversation_history": self.conversation_history,
            "options": self.options,
            "final_answer": self.final_answer
        }
    def summary(self):
       return {
        "steps": self.step,
        "num_options": len(self.options),
        "has_final_answer": bool(self.final_answer)
    }