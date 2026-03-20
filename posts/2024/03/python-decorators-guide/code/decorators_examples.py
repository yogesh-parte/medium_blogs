"""
Python Decorators - Complete Examples
Comprehensive code samples for the blog post on Python decorators
"""

import time
import functools
from typing import Callable, Any


# ============================================
# 1. BASIC DECORATORS
# ============================================

def simple_decorator(func):
    """Most basic decorator - prints before and after function call"""
    def wrapper():
        print("Before function execution")
        func()
        print("After function execution")
    return wrapper


@simple_decorator
def say_hello():
    print("Hello, World!")


# ============================================
# 2. DECORATORS WITH ARGUMENTS AND RETURN VALUES
# ============================================

def decorator_with_args(func):
    """Decorator that handles function arguments and return values"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"Function returned: {result}")
        return result
    return wrapper


@decorator_with_args
def add(a, b):
    """Add two numbers"""
    return a + b


# ============================================
# 3. TIMING DECORATOR
# ============================================

def timer(func):
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper


@timer
def slow_function(seconds=2):
    """Simulate a slow function"""
    time.sleep(seconds)
    return f"Slept for {seconds} seconds"


# ============================================
# 4. LOGGING DECORATOR
# ============================================

def log_calls(func):
    """Decorator to log function calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f">>> Entering {func.__name__}")
        print(f"    Args: {args}")
        print(f"    Kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"<<< Exiting {func.__name__} - Result: {result}")
            return result
        except Exception as e:
            print(f"!!! Exception in {func.__name__}: {e}")
            raise
    return wrapper


@log_calls
def divide(a, b):
    """Divide two numbers"""
    return a / b


# ============================================
# 5. DECORATORS WITH PARAMETERS
# ============================================

def repeat(times: int):
    """Decorator factory - repeats function execution N times"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"Execution {i+1}/{times}")
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"


def retry(max_attempts: int = 3, delay: int = 1):
    """Decorator to retry function execution on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"Failed after {max_attempts} attempts")
                        raise
                    print(f"Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_attempts=3, delay=1)
def unreliable_function():
    """Function that might fail"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Connection failed")
    return "Success!"


# ============================================
# 6. CLASS DECORATORS
# ============================================

def add_repr(cls):
    """Class decorator to add a custom __repr__ method"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls


@add_repr
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email


def dataclass_like(cls):
    """Decorator that adds useful methods to a class"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    cls.__init__ = __init__
    cls.__repr__ = __repr__
    return cls


@dataclass_like
class Book:
    pass


# ============================================
# 7. CHAINING DECORATORS
# ============================================

@timer
@log_calls
@repeat(times=2)
def chained_function(x):
    """Function with multiple decorators"""
    return x * 2


# ============================================
# 8. CACHING DECORATOR
# ============================================

def cache(func):
    """Simple caching decorator using functools.lru_cache"""
    @functools.lru_cache(maxsize=128)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@cache
def fibonacci(n):
    """Calculate nth Fibonacci number with caching"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# ============================================
# 9. VALIDATION DECORATOR
# ============================================

def validate_types(**type_checks):
    """Decorator to validate argument types"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name, expected_type in type_checks.items():
                if arg_name in kwargs:
                    if not isinstance(kwargs[arg_name], expected_type):
                        raise TypeError(
                            f"{arg_name} must be {expected_type}, "
                            f"got {type(kwargs[arg_name])}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate_types(name=str, age=int)
def create_user(name, age):
    return f"User: {name}, Age: {age}"


# ============================================
# MAIN - Run examples
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("PYTHON DECORATORS EXAMPLES")
    print("=" * 50)
    
    # Basic decorator
    print("\n1. BASIC DECORATOR:")
    say_hello()
    
    # With arguments
    print("\n2. DECORATOR WITH ARGUMENTS:")
    result = add(5, 3)
    print(f"Result: {result}\n")
    
    # Timing
    print("3. TIMING DECORATOR:")
    slow_function(1)
    
    # Logging
    print("\n4. LOGGING DECORATOR:")
    try:
        divide(10, 2)
        divide(10, 0)
    except ZeroDivisionError:
        print("Caught division by zero\n")
    
    # Repeat
    print("5. REPEAT DECORATOR:")
    greets = greet("Alice")
    print(f"Greetings: {greets}\n")
    
    # Class decorator
    print("6. CLASS DECORATOR:")
    person = Person("Bob", 30, "bob@example.com")
    print(person)
    
    book = Book(title="Python Guide", author="John Doe", pages=350)
    print(book)
    
    # Caching
    print("\n7. CACHING DECORATOR:")
    print(f"Fibonacci(10) = {fibonacci(10)}")
    
    # Type validation
    print("\n8. TYPE VALIDATION DECORATOR:")
    user = create_user(name="Charlie", age=25)
    print(user)
