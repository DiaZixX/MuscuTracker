from datetime import datetime

from models.exercise import Exercise
from models.performance import Performance


class Workout:
    def __init__(self, date: datetime = None):
        self.date = date if date else datetime.now()
        self.all_exercices = {}

    def __str__(self):
        return f"[Workout] Date : {self.date} | "

    def add_performance(self, exercise: Exercise, performance: Performance) -> None:
        if exercise not in self.all_exercices:
            self.all_exercices[exercise] = []
        self.all_exercices[exercise].append(performance)

    def total_volume(self) -> float:
        return sum(p.volume() for sets in self.all_exercices.values for p in sets)

    def summary(self) -> str:
        lines = [f"Workout on {self.date.strftime('%Y-%m-%d')}"]
        for exercise, sets in self.exercises.items():
            lines.append(f"- {exercise}:")
            for p in sets:
                lines.append(f"   {p}")
        lines.append(f"Total volume: {self.total_volume()} kg")
        return "\n".join(lines)
