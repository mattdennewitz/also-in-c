import random
from typing import List

from midiutil import MIDIFile

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


def create_performance(config: Config) -> List:
    # patterns to perform
    patterns: List[Pattern] = [
        generate_pattern() for _ in range(config.performance.patterns)
    ]

    # performers to perform them
    performers = [get_performer(key, config) for key in config.performance.types]

    # each perform gives their interpretation of a pattern
    player_performances = []

    for performer in performers:
        played = performer.perform(patterns)
        player_performances.append(played)

    return player_performances


def render_performance(config: Config, performance: List[List[Pattern]]) -> MIDIFile:
    midi = MIDIFile(len(performance))
    note: Note

    for (track_number, patterns) in enumerate(performance):
        midi.addTempo(track_number, 0, config.performance.bpm)
        time_offset = 0

        for pattern in patterns:
            for note in pattern.notes:
                if not note.is_rest:
                    midi.addNote(
                        track_number,
                        0,
                        note.midi_note,
                        time_offset,
                        note.length,
                        note.random_velocity(),
                    )

                time_offset += note.length

    return midi
