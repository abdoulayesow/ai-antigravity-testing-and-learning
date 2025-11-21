from agent import Agent
import sys

def test_agent():
    print("Testing Agent connection to Ollama...")
    try:
        # Use a small prompt to test
        agent = Agent(model="llama3.2", system_prompt="You are a test bot.")
        response = agent.chat("Hello, are you working?")
        print(f"Response received: {response}")
        
        if response and "Error" not in response:
            print("SUCCESS: Agent is working.")
        else:
            print("FAILURE: Agent returned an error or empty response.")
            
    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")

if __name__ == "__main__":
    test_agent()
