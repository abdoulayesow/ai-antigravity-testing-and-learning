from agent import Agent
import sys

def main():
    print("Initializing Agent...")
    # You can change the model here if you have a different one pulled, e.g., "mistral"
    from tools import available_tools
    agent = Agent(model="llama3.2", system_prompt="You are a helpful AI assistant running locally.", tools=available_tools)
    
    print(f"Agent initialized with model: {agent.model}")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue
                
            print("Agent: ...", end="\r")
            response = agent.chat(user_input)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
