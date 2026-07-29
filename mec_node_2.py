from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_attack
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from blockchain import blockchain
from mec_utils import is_ip_blacklisted_global
blocked_history = []
app = FastAPI(
    title="MEC Node 2"
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
def mec2_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="mec2.html",
        context={}
    )

NODE_ID = "MEC_2"


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

    # Blockchain blacklist
    if is_ip_blacklisted_global(data.ip):

        blocked_entry = {
            "ip": data.ip,
            "reason": "Blockchain Intelligence"
        }

        blocked_history.append(blocked_entry)

        return {
            "node": NODE_ID,
            "prediction": "BLACKLISTED",
            "severity": "Critical",
            "risk_score": 100,
            "status": "BLOCKED",
            "confidence": 1.0,
            "reason": "Known malicious IP from blockchain"
        }

    result = predict_attack(
        data.features,
        data.ip
    )

    result["node"] = NODE_ID

    # If backend returned an error
    if "error" in result:

        return {
            "prediction": "ERROR",
            "severity": "Unknown",
            "risk_score": 0,
            "status": "ERROR",
            "confidence": 0,
            "reason": result["error"]
        }

    # If already blacklisted
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

    if result["prediction"] != "BENIGN":

        result["status"] = "BLOCKED"

        blocked_history.append({
            "ip": data.ip,
            "reason": result["prediction"]
        })

    else:

        result["status"] = "ALLOWED"

    return result
@app.get("/status")
def status():

    return {
        "node": NODE_ID,
        "status": "CONNECTED",
        "blocked":
            len(blocked_history)
    }


@app.get("/blocked-history")
def history():

    return blocked_history


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

    