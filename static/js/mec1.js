let chart = null;

async function predictMEC1() {

    const ip =
        document.getElementById(
            "ip"
        ).value;

    const features =
        document.getElementById(
            "features"
        )
        .value
        .split(",")
        .map(Number);

    if (features.length !== 78) {

        alert(
            "Enter 78 features"
        );

        return;
    }

    const response =
        await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    ip,
                    features
                })
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "result"
    ).innerHTML = `

        <h4>
            ${data.prediction}
        </h4>

        <p>
            Severity:
            ${data.severity}
        </p>

        <p>
            Risk:
            ${data.risk_score}
        </p>

    `;
}

async function loadMEC1() {

    const status =
        await (
            await fetch(
                "/status"
            )
        ).json();

    document.getElementById(
        "status"
    ).innerText =
        status.status;

    const stats =
        await (
            await fetch(
                "/stats"
            )
        ).json();

    const labels =
        Object.keys(stats);

    const values =
        Object.values(stats);

    if (chart) {

        chart.destroy();

    }

    chart = new Chart(

        document.getElementById(
            "mecChart"
        ),

        {
            type: "pie",

            data: {

                labels,

                datasets: [
                    {
                        data: values
                    }
                ]
            }
        }
    );

    const history =
        await (
            await fetch(
                "/history"
            )
        ).json();

    document.getElementById(
        "history"
    ).innerHTML =

        history.reverse()
        .map(

            item =>

            `<div>

                ${item.prediction}

                -

                ${item.timestamp}

            </div>`

        )

        .join("");
}

setInterval(
    loadMEC1,
    5000
);

window.onload =
    loadMEC1;