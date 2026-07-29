async function predictIDS() {

    const ip = document
        .getElementById("ip")
        .value;

    const features = document
        .getElementById("features")
        .value
        .split(",")
        .map(Number);

    if (features.length !== 78) {

        alert(
            "Please enter exactly 78 features."
        );

        return;
    }

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    ip: ip,
                    features: features
                })
            }
        );

        const data =
            await response.json();

        document.getElementById(
            "result"
        ).innerHTML = `

            <p><b>Prediction:</b>
            ${data.prediction}</p>

            <p><b>Confidence:</b>
            ${data.confidence}</p>

            <p><b>Severity:</b>
            ${data.severity}</p>

            <p><b>Risk Score:</b>
            ${data.risk_score}</p>

            <p><b>Alert:</b>
            ${data.alert}</p>

        `;

    }

    catch {

        alert(
            "Prediction failed."
        );

    }

}

let chart = null;

async function loadDashboard() {

    const dashboardResponse =
        await fetch("/dashboard");

    const dashboard =
        await dashboardResponse.json();

    /* Threat Level */

    const threatElement =
        document.getElementById(
            "threatLevel"
        );

    threatElement.innerText =
        dashboard.threat_level;

    const threatColors = {
        "LOW": "#2ecc71",
        "MEDIUM": "#f1c40f",
        "HIGH": "#e67e22",
        "CRITICAL": "#e74c3c"
    };

    threatElement.style.color =
        threatColors[
            dashboard.threat_level
        ];

    /* Chart */

    const labels =
        Object.keys(
            dashboard.attack_distribution
        );

    const values =
        Object.values(
            dashboard.attack_distribution
        );

    const colorMap = {
        "BENIGN": "#2ecc71",
        "Bot": "#f39c12",
        "DDoS": "#e74c3c",
        "DoS GoldenEye": "#9b59b6",
        "DoS Hulk": "#c0392b",
        "DoS Slowhttptest": "#16a085",
        "DoS slowloris": "#1abc9c",
        "FTP-Patator": "#3498db",
        "SSH-Patator": "#2980b9",
        "PortScan": "#f1c40f",
        "Web Attack � Brute Force": "#e67e22",
        "OTHER_ATTACK": "#7f8c8d"
    };

    const colors =
        labels.map(
            label =>
                colorMap[label] || "#95a5a6"
        );

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(
        document.getElementById(
            "attackChart"
        ),
        {
            type: "bar",

            data: {
                labels: labels,

                datasets: [
                    {
                        label: "Attacks",
                        data: values,
                        backgroundColor: colors
                    }
                ]
            }
        }
    );

    /* Blockchain */

    const chainResponse =
        await fetch("/chain");

    const chain =
        await chainResponse.json();

    let timelineHTML = "";

    chain.slice(-5).reverse().forEach(
        block => {

            timelineHTML += `
                <div class="mb-2">

                    <strong>
                        Block ${block.index}
                    </strong>

                    <br>

                    ${
                        block.data.prediction ||
                        block.data
                    }

                </div>
            `;
        }
    );

    document.getElementById(
        "timeline"
    ).innerHTML =
        timelineHTML;

    /* Blacklist */

    const blacklistResponse =
        await fetch("/blacklist");

    const blacklist =
        await blacklistResponse.json();

    let blacklistHTML = "";

    Object.entries(
        blacklist
    ).forEach(
        ([ip, info]) => {

            blacklistHTML += `
                <div class="mb-2">

                    ${ip}

                    -

                    ${info.prediction}

                </div>
            `;
        }
    );

    if (!blacklistHTML) {

        blacklistHTML =
            "No blocked IPs";
    }

    document.getElementById(
        "blacklist"
    ).innerHTML =
        blacklistHTML;
}

setInterval(
    loadDashboard,
    5000
);

window.onload =
    loadDashboard;