
# Test suite for exchange_rates_finder
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
    from agents.exchange_rates_finder.content import *
    from agents.exchange_rates_finder.functions import *

    class MockTriageAgent:
        def __call__(self):
            return "Mock triage called"
    mock_triage = MockTriageAgent()

    from agents.exchange_rates_finder.agent import create_exchange_rates_finder_agent
    agent = create_exchange_rates_finder_agent(mock_triage)

    def test_memory_manager():
        memory_manager.clear_agent('exchange_rates_finder')
        test_data = {'test': 'data'}
        memory_manager.store('exchange_rates_finder', 'test_key', test_data)
        retrieved = memory_manager.retrieve('exchange_rates_finder', 'test_key')
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

    print("Running tests for exchange_rates_finder agent...")
    test_memory_manager()
    test_agent_functions()
    print("Basic tests passed!")
    all_tests_passed = True

except Exception as e:
    print(f"Test failed: {str(e)}")
    all_tests_passed = False
