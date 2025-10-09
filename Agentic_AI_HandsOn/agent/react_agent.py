from typing import List
import requests
import json
from tools import Tools
from agent import Action, Observation, ThoughtStep, AgentResponse, ActionType


class ReActAgent:
    def __init__(self):
        self.tools = Tools()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.system_prompt = """You are an AI assistant that follows the ReAct (Reasoning + Acting) pattern.
        Your goal is to help users by breaking down complex tasks into a series of thought-out steps and actions.

        You have access to these tools:
        1. search: Search for information using DuckDuckGo. Returns top 3 relevant results.
        2. calculate: Perform mathematical calculations

        For each step, you should:
        1. Think about what needs to be done
        2. Decide on an action if needed
        3. Observe the results
        4. PAUSE to reflect on the results
        5. Continue this process until you can provide a final answer

        Follow this format strictly:
        Thought: [Your reasoning about what needs to be done]
        Action: {action_type: "search/calculate", input: {query/expression}}
        Observation: [Result from tool]
        PAUSE: [Reflect on the observation and decide next steps]
        ... (repeat Thought/Action/Observation/PAUSE as needed)
        Thought: I now know the final answer
        Final Answer: [Your detailed answer here]

        Important guidelines:
        - Break down complex problems into smaller steps
        - Use search to gather information you're not certain about
        - Use calculate for any mathematical operations
        - After each observation, PAUSE to:
            * Evaluate if the information is sufficient
            * Consider if additional verification is needed
            * Plan the next logical step
            * Identify any potential errors or inconsistencies
        - Provide clear reasoning in your thoughts
        - Make sure your final answer is complete and well-explained
        - If you encounter an error, explain what went wrong and try a different approach
        """

    def _format_history(self, thought_process: List[ThoughtStep]) -> str:
        history = ""
        for step in thought_process:
            history += f"Thought: {step.thought}\n"
            if step.action:
                history += f"Action: {step.action.model_dump_json()}\n"
            if step.observation:
                history += f"Observation: {step.observation.result}\n"
            if step.pause_reflection:
                history += f"PAUSE: {step.pause_reflection}\n"
        return history

    def execute_tool(self, action: Action) -> str:
        if action.action_type == ActionType.SEARCH:
            return self.tools.search(action.input["query"])
        elif action.action_type == ActionType.CALCULATE:
            return self.tools.calculate(action.input["expression"])
        return "Error: Unknown action type"

    async def _get_llama_response(self, prompt: str) -> str:
        payload = {
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.ollama_url, json=payload)
        if response.status_code == 200:
            result = response.json()['response'].split("</think>")[-1]
            result
            return result
        else:
            raise Exception(f"Error from Ollama API: {response.text}")

    async def run(self, query: str) -> AgentResponse:
        thought_process: List[ThoughtStep] = []

        while True:
            # Prepare conversation prompt
            prompt = f"{self.system_prompt}\n\nQuestion: {query}\n\n"
            if thought_process:
                prompt += self._format_history(thought_process)

            # Get next step from Llama2
            step_text = await self._get_llama_response(prompt)

            # Parse the response
            if "Final Answer:" in step_text:
                # Extract final answer
                final_answer = step_text.split("Final Answer:")[1].strip()
                thought = step_text.split("Thought:")[1].split("Final Answer:")[0].strip()
                thought_process.append(ThoughtStep(thought=thought))
                return AgentResponse(
                    thought_process=thought_process,
                    final_answer=final_answer
                )
            else:
                try:
                    # Parse thought and action
                    thought = step_text.split("Thought:")[1].split("Action:")[0].strip()
                    action_text = step_text.split("Action:")[1].split("Observation:")[0].strip()
                    action_data = json.loads(action_text)

                    action = Action(
                        action_type=action_data["action_type"],
                        input=action_data["input"]
                    )

                    # Execute action
                    result = self.execute_tool(action)
                    observation = Observation(result=result)

                    # Parse PAUSE reflection if present
                    pause_reflection = None
                    if "PAUSE:" in step_text:
                        pause_parts = step_text.split("PAUSE:")
                        if len(pause_parts) > 1:
                            pause_reflection = pause_parts[1].split("Thought:")[0].strip()

                    # Add to thought process
                    thought_process.append(ThoughtStep(
                        thought=thought,
                        action=action,
                        observation=observation,
                        pause_reflection=pause_reflection
                    ))
                except Exception as e:
                    # Handle parsing errors
                    print(f"Error parsing LLM response: {e}")
                    print(f"Raw response: {step_text}")
                    return AgentResponse(
                        thought_process=thought_process,
                        final_answer="Error: Failed to parse LLM response"
                    ) 