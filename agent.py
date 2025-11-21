import requests
import json
from tools import available_tools

class Agent:
    def __init__(self, model="llama3.2", system_prompt="You are a helpful AI assistant.", tools=None):
        self.model = model
        self.tools = tools or {}
        
        # Enhance system prompt with tool instructions if tools are present
        if self.tools:
            tool_descriptions = "\n".join([f"- {name}: {func.__doc__}" for name, func in self.tools.items()])
            system_prompt += f"\n\nYou have access to the following tools:\n{tool_descriptions}\n\nTo use a tool, you MUST respond with ONLY the following format:\nTOOL: <tool_name> <arguments>\n\nExample:\nTOOL: calculate 2 + 2\n\nDo not explain your reasoning, just use the tool if needed."
            
        self.system_prompt = system_prompt
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

    def chat(self, user_input):
        # Add user message
        self.history.append({"role": "user", "content": user_input})
        
        return self._process_turn()

    def _process_turn(self, max_turns=5):
        for _ in range(max_turns):
            payload = {
                "model": self.model,
                "messages": self.history,
                "stream": False
            }
            
            try:
                response = requests.post("http://localhost:11434/api/chat", json=payload)
                response.raise_for_status()
                result = response.json()
                
                assistant_response = result.get("message", {}).get("content", "").strip()
                print(f"[DEBUG] Raw response: {assistant_response}") # Debugging
                self.history.append({"role": "assistant", "content": assistant_response})
                
                # Check for tool call
                if "TOOL:" in assistant_response:
                    # Extract the tool command
                    command = assistant_response[assistant_response.find("TOOL:"):]
                    # Handle cases where there might be text after the command (newline)
                    if "\n" in command:
                        command = command.split("\n")[0]
                        
                    tool_output = self._execute_tool(command)
                    print(f"[DEBUG] Tool Output: {tool_output}") # Debugging
                    self.history.append({"role": "user", "content": f"Tool Output: {tool_output}"})
                    # Continue the loop to get the final answer
                    continue
                
                return assistant_response
            except requests.exceptions.RequestException as e:
                return f"Error communicating with Ollama: {e}"
        
        return "Error: Maximum tool turns exceeded."

    def _execute_tool(self, command):
        try:
            # Parse "TOOL: <name> <args>"
            parts = command.split(" ", 2)
            if len(parts) < 2:
                return "Error: Invalid tool command format."
            
            tool_name = parts[1]
            tool_args = parts[2] if len(parts) > 2 else None
            
            if tool_name in self.tools:
                func = self.tools[tool_name]
                if tool_args:
                    return func(tool_args)
                else:
                    return func()
            else:
                return f"Error: Tool '{tool_name}' not found."
        except Exception as e:
            return f"Error executing tool: {e}"

    def clear_history(self):
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})
