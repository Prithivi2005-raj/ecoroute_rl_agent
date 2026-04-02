from server.ecoroute_rl_agent_environment import EcorouteRlAgentEnvironment
from models import EcorouteRlAgentAction

env = EcorouteRlAgentEnvironment()

print("RESET:")
reset_obs = env.reset()
print(reset_obs)
print()

action = EcorouteRlAgentAction(
    transport_mode="cycle",
    traffic_level=4,
    distance_km=6.0
)

print("STEP:")
step_obs = env.step(action)
print(step_obs)
print()

print("STATE:")
print(env.state)