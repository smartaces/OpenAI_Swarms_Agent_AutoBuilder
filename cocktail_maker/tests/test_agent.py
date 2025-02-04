
# Test suite for cocktail_maker
import sys
import os
from pathlib import Path

# Add the main project path
sys.path.append('/content/swarm/examples/magic')

def check_for_errors(result):
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
    from base.memory_manager import memory_manager
    from agents.cocktail_maker.content import *
    from agents.cocktail_maker.functions import *

    class MockTriageAgent:
        def __call__(self):
            return "Mock triage called"
    mock_triage = MockTriageAgent()

    from agents.cocktail_maker.agent import create_cocktail_maker_agent
    agent = create_cocktail_maker_agent(mock_triage)

    def test_memory_manager():
        memory_manager.clear_agent('cocktail_maker')
        test_data = {'test': 'data'}
        memory_manager.store('cocktail_maker', 'test_key', test_data)
        retrieved = memory_manager.retrieve('cocktail_maker', 'test_key')
        assert retrieved == test_data, "Memory manager store/retrieve failed"

    def test_agent_functions():
        api_errors = []
        agent_functions = [f for f in agent.functions if not f.__name__.startswith('__')]
        for func in agent_functions:
            try:
                result = func()
                if check_for_errors(result):
                    api_errors.append(f"{func.__name__}: {result}")
            except Exception as e:
                print(f"Error testing {func.__name__}: {str(e)}")
                api_errors.append(f"{func.__name__}: {str(e)}")

        if api_errors:
            raise Exception("API Errors detected:\n" + "\n".join(api_errors))

    print("Running tests for cocktail_maker agent...")
    test_memory_manager()
    test_agent_functions()
    print("Basic tests passed!")
    all_tests_passed = True

except Exception as e:
    print(f"Test failed: {str(e)}")
    all_tests_passed = False
