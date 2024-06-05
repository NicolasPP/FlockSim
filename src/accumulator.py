class Accumulator:
    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.value: float = 0.0

    def wait(self, delta_time: float) -> bool:
        self.value += delta_time
        if self.value >= self.limit:
            self.value = 0
            return True
        return False

    def set_limit(self, limit: float) -> None:
        if limit <= 0: return
        self.limit = limit

    def get_limit(self) -> float:
        return self.limit
