from dataclasses import dataclass


@dataclass
class Genre:
    GenreId: int
    Name: str

    def __str__(self):
        return f"{self.GenreId} - {self.Name}"

    def __hash__(self):
        return hash(self.GenreId)  #chiave priamria

    def __eq__(self, other):
        return self.GenreId == other.GenreId   #verifica se sti oggetti sono uguali