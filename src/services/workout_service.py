"""
Workout service module.

Provides high-level operations for managing workouts,
such as creating a workout with exercises and performances,
listing workouts, and retrieving summaries.
"""

from datetime import datetime
from typing import Optional


def create_workout(date: datetime, exercises_with_perfs: list[dict]) -> int:
    """
    Create a workout with multiple exercises and performances.

    Args:
        date (datetime): The date of the workout.
        exercises_with_perfs (list[dict]): List of exercises and their performances.
            Each dict should contain:
                - name (str): Exercise name
                - category (str): Exercise category
                - notes (str, optional): Additional notes
                - performances (list[dict]): List of performance entries with:
                    - reps (int): Number of repetitions
                    - weight (float): Weight lifted
                    - rpe (int, optional): Rate of perceived exertion

    Returns:
        int: The ID of the created workout, -1 on failure.
    """


def list_workouts() -> list[dict]:
    """
    Retrieve all workouts with basic information.

    Returns:
        list[dict]: List of workouts, each containing:
            - id (int): Workout ID
            - date (str): Workout date
    """


def get_last_workout_summary() -> Optional[dict]:
    """
    Retrieve the last workout with its exercises and performances.

    Returns:
        Optional[dict]: A dictionary containing:
            - id (int): Workout ID
            - date (str): Workout date
            - exercises (list[dict]): List of exercises with performances
        None if no workout exists or on failure.
    """
