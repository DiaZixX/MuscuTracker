import sqlite3 as sql
from datetime import datetime
from typing import Optional


class DBManager:

    def __init__(self, db_path: str):
        self.con = sql.connect(db_path)
        self.cur = self.con.cursor()
        self.con.execute("PRAGMA foreign_keys = ON;")  # Enable the foreign key logic
        self.con.row_factory = sql.Row  # Make the return of a SELECT be a dict instead of tuples

    def __del__(self):
        self.con.close()

    def create_tables(self) -> None:
        try:
            with self.con:
                # Workout table
                self.con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL
                    );
                    """
                )

                # Exercise table
                self.con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        category TEXT NOT NULL,
                        notes TEXT
                    );
                    """
                )

                # Performance table
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
        try:
            str_date = date.strftime("%Y-%m-%d")
            with self.con:
                cursor = self.con.execute("INSERT INTO workouts (date) VALUES (?)", (str_date,))
                return cursor.lastrowid
        except sql.Error as e:
            print(f"[Error] Error while adding a workout : {e}")
            return -1

    def add_exercise(self, name: str, category: str, notes: str) -> int:
        if not name.strip():
            print("[Error] Exercise name cannot be empty")
            return -1

        try:
            if notes == "":
                notes = None
            with self.con:
                cursor = self.con.execute(
                    "INSERT INTO exercises (name, category, notes) VALUES (?, ?, ?)", (name, category, notes)
                )
                return cursor.lastrowid
        except sql.Error as e:
            print(f"[Error] Error while adding an exercise : {e}")
            return -1

    def add_performance(
        self, workout_id: int, exercise_id: int, reps: int, weight: float, rpe: Optional[int] = None
    ) -> int:
        if not reps > 0:
            print("[Error] Number of reps has to be above 0")
            return -1
        if not weight > 0:
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
        try:
            with self.con:
                cursor = self.con.execute("SELECT * FROM workouts ORDER BY date DESC")
                return cursor.fetchall()
        except sql.Error as e:
            print(f"[Error] Error while getting the workouts : {e}")
            return None

    def get_last_workout(self) -> Optional[sql.Row]:
        try:
            with self.con:
                cursor = self.con.execute("SELECT * FROM workouts ORDER BY date DESC LIMIT 1")
                return cursor.fetchone()
        except sql.Error as e:
            print(f"[Error] Error while getting last workout : {e}")
            return None

    def get_exercises(self, category: Optional[str] = None) -> Optional[list[sql.Row]]:
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

    def exercise_history(self, name: str) -> Optional[list[sql.Row]]:
        try:
            with self.con:
                cursor = self.con.execute(
                    """
                    SELECT p.id, w.date, e.name, p.reps, p.weight, p.rpe
                    FROM performances p
                    JOIN workouts w ON p.workout_id = w.id
                    JOIN exercises e ON p.exercise_id = e.id
                    WHERE e.name = ?
                    ORDER BY w.date ASC
                    """,
                    (name,),
                )
                return cursor.fetchall()
        except sql.Error as e:
            print(f"[Error] Error while getting history of an exercise : {e}")
            return None
