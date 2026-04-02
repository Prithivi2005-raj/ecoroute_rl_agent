from client import EcorouteRlAgentEnv
from models import EcorouteRlAgentAction

with EcorouteRlAgentEnv(base_url="http://127.0.0.1:8000").sync() as env:
    print("RESET:")
    reset_result = env.reset()
    print(reset_result)
    print()

    action = EcorouteRlAgentAction(
        transport_mode="cycle",
        traffic_level=4,
        distance_km=6.0
    )

    print("STEP:")
    step_result = env.step(action)
    print(step_result)
    print()

    print("STATE:")
    print(env.state())