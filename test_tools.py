from agent import Agent
from tools import available_tools
import time

def test_tools():
    print("Testing Agent Tool Usage...")
    agent = Agent(model="llama3.2", system_prompt="You are a helpful AI assistant.", tools=available_tools)
    
    # Test 1: Time
    print("\nTest 1: Asking for time")
    response = agent.chat("What time is it right now?")
    print(f"Response: {response}")
    
    # Test 2: Math
    print("\nTest 2: Math calculation")
    response = agent.chat("What is 123 plus 456?")
    print(f"Response: {response}")

if __name__ == "__main__":
    test_tools()
