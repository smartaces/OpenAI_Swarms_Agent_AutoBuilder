
# Test suite for nasa_info_grab
import sys
import os
from pathlib import Path

# Add the main project path
sys.path.append('/content/swarm/examples/magic')

def check_for_errors(result):
    """Check if the result contains error indicators"""
    result_str = str(result).lower()
    error_indicators = [
        'error:',
        'error ',
        'failed',
        'exception',
        'timeout',
        'certificate verify failed',
        'max retries exceeded',
        'ssl',
        'could not'
    ]
    return any(indicator in result_str for indicator in error_indicators)

try:
    # Test imports
    from base.memory_manager import memory_manager
    from agents.nasa_info_grab.content import *
    from agents.nasa_info_grab.functions import *

    # Create mock triage agent
    class MockTriageAgent:
        def __call__(self):
            return "Mock triage called"

    mock_triage = MockTriageAgent()

    # Import the agent creation function
    from agents.nasa_info_grab.agent import create_nasa_info_grab_agent

    # Create the agent instance
    agent = create_nasa_info_grab_agent(mock_triage)

    # Test memory manager integration
    def test_memory_manager():
        # Clear any existing memory
        memory_manager.clear_agent('nasa_info_grab')
        # Test store and retrieve
        test_data = {'test': 'data'}
        memory_manager.store('nasa_info_grab', 'test_key', test_data)
        retrieved = memory_manager.retrieve('nasa_info_grab', 'test_key')
        assert retrieved == test_data, "Memory manager store/retrieve failed"

    # Test agent functions
    def test_agent_functions():
        api_errors = []
        # Get all functions defined in the agent
        agent_functions = [f for f in agent.functions if not f.__name__.startswith('__')]

        # Test each function
        for func in agent_functions:
            try:
                result = func()
                if check_for_errors(result):
                    api_errors.append(f"{func.__name__}: {result}")
            except Exception as e:
                print(f"Error testing {func.__name__}: {str(e)}")
                api_errors.append(f"{func.__name__}: {str(e)}")

        if api_errors:
            raise Exception(f"API Errors detected:\n" + "\n".join(api_errors))

    # Run tests
    print("Running tests for nasa_info_grab agent...")
    test_memory_manager()
    test_agent_functions()
    print("Basic tests passed!")
    all_tests_passed = True

except Exception as e:
    print(f"Test failed: {str(e)}")
    all_tests_passed = False
