import torch
import numpy as np
import joblib
from datetime import datetime
from smart_contract import execute_security_policy
from blockchain import blockchain
from blacklist import blacklisted_ips, is_blocked
from model import IDSDetector


# Load model
model = IDSDetector()

model.load_state_dict(
    torch.load(
        "ids_model.pth",
        map_location=torch.device("cpu")
    )
)

model.eval()


# Load scaler and encoder
scaler = joblib.load(
    "multiclass_scaler.pkl"
)

encoder = joblib.load(
    "label_encoder.pkl"
)

print("Available Classes:")
print(encoder.classes_)


def predict_attack(features, ip):

    # Check local blacklist first
    if ip in blacklisted_ips:

        if is_blocked(
            blacklisted_ips[ip]
        ):

            return {
                "source_ip": ip,
                "status": "BLOCKED",
                "message": "IP is blacklisted"
            }

    # Validate feature count
    if len(features) != 78:

        return {
            "error": f"Expected 78 features, got {len(features)}"
        }

    # Preprocess input
    features = np.array(
        features,
        dtype=np.float32
    ).reshape(1, -1)

    features = scaler.transform(
        features
    )

    tensor = torch.tensor(
        features,
        dtype=torch.float32
    )

    # Prediction
    with torch.no_grad():

        outputs = model(tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted = torch.max(
            probabilities,
            1
        )

        class_name = encoder.inverse_transform(
            [predicted.item()]
        )[0]

        # Remove hidden spaces
        class_name = class_name.strip()

        print(
            "Predicted Index:",
            predicted.item()
        )

        print(
            "Predicted Class:",
            repr(class_name)
        )

    # Severity map
    severity_map = {
        "BENIGN": "Low",

        "PortScan": "Medium",

        "Bot": "Medium",

        "DDoS": "High",

        "DoS Hulk": "High",
        "DoS GoldenEye": "High",
        "DoS Slowhttptest": "High",
        "DoS slowloris": "High",

        "FTP-Patator": "High",
        "FTP Patator": "High",

        "SSH-Patator": "High",
        "SSH Patator": "High",

        "Web Attack – Brute Force": "High",
        "Web Attack � Brute Force": "High",

        "OTHER_ATTACK": "High"
    }

    # Risk map
    risk_map = {
        "BENIGN": 0,

        "PortScan": 75,

        "Bot": 80,

        "DDoS": 100,

        "DoS Hulk": 95,
        "DoS GoldenEye": 95,

        "DoS Slowhttptest": 90,
        "DoS slowloris": 90,

        "FTP-Patator": 90,
        "FTP Patator": 90,

        "SSH-Patator": 90,
        "SSH Patator": 90,

        "Web Attack – Brute Force": 90,
        "Web Attack � Brute Force": 90,

        "OTHER_ATTACK": 90
    }

    # Result
    result = {
        "source_ip": ip,

        "prediction": class_name,

        "severity": severity_map.get(
            class_name,
            "Unknown"
        ),

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "risk_score": risk_map.get(
            class_name,
            50
        ),

        "confidence": round(
            confidence.item(),
            4
        )
    }

    # Execute smart contract
    result = execute_security_policy(
        result,
        ip
    )

    # Alert generation
    if result["risk_score"] >= 90:

        result["alert"] = (
            "CRITICAL ATTACK DETECTED"
        )

    elif result["risk_score"] >= 70:

        result["alert"] = (
            "HIGH RISK ATTACK"
        )

    elif result["risk_score"] >= 50:

        result["alert"] = (
            "MEDIUM RISK"
        )

    else:

        result["alert"] = (
            "NORMAL TRAFFIC"
        )

    print(
        "BLOCK ADDED:",
        result
    )

    # Log attacks to blockchain
    if (
        result["prediction"] != "BENIGN"
        and result["prediction"] != "BLACKLISTED"
    ):

        blockchain.add_block(
            result
        )

    return result