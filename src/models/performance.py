class Performance:
    """
    Class for the performance on a given exercise

    Keep track of the number of reps, the associated weights and the personnal feeling

    Attributes:
        reps (int): number of reps
        weight (float): the weight used
        rpe (int): feeling of the exercise (between 1 and 10)
    """

    def __init__(self, reps: int, weight: float, rpe: int = None):
        """
        Initialize the performance

        Args:
            reps (int): number of reps
            weight (float): the weight used
            rpe (int): feeling of the exercise (between 1 and 10)

        Raises:
            ValueError: If rpe is not between 1 and 10 included
        """
        self.reps = reps
        self.weight = weight

        if rpe is not None or not (1 <= rpe <= 10):
            raise ValueError("rpe value must be between 1 and 10 included")
        self.rpe = rpe

    def __str__(self):
        """
        Visualization of the object
        """
        rpe_str = f", RPE {self.rpe}" if self.rpe else ""
        return f"[Performance] {self.reps} reps @ {self.weight} kg{rpe_str}"

    def volume(self) -> float:
        """
        Compute the volume of the performance

        Returns:
            float: The volume associated to the performance
        """
        return self.reps * self.weight
