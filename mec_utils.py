
import json


def is_ip_blacklisted_global(ip):

    with open(
        "blockchain_log.json",
        "r"
    ) as f:

        chain = json.load(f)

    for block in chain:

        data = block["data"]

        if (
            isinstance(data, dict)
            and data.get("event") == "BLACKLISTED_IP"
            and data.get("ip") == ip
        ):
            return True

    return False


