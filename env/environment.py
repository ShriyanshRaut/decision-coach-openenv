class DecisionCoachEnv:

    def __init__(self):
        self.current_state = None


    def reset(self, user_problem=""):
        self.current_state = {
            "user_problem": user_problem,
            "conversation_history": [],
            "step": 0,
            "collected_info": [],
            "options": [],
            "final_answer": None
        }
        return self.current_state


    def state(self):
        return self.current_state

    def step(self, action):


        self.current_state["step"] += 1
        step = self.current_state["step"]


        content = action.get("content") or "No valid response generated"


        if step in [1, 2]:
            if isinstance(content, list):
                content = "Can you clarify your situation a bit more?"

        # Step 3 → options (ensure list format)
        if step == 3:
            if not isinstance(content, list):
                content = [str(content)]

        
        if step == 4:
            if isinstance(content, list):
                content = "Here are the tradeoffs between the options."

        # Step 5 → final recommendation
        if step == 5:
            if not content:
                content = "Start by taking one small actionable step toward your goal."

        
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

        
        action = {
            "type": action_type,
            "content": content
        }

        
        self.current_state["conversation_history"].append(action)

        

        if action_type == "ask_clarifying_question":
            self.current_state["collected_info"].append(content)

        elif action_type == "generate_options":
            if isinstance(content, list):
                self.current_state["options"].extend(content)
            else:
                self.current_state["options"].append(content)

        elif action_type == "final_recommendation":
            self.current_state["final_answer"] = content

      
        try:
            from env.reward import compute_reward
            reward = compute_reward(action, self.current_state)
        except:
            reward = 0
         
            reward -= 0.05 * step           

 
        done = (action_type == "final_recommendation") or (step >= 5)
        
        self.current_state["efficiency"] = 1 / step

        return self.current_state, reward, done, {}