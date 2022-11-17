import random
from typing import List

from inc.config import Config
from inc.models import Pattern, Note
from inc.notes import NOTE_HALF, DOTTED, NOTE_WHOLE, NOTE_LENGTHS
from inc.players import get_performer, Player


def generate_pattern():
    pattern = Pattern()

    width_remaining = random.choice(
        [
            NOTE_HALF,
            NOTE_HALF * DOTTED,
            NOTE_WHOLE,
            NOTE_WHOLE * DOTTED,
            NOTE_WHOLE * 2,
            NOTE_WHOLE * DOTTED * 2,
        ]
    )

    # randomly pack boxes full of notes
    while 1:
        note_length = random.choices(
            NOTE_LENGTHS, weights=[random.random() for _ in range(len(NOTE_LENGTHS))]
        )[0]

        if len(pattern.notes) and (pattern.length() + note_length) > width_remaining:
            break

        pattern.notes.append(Note.create(note_length))

    return pattern


def create_performance(pattern_count: int, player_types: List[str]):
    # patterns to perform
    patterns: List[Pattern] = [generate_pattern() for _ in range(pattern_count)]

    # performers to perform them
    performers = [get_performer(key) for key in player_types]

    # each perform gives their interpretation of a pattern
    for performer in performers:
        played = performer.perform(patterns)
