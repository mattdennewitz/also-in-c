from typing import List

import click
import toml

from inc.config import Config
from inc.generation import generate_pattern, create_performance
from inc.models import Pattern
from inc.players import get_performer


@click.group()
@click.option("-c", "config", type=click.File("r"), required=True)
@click.pass_context
def cli(context, config):
    parsed = toml.load(config)
    context.obj["config"] = Config(**parsed)


@cli.command()
@click.option("-o", "output", type=click.File("wb"), required=True)
@click.pass_context
def midi(context, output):
    # create patterns
    config: Config = context.obj["config"]
    performance = create_performance(
        pattern_count=config.performance.patterns, players=config.players.types
    )
