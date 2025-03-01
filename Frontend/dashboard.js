const BASE_URL = "http://my-backend-lb-963343963.us-east-1.elb.amazonaws.com";

document.addEventListener("DOMContentLoaded", function () {
    const getResultButton = document.getElementById("getResult");
    const resultContainer = document.getElementById("resultContainer");

    getResultButton.addEventListener("click", async function () {
        try {
            const token = localStorage.getItem("token"); // Ensure user is authenticated
            if (!token) {
                alert("Please log in to view results.");
                return;
            }

            const response = await fetch(`${BASE_URL}/exam/grade/`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Failed to fetch results.");
            }

            const result = await response.json();
            
            // Display results
            resultContainer.innerHTML = `
                <p>Your Score: <span class="text-blue-600">${result.score} / ${result.total_questions}</span></p>
                <p>Percentage: <span class="text-green-600">${result.percentage}%</span></p>
            `;
            resultContainer.classList.remove("hidden");
        } catch (error) {
            console.error("Error fetching results:", error);
            alert("An error occurred while fetching your results.");
        }
    });
});
