# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Ecoroute RL Agent environment.

This environment helps an agent choose the most eco-friendly travel option.
"""

from typing import Dict, Any

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class EcorouteRlAgentAction(Action):
    """Action sent by the agent to choose a travel option."""

    transport_mode: str = Field(
        ..., description="Chosen transport mode: walk, cycle, bus, or car"
    )
    traffic_level: int = Field(
        ..., description="Traffic level from 1 (low) to 10 (high)"
    )
    distance_km: float = Field(
        ..., description="Distance to travel in kilometers"
    )


class EcorouteRlAgentObservation(Observation):
    """Observation returned after evaluating the chosen travel option."""

    suggested_route: str = Field(
        default="", description="Recommended eco-friendly route description"
    )
    estimated_time: float = Field(
        default=0.0, description="Estimated travel time in minutes"
    )
    co2_emission: float = Field(
        default=0.0, description="Estimated CO2 emission in kg"
    )
    eco_score: float = Field(
        default=0.0, description="Environmental friendliness score"
    )
    air_quality_exposure: int = Field(
        default=0, description="Estimated AQI exposure during travel"
    )
    done: bool = Field(
        default=False, description="Whether the episode is finished"
    )
    reward: float = Field(
        default=0.0, description="Reward for the selected travel option"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional debugging or environment metadata"
    )