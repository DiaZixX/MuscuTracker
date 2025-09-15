class Exercise:
    def __init__(self, name: str, category: str, notes: str = ""):
        self.name = name
        self.category = category
        self.notes = notes

    def __str__(self):
        return f"[Exercise] {self.name} ({self.category})\n{self.notes}"
