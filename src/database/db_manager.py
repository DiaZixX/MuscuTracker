import sqlite3 as sql
from datetime import datetime
from typing import Optional


class DBManager:
    """
    Database manager class for handling workouts, exercises, and performance data.

    This class provides methods to create tables, insert, query, and manage data
    related to workouts, exercises, and performance tracking.
    """

    def __init__(self, db_name: str = "performance_tracker.db"):
        """
        Initialize the database manager.

        Args:
            db_name (str): The name of the SQLite database file. Defaults to "performance_tracker.db".
        """
        try:
            self.con = sql.connect(db_name)
            self.con.row_factory = sql.Row
            self.cur = self.con.cursor()
            self.con.execute("PRAGMA foreign_keys = ON;")
        except sql.Error as e:
            print(f"[Error] Error while connecting to the database : {e}")

    def __del__(self):
        """
        Destructor method to close the database connection when the object is deleted.
        """
        if hasattr(self, "con"):
            self.con.close()

    def create_tables(self):
        """
        Create the database tables if they do not already exist.

        Tables:
            - workouts
            - exercises
            - performances
        """
        try:
            with self.con:
                self.con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL
                    );
                    """
                )
                self.con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        category TEXT,
                        notes TEXT
                    );
                    """
                )
                self.con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS performances (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        workout_id INTEGER NOT NULL,
                        exercise_id INTEGER NOT NULL,
                        reps INTEGER NOT NULL,
                        weight REAL NOT NULL,
                        rpe REAL,
                        FOREIGN KEY (workout_id) REFERENCES workouts(id),
                        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
                    );
                    """
                )
        except sql.Error as e:
            print(f"[Error] Error while creating tables : {e}")

    def add_workout(self, date: datetime) -> int:
        """
        Add a new workout to the database.

        Args:
            date (datetime): The date of the workout.

        Returns:
            int: The ID of the inserted workout, -1 on failure.
        """
        try:
            with self.con:
                str_date = date.strftime("%Y-%m-%d")
                self.con.execute("INSERT INTO workouts (date) VALUES (?)", (str_date,))
                res = self.con.execute("SELECT last_insert_rowid()")
                return res.fetchone()[0]
        except sql.Error as e:
            print(f"[Error] Error while adding a workout : {e}")
            return -1

    def add_exercise(self, name: str, category: str, notes: str) -> int:
        """
        Add a new exercise to the database.

        Args:
            name (str): The exercise name.
            category (str): The category of the exercise.
            notes (str): Additional notes for the exercise.

        Returns:
            int: The ID of the inserted exercise, -1 on failure.
        """
        try:
            if notes == "":
                notes = None
            with self.con:
                cursor = self.con.execute(
                    "INSERT INTO exercises (name, category, notes) VALUES (?, ?, ?)",
                    (name, category, notes),
                )
                return cursor.lastrowid
        except sql.Error as e:
            print(f"[Error] Error while adding an exercise : {e}")
            return -1

    def add_performance(
        self,
        workout_id: int,
        exercise_id: int,
        reps: int,
        weight: float,
        rpe: Optional[int] = None,
    ) -> int:
        """
        Add a performance entry to the database.

        Args:
            workout_id (int): The workout ID reference.
            exercise_id (int): The exercise ID reference.
            reps (int): Number of repetitions.
            weight (float): Weight lifted.
            rpe (Optional[int]): Rate of perceived exertion, optional.

        Returns:
            int: The ID of the inserted performance, -1 on failure.
        """
        if reps <= 0:
            print("[Error] Number of reps has to be above 0")
            return -1
        if weight <= 0:
            print("[Error] Weight has to be above 0")
            return -1
        if workout_id <= 0 or exercise_id <= 0:
            print("[Error] Invalid workout_id or exercise_id")
            return -1

        try:
            with self.con:
                cursor = self.con.execute(
                    "INSERT INTO performances (workout_id, exercise_id, reps, weight, rpe) VALUES (?, ?, ?, ?, ?)",
                    (workout_id, exercise_id, reps, weight, rpe),
                )
                return cursor.lastrowid
        except sql.Error as e:
            print(f"[Error] Error while adding a performance : {e}")
            return -1

    def get_workouts(self) -> Optional[list[sql.Row]]:
        """
        Retrieve all workouts from the database.

        Returns:
            Optional[list[sql.Row]]: List of workout rows, or None on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute("SELECT * FROM workouts ORDER BY date DESC")
                return cursor.fetchall()
        except sql.Error as e:
            print(f"[Error] Error while listing the workouts : {e}")
            return None

    def get_last_workout(self) -> Optional[sql.Row]:
        """
        Retrieve the most recent workout.

        Returns:
            Optional[sql.Row]: The most recent workout row, or None if none exist or on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute("SELECT * FROM workouts ORDER BY date DESC LIMIT 1")
                return cursor.fetchone()
        except sql.Error as e:
            print(f"[Error] Error while getting last workout : {e}")
            return None

    def get_exercises(self, category: Optional[str] = None) -> Optional[list[sql.Row]]:
        """
        Retrieve all exercises, optionally filtered by category.

        Args:
            category (Optional[str]): Exercise category to filter by. Defaults to None.

        Returns:
            Optional[list[sql.Row]]: List of exercise rows, or None on failure.
        """
        try:
            with self.con:
                if category:
                    cursor = self.con.execute(
                        "SELECT * FROM exercises WHERE category = ? ORDER BY name ASC",
                        (category,),
                    )
                else:
                    cursor = self.con.execute("SELECT * FROM exercises ORDER BY name ASC")
                return cursor.fetchall()
        except sql.Error as e:
            print(f"[Error] Error while listing the exercises : {e}")
            return None

    def get_exercise_category(self, name: str) -> Optional[str]:
        """
        Retrieve the category of an exercise by its name.

        Args:
            name (str): The name of the exercise.

        Returns:
            Optional[str]: The exercise category, or None if not found or on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute(
                    "SELECT category FROM exercises WHERE name = ?",
                    (name,),
                )
                row = cursor.fetchone()
                return row["category"] if row else None
        except sql.Error as e:
            print(f"[Error] Error while getting exercise category : {e}")
            return None

    def get_exercise_history(self, name: str) -> Optional[list[sql.Row]]:
        """
        Retrieve the performance history of a given exercise by name.

        Args:
            name (str): The name of the exercise.

        Returns:
            Optional[list[sql.Row]]: List of performance rows with workout info, or None on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute(
                    """
                    SELECT p.id, w.date, e.name, p.reps, p.weight, p.rpe
                    FROM performances p
                    JOIN workouts w ON p.workout_id = w.id
                    JOIN exercises e ON p.exercise_id = e.id
                    WHERE e.name = ?
                    ORDER BY w.date ASC;
                    """,
                    (name,),
                )
                return cursor.fetchall()
        except sql.Error as e:
            print(f"[Error] Error while getting exercise history : {e}")
            return None

    def get_exercise_best_lift(self, name: str) -> Optional[sql.Row]:
        """
        Retrieve the best lift for a given exercise, defined as the heaviest weight,
        and associated reps (and RPE if available).

        Args:
            name (str): The name of the exercise.

        Returns:
            Optional[sql.Row]: A row containing weight, reps, rpe, and workout date, or None on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute(
                    """
                    SELECT p.weight, p.reps, p.rpe, w.date
                    FROM performances p
                    JOIN exercises e ON p.exercise_id = e.id
                    JOIN workouts w ON p.workout_id = w.id
                    WHERE e.name = ?
                    ORDER BY p.weight DESC, p.reps DESC
                    LIMIT 1;
                    """,
                    (name,),
                )
                return cursor.fetchone()
        except sql.Error as e:
            print(f"[Error] Error while getting best lift : {e}")
            return None

    def get_exercise_best_1rm(self, name: str) -> Optional[float]:
        """
        Retrieve the best estimated 1RM for a given exercise.

        The 1RM is estimated using the Epley formula:
            1RM = weight * (1 + reps / 30)

        Args:
            name (str): The name of the exercise.

        Returns:
            Optional[float]: The best estimated 1RM value, or None on failure.
        """
        try:
            with self.con:
                cursor = self.con.execute(
                    """
                    SELECT MAX(p.weight * (1 + p.reps / 30.0)) AS estimated_1RM
                    FROM performances p
                    JOIN exercises e ON p.exercise_id = e.id
                    WHERE e.name = ?;
                    """,
                    (name,),
                )
                row = cursor.fetchone()
                return row["estimated_1RM"] if row else None
        except sql.Error as e:
            print(f"[Error] Error while getting best estimated 1RM : {e}")
            return None
