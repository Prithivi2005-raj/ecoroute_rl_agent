# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Ecoroute RL Agent Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

try:
    from models import EcorouteRlAgentAction, EcorouteRlAgentObservation
except ImportError:
    from .models import EcorouteRlAgentAction, EcorouteRlAgentObservation


class EcorouteRlAgentEnv(
    EnvClient[EcorouteRlAgentAction, EcorouteRlAgentObservation, State]
):
    """
    Client for the Ecoroute RL Agent Environment.
    """

    def _step_payload(self, action: EcorouteRlAgentAction) -> Dict:
        """
        Convert EcorouteRlAgentAction to JSON payload for step request.
        """
        return {
            "transport_mode": action.transport_mode,
            "traffic_level": action.traffic_level,
            "distance_km": action.distance_km,
        }

    def _parse_result(self, payload: Dict) -> StepResult[EcorouteRlAgentObservation]:
        """
        Parse server response into StepResult[EcorouteRlAgentObservation].
        """
        obs_data = payload.get("observation", payload)

        observation = EcorouteRlAgentObservation(
            suggested_route=obs_data.get("suggested_route", ""),
            estimated_time=obs_data.get("estimated_time", 0.0),
            co2_emission=obs_data.get("co2_emission", 0.0),
            eco_score=obs_data.get("eco_score", 0.0),
            air_quality_exposure=obs_data.get("air_quality_exposure", 0),
            done=payload.get("done", obs_data.get("done", False)),
            reward=payload.get("reward", obs_data.get("reward", 0.0)),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=observation.reward,
            done=observation.done,
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )