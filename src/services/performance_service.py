"""
Performance service module.

Provides high-level operations for managing exercise performances,
including logging new entries and retrieving histories.
"""

from typing import Optional


def log_performance(workout_id: int, exercise_name: str, reps: int, weight: float, rpe: Optional[int] = None) -> int:
    """
    Log a new performance for an exercise in a given workout.

    Args:
        workout_id (int): The workout ID.
        exercise_name (str): The exercise name.
        reps (int): Number of repetitions.
        weight (float): Weight lifted.
        rpe (Optional[int]): Rate of perceived exertion, optional.

    Returns:
        int: The ID of the inserted performance, -1 on failure.
    """


def get_exercise_history(name: str) -> list[dict]:
    """
    Retrieve the full history of performances for a given exercise.

    Args:
        name (str): The exercise name.

    Returns:
        list[dict]: List of performance entries, each containing:
            - id (int): Performance ID
            - date (str): Workout date
            - reps (int): Number of repetitions
            - weight (float): Weight lifted
            - rpe (int, optional): RPE value
    """


def get_workout_performances(workout_id: int) -> list[dict]:
    """
    Retrieve all performances associated with a given workout.

    Args:
        workout_id (int): The workout ID.

    Returns:
        list[dict]: List of performances, each containing:
            - id (int): Performance ID
            - exercise (str): Exercise name
            - reps (int): Number of repetitions
            - weight (float): Weight lifted
            - rpe (int, optional): RPE value
    """
