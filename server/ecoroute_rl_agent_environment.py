# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
EcoRoute RL Agent Environment Implementation.

A reinforcement learning style environment where an agent selects a travel mode
for a given trip and receives feedback based on:
- travel time
- CO2 emissions
- eco-friendliness
- air quality exposure

This environment simulates sustainable urban mobility decisions.
"""

from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import EcorouteRlAgentAction, EcorouteRlAgentObservation
except ImportError:
    from models import EcorouteRlAgentAction, EcorouteRlAgentObservation


class EcorouteRlAgentEnvironment(Environment):
    """
    EcoRoute RL environment for sustainable transport selection.

    The agent provides:
    - transport_mode
    - traffic_level
    - distance_km

    The environment returns:
    - suggested_route
    - estimated_time
    - co2_emission
    - eco_score
    - air_quality_exposure
    - reward
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the EcoRoute RL environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count = 0
        self._max_steps = 10

    def reset(self) -> EcorouteRlAgentObservation:
        """
        Reset the environment to start a new episode.

        Returns:
            Initial observation indicating the environment is ready.
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count += 1

        return EcorouteRlAgentObservation(
            suggested_route="EcoRoute ready. Choose a transport mode for the next trip.",
            estimated_time=0.0,
            co2_emission=0.0,
            eco_score=0.0,
            air_quality_exposure=0,
            done=False,
            reward=0.0,
            metadata={
                "reset_count": self._reset_count,
                "max_steps": self._max_steps,
                "supported_modes": ["walk", "cycle", "bus", "car", "metro"],
            },
        )

    def step(self, action: EcorouteRlAgentAction) -> EcorouteRlAgentObservation:  # type: ignore[override]
        """
        Execute one environment step based on the chosen travel option.

        Args:
            action: EcorouteRlAgentAction containing:
                - transport_mode
                - traffic_level
                - distance_km

        Returns:
            EcorouteRlAgentObservation with route metrics and reward.
        """
        self._state.step_count += 1

        transport = action.transport_mode.lower().strip()
        traffic = max(1, min(action.traffic_level, 10))  # clamp to 1..10
        distance = max(0.5, action.distance_km)  # minimum 0.5 km

        # Base values per transport mode
        if transport == "walk":
            speed_kmph = 5
            co2_per_km = 0.0
            eco_base = 10.0
            aqi_base = 18
            route = "Walking route through shaded low-traffic local streets"

        elif transport == "cycle":
            speed_kmph = 15
            co2_per_km = 0.0
            eco_base = 9.0
            aqi_base = 24
            route = "Dedicated cycling lane route avoiding major congestion points"

        elif transport == "bus":
            speed_kmph = 24
            co2_per_km = 0.08
            eco_base = 7.2
            aqi_base = 34
            route = "Public bus route with moderate congestion and shared emissions"

        elif transport == "metro":
            speed_kmph = 40
            co2_per_km = 0.03
            eco_base = 8.5
            aqi_base = 20
            route = "Metro route with low emissions and minimal traffic interference"

        elif transport == "car":
            speed_kmph = 35
            co2_per_km = 0.25
            eco_base = 3.0
            aqi_base = 50
            route = "Private car route optimized for speed but high carbon impact"

        else:
            done = self._state.step_count >= self._max_steps
            return EcorouteRlAgentObservation(
                suggested_route="Invalid transport mode. Use walk, cycle, bus, car, or metro.",
                estimated_time=0.0,
                co2_emission=0.0,
                eco_score=0.0,
                air_quality_exposure=0,
                done=done,
                reward=-5.0,
                metadata={
                    "invalid_transport_mode": action.transport_mode,
                    "valid_modes": ["walk", "cycle", "bus", "car", "metro"],
                    "step": self._state.step_count,
                },
            )

        # Traffic reduces effective speed
        traffic_factor = 1 - (traffic * 0.05)
        effective_speed = max(2.0, speed_kmph * traffic_factor)

        # Estimated travel time (minutes)
        estimated_time = (distance / effective_speed) * 60

        # CO2 emission (kg)
        co2_emission = distance * co2_per_km

        # Air quality exposure
        air_quality_exposure = aqi_base + (traffic * 3)

        # Eco score
        eco_score = max(0.0, eco_base - (traffic * 0.2))

        # Reward design
        # - reward eco-friendly choices
        # - penalize emissions
        # - slightly penalize longer time
        # - slightly penalize pollution exposure
        reward = (
            (eco_score * 2.2)
            - (co2_emission * 12.0)
            - (estimated_time * 0.04)
            - (air_quality_exposure * 0.03)
        )

        # End episode after max steps
        done = self._state.step_count >= self._max_steps

        return EcorouteRlAgentObservation(
            suggested_route=route,
            estimated_time=round(estimated_time, 2),
            co2_emission=round(co2_emission, 3),
            eco_score=round(eco_score, 2),
            air_quality_exposure=air_quality_exposure,
            done=done,
            reward=round(reward, 2),
            metadata={
                "transport_mode": transport,
                "traffic_level": traffic,
                "distance_km": distance,
                "effective_speed_kmph": round(effective_speed, 2),
                "step": self._state.step_count,
                "max_steps": self._max_steps,
            },
        )

    @property
    def state(self) -> State:
        """
        Get the current environment state.

        Returns:
            Current State with episode_id and step_count.
        """
        return self._state