from __future__ import annotations

import math
import random
from typing import Type, Optional, List

from inc.config import Config
from inc.models import Pattern, Note


class Player:
    """Plays the pattern as given"""

    def __init__(
        self, pattern_iterations_minimum: int = 4, pattern_iterations_maximum: int = 12
    ):
        self.pattern_iterations_minimum = pattern_iterations_minimum
        self.pattern_iterations_maximum = pattern_iterations_maximum

    def humanize(self, pattern: Pattern) -> Pattern:
        """Adds very slight random jitter to the end of each note"""

        for note in pattern.notes:
            jitter = random.random() / 10
            note.length += jitter

        return pattern

    def repeat_count(self):
        """Repeats a pattern a number of times"""

        return random.randint(
            self.pattern_iterations_minimum, self.pattern_iterations_maximum
        )

    def interpret(self, pattern: Pattern, humanize: bool = True) -> Pattern:
        pattern = pattern.copy(deep=True)  # patterns should be immutable-ish
        pattern = self.humanize(pattern)
        return pattern

    def perform(self, patterns: List[Pattern], humanize: bool = True) -> List[Pattern]:
        interpreted_patterns: List[Pattern] = []

        for pattern in patterns:
            for _ in range(self.repeat_count()):
                interpreted = self.interpret(pattern, humanize)
                interpreted_patterns.append(interpreted)

        return interpreted_patterns


class DropoutPlayer(Player):
    """Probabilistically drop notes"""

    def interpret(self, pattern: Pattern, humanize: bool = True) -> Pattern:
        pattern = super().interpret(pattern, humanize)

        length = int(math.ceil(pattern.length()))
        dropout_percentage = random.randint(0, length) / length

        for note in pattern.notes:
            if random.random() < dropout_percentage:
                note.is_rest = True

        return pattern


class EveryOtherNotePlayer(Player):
    """Replaces every other note in the pattern with a rest of equal length to replaced note"""

    def interpret(self, pattern: Pattern, humanize: bool = True) -> Pattern:
        pattern = super().interpret(pattern, humanize)

        for index, note in enumerate(pattern.notes):
            note.is_rest = index % 2 != 0

        return pattern


class DronePlayer(Player):
    """Samples the first note from a pattern, quadruples its length, fills remaining space with rest"""

    def interpret(self, pattern: Pattern, humanize: bool = True) -> Pattern:
        pattern = super().interpret(pattern, humanize)

        note = pattern.notes[0]
        note.length *= 4
        note.midi_note -= 12

        if (filler_length := pattern.length() - note.length) < 0:
            filler_length = 0

        filler = Note(
            is_rest=True,
            length=filler_length,
            midi_note=0,
            name="[rest]",
        )

        pattern.notes = [note, filler]

        return pattern


player_map = {
    "basic": Player,
    "drone": DronePlayer,
    "dropout": DropoutPlayer,
    "every_other": EveryOtherNotePlayer,
}


def get_performer(
    key: str, performer_kwargs: Optional[dict] = None
) -> Type[Player | DronePlayer | DropoutPlayer | EveryOtherNotePlayer]:
    """Creates a performer"""

    if player_type := player_map.get(key) is None:
        raise KeyError(f'Player types are: {"".join(player_map.keys())}')

    if performer_kwargs:
        return player_type(**performer_kwargs)

    return player_type()
