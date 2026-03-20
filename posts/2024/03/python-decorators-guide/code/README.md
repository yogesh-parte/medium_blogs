# Code Samples - Python Decorators Guide

This folder contains complete Python examples for the blog post on decorators.

## Files

- `decorators_examples.py` - Comprehensive examples of different decorator patterns

## Running the Code

### Prerequisites

- Python 3.7+
- No external dependencies required

### Execution

Run the complete examples:

```bash
python decorators_examples.py
```

Or import specific decorators:

```python
from decorators_examples import timer, log_calls, repeat

@timer
@log_calls
def my_function():
    pass
```

## Topics Covered

1. **Basic Decorators** - Simple function decoration
2. **Decorators with Arguments** - Handling args and return values
3. **Timing Decorator** - Measure execution time
4. **Logging Decorator** - Log function calls and results
5. **Parameterized Decorators** - Decorators that accept parameters
6. **Retry Decorator** - Automatic retry logic
7. **Class Decorators** - Decorating classes
8. **Chaining Decorators** - Combining multiple decorators
9. **Caching Decorator** - Memoization using functools
10. **Validation Decorator** - Type checking for arguments

## Example Usage

```python
# Use the timer decorator
@timer
def slow_operation():
    time.sleep(2)
    return "Done"

# Use the retry decorator
@retry(max_attempts=3, delay=1)
def api_call():
    # Your API call here
    pass

# Combine decorators
@timer
@log_calls
def process_data(data):
    return sum(data)
```

## Notes

- All examples follow PEP 8 style guidelines
- `functools.wraps` is used to preserve function metadata
- Examples are educational and ready for production use
- Each decorator includes docstrings and type hints where appropriate

## Further Reading

- [Python functools Documentation](https://docs.python.org/3/library/functools.html)
- [Real Python: Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Decorator Pattern in Design Patterns](https://refactoring.guru/design-patterns/decorator)
