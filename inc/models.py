import random
from typing import List

import pydantic
from mingus.core import scales
from mingus.core.notes import note_to_int


class Note(pydantic.BaseModel):
    """A specific note or rest played for an amount of time at a certain velocity"""

    name: str  # e.g., "C" or "G"
    midi_note: int
    length: float
    is_rest: bool = False

    @classmethod
    def create(cls, length: float) -> "Note":
        if random.random() < 0.1:
            return cls(name="[rest]", midi_note=0, length=length, is_rest=True)

        name = random.choice(scales.Dorian("C").ascending())
        base_note_number = note_to_int(name)
        note_offset = random.choice([-12, 0, 12])

        # calculate midi note from C with offsets
        midi_note_offset = base_note_number + note_offset
        midi_note = 60 + midi_note_offset

        return cls(name=name, midi_note=midi_note, length=length)

    def random_velocity(self):
        return random.randint(80, 127)


class Pattern(pydantic.BaseModel):
    """A collection of notes"""

    notes: List[Note] = pydantic.Field(default_factory=list)

    def length(self):
        return sum([note.length for note in self.notes])
