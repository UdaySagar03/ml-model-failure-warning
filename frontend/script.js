const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");

const statusMessage = document.getElementById("status-message");
const predictionResults = document.getElementById("prediction-results");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    predictButton.disabled = true;
    statusMessage.textContent = "Analyzing machine readings...";
    predictionResults.hidden = true;

    const reading = {
        machine_type: document.getElementById("machine-type").value,
        air_temperature: Number(
            document.getElementById("air-temperature").value
        ),
        process_temperature: Number(
            document.getElementById("process-temperature").value
        ),
        rotational_speed: Number(
            document.getElementById("rotational-speed").value
        ),
        torque: Number(
            document.getElementById("torque").value
        ),
        tool_wear: Number(
            document.getElementById("tool-wear").value
        )
    };

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(reading)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "The prediction request failed."
            );
        }

        const predictionStatus =
            document.getElementById("prediction-status");

        const failureProbability =
            document.getElementById("failure-probability");

        const riskLevel =
            document.getElementById("risk-level");

        const predictionMessage =
            document.getElementById("prediction-message");

        predictionStatus.textContent =
            result.predicted_failure === 1
                ? "Potential Failure"
                : "No Failure Predicted";

        predictionStatus.dataset.status =
            result.predicted_failure === 1
                ? "failure"
                : "normal";

        failureProbability.textContent =
            `${result.failure_probability_percent}%`;
        const probabilityFill = document.getElementById("probability-fill");
        const emptyResults = document.getElementById("empty-results");

        probabilityFill.style.width =
            `${Math.max(0, Math.min(100, result.failure_probability_percent))}%`;

        emptyResults.hidden = true;

        riskLevel.textContent = result.risk_level;
        riskLevel.dataset.risk = result.risk_level;

        predictionMessage.textContent = result.message;

        statusMessage.textContent = "Prediction completed.";
        predictionResults.hidden = false;

    } catch (error) {
        statusMessage.textContent =
            `Error: ${error.message}. Check whether the FastAPI server is running.`;
    } finally {
        predictButton.disabled = false;
    }
});