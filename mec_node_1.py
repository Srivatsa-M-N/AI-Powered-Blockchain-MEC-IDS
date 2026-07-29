from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from predict import predict_attack
from blockchain import blockchain
from mec_utils import is_ip_blacklisted_global

prediction_history = []

app = FastAPI(
    title="MEC Node 1"
)

templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/ui", response_class=HTMLResponse)
def mec1_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="mec1.html",
        context={}
    )


NODE_ID = "MEC_1"


class TrafficData(BaseModel):
    ip: str
    features: list[float]


@app.get("/")
def home():

    return {
        "node": NODE_ID,
        "status": "ACTIVE"
    }


@app.post("/predict")
def predict(data: TrafficData):

    # Check shared blockchain blacklist
    if is_ip_blacklisted_global(data.ip):

        blocked_entry = {
            "ip": data.ip,
            "reason": "Blockchain Intelligence"
        }

        prediction_history.append(blocked_entry)

        return {
            "node": NODE_ID,
            "prediction": "BLACKLISTED",
            "severity": "Critical",
            "risk_score": 100,
            "status": "BLOCKED",
            "confidence": 1.0,
            "reason": "Known malicious IP from blockchain"
        }

    # Local DNN prediction
    result = predict_attack(
        data.features,
        data.ip
    )

    result["node"] = NODE_ID

    # Handle backend errors
    if "error" in result:

        return {
            "prediction": "ERROR",
            "severity": "Unknown",
            "risk_score": 0,
            "status": "ERROR",
            "confidence": 0,
            "reason": result["error"]
        }

    # Handle locally blacklisted IPs
    if result.get("status") == "BLOCKED":

        return {
            "prediction": "BLACKLISTED",
            "severity": "Critical",
            "risk_score": 100,
            "status": "BLOCKED",
            "confidence": 1.0,
            "reason": result.get(
                "message",
                "IP is blacklisted"
            )
        }

    # Decide MEC status
    if result["prediction"] != "BENIGN":

        result["status"] = "BLOCKED"

    else:

        result["status"] = "ALLOWED"

    prediction_history.append(result)

    if len(prediction_history) > 10:

        prediction_history.pop(0)

    return result


@app.get("/stats")
def mec1_stats():

    counts = {}

    for item in prediction_history:

        prediction = item.get(
            "prediction",
            "UNKNOWN"
        )

        counts[prediction] = (
            counts.get(prediction, 0) + 1
        )

    return counts


@app.get("/history")
def mec1_history():

    return prediction_history


@app.get("/shared-threats")
def shared_threats():

    threats = []

    chain = blockchain.get_chain()

    for block in chain:

        data = block["data"]

        if (
            isinstance(data, dict)
            and data.get("event")
            == "BLACKLISTED_IP"
        ):

            threats.append(data)

    return threats


@app.get("/status")
def mec1_status():

    return {
        "node": NODE_ID,
        "status": "CONNECTED",
        "processed": len(
            prediction_history
        )
    }