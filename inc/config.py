from typing import List, Literal

import pydantic
from pydantic import Field


class PlayerConfig(pydantic.BaseModel):
    types: List[Literal["basic", "drone", "every_other", "dropout"]]


class PerformanceConfig(pydantic.BaseModel):
    jitter: bool = Field(default=True)  # enable very slight humanization
    patterns: int = Field(default=40)
    pattern_iterations_minimum: int = Field(default=4)
    pattern_iterations_maximum: int = Field(default=12)
    bpm: int = Field(default=120)
    scale: Literal["dorian", "major", "minor"]


class Config(pydantic.BaseModel):
    players: PlayerConfig
    performance: PerformanceConfig
