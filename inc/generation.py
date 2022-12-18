import logging
import random
from typing import List

from midiutil import MIDIFile

from inc.config import Config
from inc.models import Pattern, Note
from inc.notes import NOTE_HALF, DOTTED, NOTE_WHOLE, NOTE_LENGTHS
from inc.players import get_performer, Player


log = logging.getLogger("alsoinc.generation")


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

    log.info("Generating pattern of %s width", width_remaining)

    while 1:
        note_length = random.choices(
            NOTE_LENGTHS, weights=[random.random() for _ in range(len(NOTE_LENGTHS))]
        )[0]

        # would adding this note exceed the remaining size?
        would_exceed_max_length = (pattern.length() + note_length) > width_remaining

        if len(pattern.notes) and would_exceed_max_length:
            break
        elif not pattern.notes and would_exceed_max_length:
            continue

        note = Note.create(note_length)
        pattern.notes.append(note)
        log.debug("Added note %s", note)

    return pattern


def create_performance(config: Config) -> List:
    # patterns to perform
    patterns: List[Pattern] = [
        generate_pattern() for _ in range(config.performance.patterns)
    ]

    # performers to perform them
    performers = [get_performer(key, config) for key in config.performance.types]

    # each perform gives their interpretation of a pattern
    player_performances: List[List[Pattern]] = []

    for performer in performers:
        played = performer.perform(patterns)
        player_performances.append(played)

    # all musicians should converge on the final pattern.
    # detect the longest performance, then pad all others to reach the same length.
    longest_performance_length = len(max(player_performances, key=len))

    log.info("Longest performance length: %s patterns", longest_performance_length)

    for performer, played in zip(performers, player_performances):
        performance_length = len(played)

        if performance_length < longest_performance_length:
            # repeat the pattern until all patterns match
            diff = longest_performance_length - performance_length

            log.info(
                "Padding performance from %s to %s patterns",
                performance_length,
                longest_performance_length,
            )

            final_repeating_patterns = [patterns[-1]] * diff
            played.extend(performer.perform(final_repeating_patterns, repeat_count=1))

        log.info("Player will perform %s patterns", len(played))

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
