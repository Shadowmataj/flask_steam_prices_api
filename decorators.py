from datetime import datetime

def time_decorator(func):
    """Decorator to check the time spend on a function."""
    def wrapper():
        # start
        begin = datetime.now()
        func()
        # end
        end = datetime.now()
        # total time
        total = end - begin
        print(f"Total time: {total.total_seconds()} s")

    return wrapper