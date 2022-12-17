from typing import List

import click
import pydash
import toml

from inc.config import Config
from inc.generation import create_performance, render_performance


@click.group()
@click.option("-c", "config", type=click.File("r"), required=True)
@click.pass_context
def cli(context, config):
    parsed = toml.load(config)

    parsed["performance"]["base_player_rules"] = parsed["performance"].pop(
        "players", {}
    )
    parsed["performance"]["player_specific_rules"] = parsed["performance"].pop(
        "player", {}
    )

    context.obj["config"] = Config(**parsed)


@cli.command()
@click.option("-o", "output", type=click.File("wb"), required=True)
@click.pass_context
def midi(context, output):
    # create patterns
    config: Config = context.obj["config"]
    performance = create_performance(config)

    midi = render_performance(config, performance)
    midi.writeFile(output)
