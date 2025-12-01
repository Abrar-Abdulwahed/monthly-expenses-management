

def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(f"[ERROR] {func.__name__}: {exc}")
            raise
    return wrapper
