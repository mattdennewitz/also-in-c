# also in c

Generates In C-like performances

## Installation

## Configuration

This app uses a TOML configuration file to define performance and player parameters.

### Performance

Performances are made of a number of players interpreting a set number of patterns in unexpected ways. Player interpretations are governed by their types: basic players play as instructed, drone players spend more time on fewer notes, etc. Player behavior may be customized to dictate humanization and the minimum and maximum number of times any pattern may be repeated.

Patterns themselves are sequences of musical notes or rests played for specific intervals at changing velocities. Patterns maybe humanized with "jitter" for imperfection.

Other aspects of performance may also be controlled, such as tempo in beats per minute, musical scale, and the number of patterns to be given to each player.

#### Player types

- `basic`: Plays notes as instructed
- `drone`: Samples first note from pattern, quadruples length of note, fills remaining time with silence
- `dropout`: Randomly (ish) drops notes from a pattern
- `every_other`: Plays every other note in a pattern

## Usage

Example configuration file:

```toml
[performance]
types = ["basic", "basic", "drone"]
scale = "dorian"
patterns = 40
bpm = 120

[performance.players]
jitter = false
pattern_iterations_minimum = 4
pattern_iterations_maximum = 12

[performance.player.basic]
jitter = true
```

This configuration will generate a performance with the following conditions:

- Three players, two basic and one drone, will perform 40 patterns
- The performance will be played at 120 BPM, and in Dorian scale
- By default, all players will not humanize ("jitter") their performance. The "basic" player type overrides this rule, and introduces jitter.
- All players will play each pattern between four and twelve times before proceeding

Run the CLI to create a MIDI file:

```shell
python -m inc -c config.toml midi -o output.mid
```

Required options:

- `-c`: path to TOML performance configuration file
- `-o`: output path for generated MIDI file

You will see a flurry of log output. At the end of execution, you will also have a MIDI file containing your performance. Drag the MIDI file into your DAW of choice, add a few instruments, some reverb, and enjoy!
