import logging

import click
import toml
from rich.logging import RichHandler

from inc.config import Config
from inc.generation import create_performance, render_performance


logging.basicConfig(
    level="DEBUG",
    format="[%(module)s.%(funcName)s] %(message)s",
    handlers=[RichHandler()],
)

log = logging.getLogger("alsoinc.cli")


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

    log.info("Creating performance with configuration: %s", parsed)

    context.obj["config"] = Config(**parsed)


@cli.command()
@click.option("-o", "output", type=click.File("wb"), required=True)
@click.pass_context
def midi(context, output):
    # create patterns
    config: Config = context.obj["config"]
    performance = create_performance(config)

    log.info("Writing to %s", output.name)

    midi = render_performance(config, performance)
    midi.writeFile(output)
