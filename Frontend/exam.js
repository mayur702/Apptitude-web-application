
const BASE_URL = "https://new-web-vamn.onrender.com";

document.addEventListener("DOMContentLoaded", async () => {
    // const BASE_URL = "http://192.168.39.174:8000"; // Update with your API URL
     const token = localStorage.getItem("token");
 
     if (!token) {
         alert("You must be logged in to take the exam.");
         window.location.href = "index.html"; // Redirect if not logged in
         return;
     }
 
     const examContainer = document.getElementById("examContainer");
     const submitButton = document.getElementById("submitExam");
     const timerDisplay = document.getElementById("timer");
 
     let questionsData = []; // Store questions
     let timeLeft = 1800; // 30 minutes in seconds
     let timerInterval; // Timer reference
 
     async function fetchExamQuestions() {
         try {
             const response = await fetch(`${BASE_URL}/exam/questions/`, {
                 method: "GET",
                 headers: {
                     "Authorization": `Bearer ${token}`,
                     "Content-Type": "application/json"
                 }
             });
 
             if (!response.ok) {
                 throw new Error("Failed to fetch questions");
             }
 
             questionsData = await response.json();
 
             if (questionsData.length === 0) {
                 examContainer.innerHTML = `<p class="text-red-500 text-center">No questions available.</p>`;
                 return;
             }
 
             renderQuestions(questionsData);
             startTimer(); // Start the timer when questions load
         } catch (error) {
             console.error("Error fetching questions:", error);
             examContainer.innerHTML = `<p class="text-red-500 text-center">Error loading exam questions.</p>`;
         }
     }
 
     function renderQuestions(questions) {
         examContainer.innerHTML = ""; // Clear previous content
 
         questions.forEach((question, index) => {
             const questionBlock = document.createElement("div");
             questionBlock.classList.add("p-4", "border", "rounded-lg", "shadow-md", "mb-4");
 
             questionBlock.innerHTML = `
                 <h3 class="font-bold text-lg mb-2">${index + 1}. ${question.question_text}</h3>
                 <div class="space-y-2">
                     <label class="flex items-center">
                         <input type="radio" name="question_${question.id}" value="a" class="mr-2"> ${question.option_a}
                     </label>
                     <label class="flex items-center">
                         <input type="radio" name="question_${question.id}" value="b" class="mr-2"> ${question.option_b}
                     </label>
                     <label class="flex items-center">
                         <input type="radio" name="question_${question.id}" value="c" class="mr-2"> ${question.option_c}
                     </label>
                     <label class="flex items-center">
                         <input type="radio" name="question_${question.id}" value="d" class="mr-2"> ${question.option_d}
                     </label>
                 </div>
             `;
 
             examContainer.appendChild(questionBlock);
         });
 
         submitButton.classList.remove("hidden"); // Show Submit button
     }
 
     function startTimer() {
         updateTimerDisplay();
         timerInterval = setInterval(() => {
             if (timeLeft <= 0) {
                 clearInterval(timerInterval);
                 submitExam(); // Auto-submit when time runs out
             } else {
                 timeLeft--;
                 updateTimerDisplay();
             }
         }, 1000);
     }
 
     function updateTimerDisplay() {
         const minutes = Math.floor(timeLeft / 60);
         const seconds = timeLeft % 60;
         timerDisplay.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
     }
 
     async function submitExam() {
         clearInterval(timerInterval); // Stop timer
 
         const answers = [];
 
         questionsData.forEach((question) => {
             const selectedOption = document.querySelector(`input[name="question_${question.id}"]:checked`);
             if (selectedOption) {
                 answers.push({
                     question_id: question.id,
                     answer: selectedOption.value
                 });
             }
         });
 
         // Disable all options after time is up
         document.querySelectorAll("input[type=radio]").forEach(input => {
             input.disabled = true;
         });
 
         submitButton.disabled = true; // Disable submit button
 
         try {
             const response = await fetch(`${BASE_URL}/exam/submit/`, {
                 method: "POST",
                 headers: {
                     "Authorization": `Bearer ${token}`,
                     "Content-Type": "application/json"
                 },
                 body: JSON.stringify(answers)
             });
 
             const result = await response.json();
 
             if (response.ok) {
                 alert(result.message);
                 window.location.href = "dashboard.html"; // Redirect after submission
             } else {
                 alert("Error submitting exam: " + result.detail);
             }
         } catch (error) {
             console.error("Error submitting exam:", error);
             alert("Failed to submit exam. Please try again.");
         }
     }
 
     submitButton.addEventListener("click", submitExam);
 
     fetchExamQuestions();
 });