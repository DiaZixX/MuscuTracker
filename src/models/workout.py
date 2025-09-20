from datetime import datetime

from models.exercise import Exercise
from models.performance import Performance


class Workout:
    """
    Class for a gym workout

    Combines the exercise class and the perfomance class in order to describe the workout done

    Attributes:
        date (datetime): date of the workout
        all_exercise (dict): dictionary keeping track of all the exercises and performances associated
    """

    def __init__(self, date: datetime = None):
        """
        Initialize the workout

        Args:
            date (datetime): date of the workout
            all_exercise (dict): dictionary keeping track of all the exercises and performances associated
        """
        self.date = date if date else datetime.now()
        self.all_exercises = {}

    def __str__(self):
        """
        Visualization of the object
        """
        return f"[Workout] Date : {self.date} | "

    def add_performance(self, exercise: Exercise, performance: Performance) -> None:
        """
        Add a new performance in a new set or current set

        Args:
            exercise (Exercise): the description of the exercise
            performance (Performance): the performance associated to this exercise
        """
        if exercise not in self.all_exercises:
            self.all_exercises[exercise] = []
        self.all_exercises[exercise].append(performance)

    def total_volume(self) -> float:
        """
        Process the total volume of the workout

        Returns:
            float: the total volume
        """
        return sum(p.volume() for sets in self.all_exercises.values for p in sets)

    def summary(self) -> str:
        """
        Provides a summary of the workout in a formatted str

        Returns:
            str: the formatted string containing the summary
        """
        lines = [f"Workout on {self.date.strftime('%Y-%m-%d')}"]
        for exercise, sets in self.exercises.items():
            lines.append(f"- {exercise}:")
            for p in sets:
                lines.append(f"   {p}")
        lines.append(f"Total volume: {self.total_volume()} kg")
        return "\n".join(lines)
