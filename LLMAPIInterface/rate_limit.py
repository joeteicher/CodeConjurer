import time

# Assuming a simple rate limit rule: a maximum number of requests per time period
MAX_REQUESTS = 10  # Max number of requests
TIME_PERIOD = 60  # Time period in seconds

class RateLimiter:
    def __init__(self):
        self.requests = []

    def check_rate_limit(self):
        """
        Checks if the rate limit has been reached.
        :return: bool, True if rate limit is reached, False otherwise.
        """
        current_time = time.time()
        self.requests = [req for req in self.requests if current_time - req < TIME_PERIOD]

        if len(self.requests) >= MAX_REQUESTS:
            return True
        return False

    def wait_for_slot(self):
        """
        Waits until there is a slot available to make a request.
        """
        while self.check_rate_limit():
            time.sleep(1)
        self.requests.append(time.time())

# This can be used for testing the functions in this class.
if __name__ == "__main__":
    # Example usage and testing
    rate_limiter = RateLimiter()
    for _ in range(MAX_REQUESTS):
        if not rate_limiter.check_rate_limit():
            print("Request allowed")
            rate_limiter.requests.append(time.time())
        else:
            print("Rate limit reached, waiting...")
            rate_limiter.wait_for_slot()
            print("Slot available, proceeding with request")
