import time
from functools import wraps

# From https://glinteco.com/en/post/python-decorators-throttle/

def throttle(seconds):
    def decorator(func):
        last_called = [0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed >= seconds:
                last_called[0] = time.time()
                return func(*args, **kwargs)
            else:
                print("Function call throttled")
        return wrapper
    return decorator
