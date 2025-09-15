class Performance:
    def __init__(self, reps: int, weight: float, rpe: int = None):
        self.reps = reps
        self.weight = weight
        self.rpe = rpe

    def __str__(self):
        rpe_str = f", RPE {self.rpe}" if self.rpe else ""
        return f"[Performance] {self.reps} reps @ {self.weight} kg{rpe_str}"

    def volume(self) -> float:
        return self.reps * self.weight
