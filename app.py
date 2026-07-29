from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from predict import predict_attack
from blockchain import blockchain
from blacklist import blacklisted_ips, is_blocked


app = FastAPI()
# Templates
templates = Jinja2Templates(directory="templates")

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
@app.get("/ui", response_class=HTMLResponse)
def home_ui(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="home.html",
    context={}
)
@app.get("/dashboard-ui", response_class=HTMLResponse)
def dashboard_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )

@app.get("/chain")
def get_chain():
    return blockchain.get_chain()

class TrafficData(BaseModel):
    ip: str
    features: list[float]


@app.get("/")
def home():

    return {
        "message":
        "12-Class IDS API Running"
    }


@app.post("/predict")
def predict(data: TrafficData):

    result = predict_attack(
    data.features,
    data.ip
)
    return result
@app.get("/stats")
def stats():

    chain = blockchain.get_chain()

    attack_counts = {}

    for block in chain[1:]:

        prediction = block["data"]["prediction"]

        attack_counts[prediction] = (
            attack_counts.get(prediction, 0) + 1
        )

    return attack_counts
@app.get("/classes")
def classes():
    from predict import encoder
    return encoder.classes_.tolist()
@app.get("/history")
def history():

    chain = blockchain.get_chain()

    history = []

    for block in chain[1:]:

        history.append(
            block["data"]
        )

    return history
@app.get("/latest")
def latest():

    chain = blockchain.get_chain()

    if len(chain) <= 1:
        return {
            "message": "No attacks logged yet"
        }

    return chain[-1]["data"]
@app.get("/critical")
def critical():

    chain = blockchain.get_chain()

    critical_attacks = []

    for block in chain[1:]:

        data = block["data"]

        if data.get("risk_score", 0) >= 90:

            critical_attacks.append(data)

    return critical_attacks
@app.get("/dashboard")
def dashboard():

    chain = blockchain.get_chain()

    total_events = len(chain) - 1

    critical_events = 0

    attack_counts = {}

    for block in chain[1:]:

        data = block["data"]

        prediction = data.get("prediction")

        attack_counts[prediction] = (
            attack_counts.get(prediction, 0) + 1
        )

        if data.get("risk_score", 0) >= 90:
            critical_events += 1

    threat_level = "LOW"

    if critical_events >= 5:
      threat_level = "CRITICAL"
    elif critical_events >= 3:
      threat_level = "HIGH"
    elif critical_events >= 1:
     threat_level = "MEDIUM"

    return {
    "total_events": total_events,
    "critical_events": critical_events,
    "threat_level": threat_level,
    "attack_distribution": attack_counts
}
@app.get("/health")
def health():

    return {
        "status": "UP",
        "model": "Loaded",
        "blockchain_blocks": len(
            blockchain.get_chain()
        ) - 1
    }
@app.get("/blacklist")
def get_blacklist():

    return blacklisted_ips
@app.get("/blocked")
def blocked_entries():

    blocked = {}

    for key, value in blacklisted_ips.items():

        if is_blocked(value):

            blocked[key] = value

    return blocked
