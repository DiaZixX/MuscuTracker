"""
Exercise service module.

Provides high-level operations for managing exercises,
including creation, listing, and performance analysis.
"""

from typing import Optional


def add_exercise(name: str, category: str, notes: Optional[str] = None) -> int:
    """
    Add a new exercise to the database.

    Args:
        name (str): Name of the exercise.
        category (str): Category of the exercise (e.g., push, pull, legs).
        notes (Optional[str]): Additional notes about the exercise.

    Returns:
        int: The ID of the inserted exercise, -1 on failure.
    """


def list_exercises(category: Optional[str] = None) -> list[dict]:
    """
    List all exercises, optionally filtered by category.

    Args:
        category (Optional[str]): Category filter. Defaults to None.

    Returns:
        list[dict]: List of exercises, each containing:
            - id (int): Exercise ID
            - name (str): Exercise name
            - category (str): Exercise category
            - notes (str, optional): Exercise notes
    """


def get_best_lift(name: str) -> Optional[dict]:
    """
    Retrieve the best lift for a given exercise.

    Args:
        name (str): The name of the exercise.

    Returns:
        Optional[dict]: A dictionary containing:
            - weight (float): Maximum weight lifted
            - reps (int): Number of reps at that weight
            - rpe (int, optional): RPE value if available
            - date (str): Date of the performance
        None if not found or on failure.
    """


def get_best_1rm(name: str) -> Optional[float]:
    """
    Retrieve the best estimated 1RM for a given exercise.

    The 1RM is estimated using the Epley formula:
        1RM = weight * (1 + reps / 30)

    Args:
        name (str): The name of the exercise.

    Returns:
        Optional[float]: The best estimated 1RM, or None on failure.
    """
