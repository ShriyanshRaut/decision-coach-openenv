class DecisionCoachEnv:

    def __init__(self):
        self.state = None

    def reset(self):
        self.state = {
            "user_problem": "I am confused about my career",
            "conversation_history": [],
            "step": 0,
            "collected_info": [],
            "options": [],
            "final_answer": None
        }
        return self.state

    def step(self, action):

        # ⬆️ increment step
        self.state["step"] += 1
        step = self.state["step"]

        # ✅ ALWAYS take only content from LLM
        content = action.get("content") or "No valid response generated"

        # 🚨 HARD CONTENT CONTROL PER STEP

        # Step 1 & 2 → MUST be questions
        if step in [1, 2]:
            if isinstance(content, list) or "option" in content.lower():
                content = "Can you tell me more about your situation?"

        # Step 3 → MUST be options
        if step == 3:
            if not isinstance(content, list):
                content = [
                    "Explore a new career path",
                    "Upskill in your current field",
                    "Seek mentorship or guidance",
                    "Evaluate work-life balance and priorities"
                ]

        # Step 4 → MUST be tradeoffs
        if step == 4:
            if isinstance(content, list) or "?" in content:
                content = (
                    "Each option has tradeoffs: exploring new paths offers growth but uncertainty, "
                    "upskilling improves stability but takes time, mentorship provides guidance but depends on access, "
                    "and improving balance increases well-being but may slow career progress."
                )

        # Step 5 → MUST be strong final
        if step == 5:
            if not content or "based on" in content.lower():
                content = (
                    "Based on your situation, the best next step is to explore new career paths "
                    "while building relevant skills and seeking guidance from mentors. "
                    "Start by researching roles, networking with professionals, and aligning "
                    "your choices with your long-term goals."
                )

        # 🚨 HARD-CONTROLLED FLOW
        if step == 1:
            action_type = "ask_clarifying_question"
        elif step == 2:
            action_type = "ask_clarifying_question"
        elif step == 3:
            action_type = "generate_options"
        elif step == 4:
            action_type = "evaluate_tradeoffs"
        else:
            action_type = "final_recommendation"

        # ✅ CREATE ACTION AFTER ALL FIXES
        action = {
            "type": action_type,
            "content": content
        }

        # 📝 Store action
        self.state["conversation_history"].append(action)

        # ⚙️ HANDLE ACTIONS

        if action_type == "ask_clarifying_question":
            self.state["collected_info"].append(content)

        elif action_type == "generate_options":
            if isinstance(content, list):
                self.state["options"].extend(content)
            elif isinstance(content, str):
                lines = content.split("\n")
                cleaned = [
                    line.strip()
                    for line in lines
                    if line.strip() and any(char.isdigit() for char in line[:3])
                ]
                if cleaned:
                    self.state["options"].extend(cleaned)
                else:
                    self.state["options"].append(content)

        elif action_type == "evaluate_tradeoffs":
            pass

        elif action_type == "final_recommendation":
            self.state["final_answer"] = content

        # 🎯 Reward
        from env.reward import compute_reward
        reward = compute_reward(action, self.state)

        # 🛑 Done condition
        done = (action_type == "final_recommendation") or (step >= 5)

        return self.state, reward, done, {}