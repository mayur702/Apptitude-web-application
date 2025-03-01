const BASE_URL = "http://my-backend-lb-963343963.us-east-1.elb.amazonaws.com";

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const questionForm = document.getElementById("questionForm");

    // Handle User Registration
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("name").value;
            const mobile_no = document.getElementById("mobile_no").value;
            const email = document.getElementById("email").value;
            const role = document.getElementById("role").value;
            const password = document.getElementById("password").value;
            const confirm_password = document.getElementById("confirm_password").value;

            const response = await fetch(`${BASE_URL}/register/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, mobile_no, email, role, password, confirm_password }),
            });

            const result = await response.json();
            if (response.ok) {
                alert("Registration successful! You can now login.");
                window.location.href = "index.html"; // Redirect to login page
            } else {
                alert(result.detail || "Registration failed!");
            }
        });
    }

    // Handle User Login
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;

            try {
                const response = await fetch(`${BASE_URL}/login/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password }),
                });

                const result = await response.json();
                if (response.ok) {
                    localStorage.setItem("token", result.access_token);
                    localStorage.setItem("userEmail", email);
                    alert("Login successful!");
                    window.location.href = "dashboard.html"; // Redirect to dashboard
                } else {
                    alert("Invalid email or password");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    }

    // Handle Question Upload (Only for Admins)
    // if (questionForm) {
    //     questionForm.addEventListener("submit", async (e) => {
    //         e.preventDefault();

    //         const token = localStorage.getItem("token");
    //         if (!token) {
    //             alert("You must be logged in to add questions!");
    //             return;
    //         }

    //         const question_text = document.getElementById("question_text").value;
    //         const option_a = document.getElementById("option_a").value;
    //         const option_b = document.getElementById("option_b").value;
    //         const option_c = document.getElementById("option_c").value;
    //         const option_d = document.getElementById("option_d").value;
    //         const correct_option = document.getElementById("correct_option").value;

    //         try {
    //             const response = await fetch(`${BASE_URL}/questions/`, {
    //                 method: "POST",
    //                 headers: {
    //                     "Content-Type": "application/json",
    //                     "Authorization": `Bearer ${token}`
    //                 },
    //                 body: JSON.stringify({ question_text, option_a, option_b, option_c, option_d, correct_option })
    //             });

    //             const result = await response.json();
    //             if (response.ok) {
    //                 alert("Question uploaded successfully!");
    //                 document.getElementById("questionForm").reset();
    //             } else {
    //                 alert(result.detail || "Failed to upload question!");
    //             }
    //         } catch (error) {
    //             console.error("Error:", error);
    //             alert("Something went wrong. Please try again.");
    //         }
    //     });
    // }
});
