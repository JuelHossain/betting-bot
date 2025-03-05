"""
Sequence handler for visualizing API requests in sequence.

This module provides a class to handle sequences of API requests
with visual indicators in the terminal.
"""
import time
import sys
from typing import Callable, Any, List, Dict, Optional
import threading

# Try to import tqdm, install if not available
try:
    from tqdm import tqdm
except ImportError:
    import subprocess
    print("Installing required package: tqdm")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm

# ASCII art components
SPINNER_CHAR = "⏳"
TICK_CHAR = "✅"
ERROR_CHAR = "❌"
STEP_DOT = "●"
CONNECTING_LINE = "│"


class SequenceStep:
    """
    Represents a single step in a sequence.
    
    Each step has a description, a function to execute,
    and optional arguments for that function.
    """
    
    def __init__(self, description: str, func: Callable, **kwargs):
        """
        Initialize a sequence step.
        
        Args:
            description: Human-readable description of the step
            func: Function to execute
            **kwargs: Arguments to pass to the function
        """
        self.description = description
        self.func = func
        self.kwargs = kwargs
        self.result = None
        self.error = None
        self.is_complete = False
        self.is_success = False
    
    def execute(self, results: Dict[str, Any] = None) -> Any:
        """
        Execute the step's function with the provided arguments.
        
        Args:
            results: Results from previous steps
            
        Returns:
            Any: Result of the function
        """
        try:
            # Process any lambda functions in kwargs
            processed_kwargs = {}
            for k, v in self.kwargs.items():
                if callable(v) and not isinstance(v, type):
                    # If it's a lambda function, call it with the results
                    processed_kwargs[k] = v(results or {})
                else:
                    # Otherwise just use the value directly
                    processed_kwargs[k] = v
            
            # Execute the function with the processed kwargs
            self.result = self.func(**processed_kwargs)
            self.is_complete = True
            self.is_success = True
            return self.result
        except Exception as e:
            self.error = str(e)
            self.is_complete = True
            self.is_success = False
            return None


class SequenceHandler:
    """
    Handler for sequences of API requests with visual indicators.
    
    This class manages a sequence of steps, executes them in order,
    and displays visual progress indicators in the terminal.
    """
    
    def __init__(self, title: str = "API Sequence"):
        """
        Initialize a sequence handler.
        
        Args:
            title: Title of the sequence
        """
        self.title = title
        self.steps: List[SequenceStep] = []
        self.results: Dict[str, Any] = {}
        self._spinner_active = False
        self._spinner_thread = None
    
    def add_step(self, description: str, func: Callable, **kwargs) -> 'SequenceHandler':
        """
        Add a step to the sequence.
        
        Args:
            description: Human-readable description of the step
            func: Function to execute
            **kwargs: Arguments to pass to the function
            
        Returns:
            SequenceHandler: Self for method chaining
        """
        self.steps.append(SequenceStep(description, func, **kwargs))
        return self
    
    def _show_spinner(self, description: str, step_index: int):
        """
        Show a spinner animation until stopped.
        
        Args:
            description: Description to show with the spinner
            step_index: Index of the current step
        """
        self._spinner_active = True
        
        # Use tqdm for the spinner
        with tqdm(desc=f"{SPINNER_CHAR} {description}", bar_format="{desc}", leave=False) as pbar:
            i = 0
            spinner_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
            while self._spinner_active:
                pbar.set_description_str(f"{SPINNER_CHAR} {description} {spinner_chars[i % len(spinner_chars)]}")
                time.sleep(0.1)
                i += 1
    
    def _start_spinner(self, description: str, step_index: int):
        """
        Start the spinner animation in a separate thread.
        
        Args:
            description: Description to show with the spinner
            step_index: Index of the current step
        """
        self._spinner_active = True
        self._spinner_thread = threading.Thread(
            target=self._show_spinner,
            args=(description, step_index)
        )
        self._spinner_thread.daemon = True
        self._spinner_thread.start()
    
    def _stop_spinner(self):
        """Stop the spinner animation."""
        self._spinner_active = False
        if self._spinner_thread:
            self._spinner_thread.join(timeout=1.0)
    
    def execute(self, continue_on_error: bool = False) -> Dict[str, Any]:
        """
        Execute all steps in the sequence.
        
        Args:
            continue_on_error: Whether to continue executing steps after an error
            
        Returns:
            Dict[str, Any]: Results of all successful steps
        """
        print(f"\n=== {self.title} ===")
        print("=" * (len(self.title) + 8))
        
        for i, step in enumerate(self.steps):
            # Show step indicator
            print(f"\n{STEP_DOT} {step.description}")
            
            # Start spinner
            self._start_spinner(step.description, i)
            
            # Execute step with results from previous steps
            step.execute(self.results)
            
            # Stop spinner
            self._stop_spinner()
            
            # Show result
            if step.is_success:
                print(f"{TICK_CHAR} {step.description} - Completed")
                self.results[f"step_{i}"] = step.result
                
                # Add a more descriptive key based on the step description
                key_name = step.description.lower().replace(" ", "_")
                self.results[key_name] = step.result
            else:
                print(f"{ERROR_CHAR} {step.description} - Failed: {step.error}")
                if not continue_on_error:
                    print(f"\n{ERROR_CHAR} Sequence aborted at step {i+1}: {step.description}")
                    break
            
            # Show connecting line to next step
            if i < len(self.steps) - 1:
                print(f"{CONNECTING_LINE}")
        
        # Show completion
        if all(step.is_success for step in self.steps):
            print(f"\n✨ {self.title} completed successfully! ✨")
        else:
            print(f"\n{ERROR_CHAR} {self.title} completed with errors.")
        
        return self.results
