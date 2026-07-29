async function predictMEC2() {

    const ip = document
        .getElementById("ip")
        .value
        .trim();

    const features = document
        .getElementById("features")
        .value
        .split(",")
        .map(x => parseFloat(x.trim()))
        .filter(x => !isNaN(x));

    if (!ip) {

        alert("Please enter an IP address.");

        return;
    }

    if (features.length !== 78) {

        alert(
            `Exactly 78 features are required. Found ${features.length}.`
        );

        return;
    }

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    ip: ip,
                    features: features
                })
            }
        );

        const data = await response.json();

        console.log("MEC2 Response:", data);

        const prediction =
            data.prediction || "Unknown";

        const severity =
            data.severity || "N/A";

        const risk =
            data.risk_score ?? "N/A";

        const status =
            data.status || "Unknown";

        const confidence =
            data.confidence ?? "N/A";

        const reason =
            data.reason ||
            data.message ||
            "";

        let resultClass = "text-success";

        if (
            status === "BLOCKED" ||
            prediction !== "BENIGN"
        ) {

            resultClass = "text-danger";
        }

        document.getElementById(
            "result"
        ).innerHTML = `

            <div class="${resultClass}">

                <h3>
                    ${prediction}
                </h3>

                <p>
                    <strong>Severity:</strong>
                    ${severity}
                </p>

                <p>
                    <strong>Risk:</strong>
                    ${risk}
                </p>

                <p>
                    <strong>Status:</strong>
                    ${status}
                </p>

                <p>
                    <strong>Confidence:</strong>
                    ${confidence}
                </p>

                ${
                    reason
                    ?
                    `<p>
                        <strong>Reason:</strong>
                        ${reason}
                    </p>`
                    :
                    ""
                }

            </div>

        `;

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "result"
        ).innerHTML = `

            <div class="text-danger">

                <h3>
                    Prediction Failed
                </h3>

                <p>
                    Unable to contact MEC2.
                </p>

            </div>

        `;
    }
}


async function loadMEC2() {

    try {

        /* Status */

        const status =
            await (
                await fetch("/status")
            ).json();

        document.getElementById(
            "status"
        ).innerText =
            status.status;


        /* Shared Threats */

        const sharedResponse =
            await fetch("/shared-threats");

        const shared =
            await sharedResponse.json();

        if (
            !shared ||
            shared.length === 0
        ) {

            document.getElementById(
                "shared"
            ).innerHTML =
                "No shared threats.";

        }

        else {

            document.getElementById(
                "shared"
            ).innerHTML =

                shared
                .slice(-5)
                .reverse()
                .map(threat => `

                    <div>

                        ${threat.ip || "Unknown IP"}

                        -

                        ${threat.prediction ||
                          threat.event ||
                          "Unknown Threat"}

                        (Risk:
                        ${threat.risk_score || "N/A"})

                    </div>

                `)

                .join("");
        }


        /* Blocked Requests */

        const blockedResponse =
            await fetch("/blocked-history");

        const blocked =
            await blockedResponse.json();

        if (
            !blocked ||
            blocked.length === 0
        ) {

            document.getElementById(
                "blocked"
            ).innerHTML =
                "No blocked requests.";

        }

        else {

            document.getElementById(
                "blocked"
            ).innerHTML =

                blocked
                .slice()
                .reverse()
                .map(item => `

                    <div>

                        ${item.ip}

                        -

                        ${item.reason}

                    </div>

                `)

                .join("");
        }

    }

    catch (error) {

        console.error(
            "MEC2 Dashboard Error:",
            error
        );

        document.getElementById(
            "shared"
        ).innerHTML =
            "Unable to load threats.";

        document.getElementById(
            "blocked"
        ).innerHTML =
            "Unable to load blocked requests.";
    }
}


setInterval(
    loadMEC2,
    5000
);

window.onload =
    loadMEC2;