class Exercise:
    """
    Class for a gym exercise

    Give the type and name of the exercise in order to be use in combination with other classes

    Attributes:
        name (str): Name of the exercise
        category (str): Part of the body that the exercise belongs to
        notes (str): Personnal notes
    """

    def __init__(self, name: str, category: str, notes: str = ""):
        """
        Initialize the exercise

        Args:
            name (str): Name of the exercise
            category (str): Part of the body that the exercise belongs to
            notes (str): Personnal notes
        """
        self.name = name
        self.category = category
        self.notes = notes

    def __str__(self):
        """
        Visualization of the object
        """
        return f"[Exercise] {self.name} ({self.category})\n{self.notes}"
