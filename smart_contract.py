from blacklist import blacklisted_ips
from blockchain import blockchain


def execute_security_policy(result, ip):

    if result["risk_score"] >= 90:

        blacklist_entry = {
            "ip": ip,
            "prediction": result["prediction"],
            "timestamp": result["timestamp"],
            "risk_score": result["risk_score"]
        }

        if ip not in blacklisted_ips:
         blacklisted_ips[ip] = blacklist_entry

         blockchain.add_block({
            "event": "BLACKLISTED_IP",
            **blacklist_entry
        })

        result["blockchain_status"] = "BLACKLISTED"

    return result