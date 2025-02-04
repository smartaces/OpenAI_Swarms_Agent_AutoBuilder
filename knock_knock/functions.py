"""
Functions for the knock knock jokes agent
"""
import random
import sys
import os

# Add the parent directory to the Python path
sys.path.append('/content/swarm/examples/magic')

from base.memory_manager import memory_manager
from agents.knock_knock.content import KNOCK_KNOCK_JOKES

def tell_knock_joke():
    """
    Select and return a knock knock joke that hasn't been told recently
    """
    # Get all jokes that haven't been told
    available_jokes = [joke for joke in KNOCK_KNOCK_JOKES
                      if not memory_manager.retrieve('knock_knock', str(joke))]

    # If all jokes have been told, reset memory
    if not available_jokes:
        memory_manager.clear_agent('knock_knock')
        available_jokes = KNOCK_KNOCK_JOKES

    # Select and mark joke as told
    chosen_joke = random.choice(available_jokes)
    memory_manager.store('knock_knock', str(chosen_joke), True)

    return chosen_joke
