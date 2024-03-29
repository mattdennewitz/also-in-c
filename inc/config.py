from typing import List, Literal, Dict, Optional, Any

import pydantic
import pydash
from pydantic import Field


class PlayerConfig(pydantic.BaseModel):
    pattern_iterations_minimum: Optional[int]
    pattern_iterations_maximum: Optional[int]
    jitter: Optional[bool]


class PerformanceConfig(pydantic.BaseModel):
    types: List[Literal["basic", "drone", "every_other", "dropout"]]
    scale: Literal["dorian", "major", "minor"]
    patterns: int = Field(default=40)
    bpm: int = Field(default=120)

    base_player_rules: PlayerConfig
    player_specific_rules: Dict[str, PlayerConfig]

    def player_rules(self, key: Optional[str] = None) -> Dict[str, Any]:
        performance_config = pydash.get(self, "base_player_rules", {})
        player_performance_config = pydash.get(self, f"player_specific_rules.{key}", {})

        # flatten to dicts from pydantic structures
        performance_config = performance_config.dict(exclude_none=True)

        if not isinstance(player_performance_config, dict):
            player_performance_config = player_performance_config.dict(
                exclude_none=True
            )

        # merge player-specific performance rules with overall performance rules
        merged = pydash.merge(dict(), performance_config, player_performance_config)

        return merged


class Config(pydantic.BaseModel):
    performance: PerformanceConfig
