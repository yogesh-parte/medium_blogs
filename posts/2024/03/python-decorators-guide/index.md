---
title: "Mastering Python Decorators: A Complete Guide"
date: 2024-03-15
updated: 2024-03-15
categories:
  - python
  - programming
tags:
  - python
  - decorators
  - functions
  - advanced-python
medium_url: "https://medium.com/@yourhandle/python-decorators-guide"
difficulty: "intermediate"
series: "Python Advanced Techniques"
series_part: 1
related:
  - "2024/03/python-context-managers"
---

# Mastering Python Decorators: A Complete Guide

Python decorators are one of the most powerful and flexible features of the language. They allow you to modify or enhance functions and classes without directly changing their source code. In this guide, we'll explore decorators from basics to advanced patterns.

## What is a Decorator?

A decorator is a function that takes another function or class as an argument and extends its behavior without modifying it permanently. It's a form of metaprogramming that makes your code more concise and reusable.

### Basic Concept

```python
def my_decorator(func):
    def wrapper():
        print("Something before the function")
        func()
        print("Something after the function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

## Simple Function Decorators

The simplest decorators wrap a function and execute code before and after it runs.

### Timing Decorator

Measure how long a function takes to execute:

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    return "Done"
```

### Logging Decorator

Log every function call:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b
```

## Decorators with Arguments

Decorators can accept arguments to customize their behavior:

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
# Output: ['Hello, Alice!', 'Hello, Alice!', 'Hello, Alice!']
```

## Class Decorators

Decorators can also modify classes:

```python
def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(person)  # Person(name=Alice, age=30)
```

## Built-in Decorators

Python provides several built-in decorators:

### @property

Convert methods to properties:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def area(self):
        return 3.14 * self._radius ** 2

circle = Circle(5)
print(circle.area)  # 78.5
```

### @staticmethod and @classmethod

Define static and class methods:

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b
    
    @classmethod
    def create_from_string(cls, values):
        return cls(*map(int, values.split(",")))
```

## Advanced Patterns

### Chaining Decorators

Apply multiple decorators:

```python
@timer
@log_calls
def process_data(data):
    return sum(data)
```

### Preserving Function Metadata

Use `functools.wraps` to preserve original function information:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper documentation"""
        return func(*args, **kwargs)
    return wrapper
```

## Best Practices

1. **Use functools.wraps** - Always preserve the original function's metadata
2. **Keep decorators simple** - Each decorator should have a single responsibility
3. **Document decorator behavior** - Clearly explain what your decorator does
4. **Consider side effects** - Be aware of decorators that modify global state
5. **Test decorators thoroughly** - They can be tricky to debug

## Common Use Cases

- **Authentication/Authorization** - Protect functions with access control
- **Caching** - Memoize expensive computations
- **Validation** - Check inputs before function execution
- **Retry logic** - Automatically retry failed operations
- **Rate limiting** - Control function call frequency
- **Dependency injection** - Inject dependencies into functions

## Conclusion

Decorators are a powerful tool for writing clean, reusable, and maintainable Python code. They enable you to separate concerns and reduce code duplication. By mastering decorators, you'll write more Pythonic and efficient code.

## Resources

- [Python Decorators Documentation](https://docs.python.org/3/glossary.html#term-decorator)
- [Real Python: Decorators](https://realpython.com/primer-on-python-decorators/)
- [PEP 318: Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)

---

**Published:** March 15, 2024  
**Last Updated:** March 15, 2024  
**Read on Medium:** [Link to Medium article](https://medium.com/@yourhandle/python-decorators-guide)
