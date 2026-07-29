import json

def is_ip_blacklisted_global(ip):
    """
    Check blockchain log for IP status.
    Returns one of:
    - "BLACKLISTED"
    - "ATTEMPT X/Y (not blacklisted)"
    - "NOT_BLACKLISTED"
    """
    try:
        with open("blockchain_log.json", "r") as f:
            chain = json.load(f)
    except FileNotFoundError:
        return "NOT_BLACKLISTED"

    status = "NOT_BLACKLISTED"
    for block in chain:
        data = block.get("data", {})
        if isinstance(data, dict):
            # Final blacklist event
            if data.get("event") == "BLACKLISTED_IP" and data.get("ip") == ip:
                return "BLACKLISTED"
            # Attempt status recorded in prediction results
            if data.get("source_ip") == ip and "blockchain_status" in data:
                status = data["blockchain_status"]

    return status
