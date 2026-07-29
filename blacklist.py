from datetime import datetime
from blockchain import blockchain


def restore_blacklist():

    chain = blockchain.get_chain()

    for block in chain:

        data = block["data"]

        if (
            isinstance(data, dict)
            and data.get("event") == "BLACKLISTED_IP"
        ):

            blacklisted_ips[
                data["ip"]
            ] = {
                "prediction": data["prediction"],
                "timestamp": data["timestamp"],
                "risk_score": data["risk_score"]
            }

    print(
        f"Restored {len(blacklisted_ips)} blacklisted IPs"
    )
blacklisted_ips = {}

BLOCK_THRESHOLD = 300
def is_blocked(entry):

    timestamp = datetime.strptime(
        entry["timestamp"],
        "%Y-%m-%d %H:%M:%S"
    )

    elapsed = (
        datetime.now() - timestamp
    ).total_seconds()

    return elapsed < BLOCK_THRESHOLD
restore_blacklist()