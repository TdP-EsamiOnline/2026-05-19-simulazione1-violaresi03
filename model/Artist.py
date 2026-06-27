from dataclasses import dataclass


@dataclass
class Artist:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.ArtistId} - {self.Name}"

    def __hash__(self):
        return hash(self.ArtistId)  #chiave priamria

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId   #verifica se sti oggetti sono uguali