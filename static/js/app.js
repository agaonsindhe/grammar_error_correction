const fileSubmit = document.getElementById("fileSubmit");
const textSubmit = document.getElementById("textSubmit");
const fileInput = document.getElementById("fileInput");
const textInput = document.getElementById("textInput");
const fileResult = document.getElementById("fileResult");
const textResult = document.getElementById("textResult");

// Modal Elements
const modal = document.createElement("div");
modal.classList.add("modal");
modal.innerHTML = `
    <div class="modal-content">
        <h2>Error</h2>
        <p id="modalMessage"></p>
        <button id="modalClose">Close</button>
    </div>
`;
document.body.appendChild(modal);
const modalMessage = document.getElementById("modalMessage");
const modalClose = document.getElementById("modalClose");

modalClose.addEventListener("click", () => {
    modal.style.display = "none";
});

// Function to show modal
function showModal(message) {
    modalMessage.textContent = message;
    modal.style.display = "flex";
}

// Function to handle grammar correction for text input
async function correctTextInput() {
    const inputText = textInput.value.trim();
    if (!inputText) {
        showModal("Please enter some text.");
        return;
    }

    try {
        const response = await fetch("/correct_text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: inputText }),
        });

        if (!response.ok) throw new Error("Failed to correct text.");

        const data = await response.json();
        textResult.innerHTML = `
            <strong>Original:</strong> ${data.original_text}<br>
            <strong>Corrected:</strong> ${data.corrected_text}
        `;
        textResult.style.display = "block";
    } catch (error) {
        showModal("An error occurred while correcting the text.");
    }
}

// Function to handle file upload for grammar correction
async function correctFileUpload() {
    const file = fileInput.files[0];
    if (!file) {
        showModal("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Show the progress bar
    const progressBarContainer = document.getElementById("progressBarContainer");
    const progressBar = document.getElementById("progressBar");
    progressBarContainer.style.display = "block";
    progressBar.style.width = "0%"; // Reset progress bar

    try {
        const response = await fetch("/upload_file", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest", // Required for progress
            },
        });

        // Simulate progress bar (if no real-time progress is available)
        for (let i = 0; i <= 100; i += 10) {
            progressBar.style.width = `${i}%`;
            await new Promise((resolve) => setTimeout(resolve, 50)); // Simulated delay
        }

        if(response.status===400) {
            showModal("Invalid file type");
            return;
        }
        if (!response.ok ) throw new Error("Failed to upload and correct file.");

        const data = await response.json();
        progressBar.style.width = "100%"; // Complete progress bar
        fileResult.innerHTML = `
            File corrected successfully. 
            <a href="${data.corrected_file_url}" target="_blank" download>Download Corrected File</a>
        `;
        fileResult.style.display = "block";
    } catch (error) {
        progressBarContainer.style.display = "none"; // Hide progress bar on error
        showModal("An error occurred while processing the file.");
    } finally {
        // Hide the progress bar after some delay
        setTimeout(() => {
            progressBarContainer.style.display = "none";
        }, 1000);
    }
}

// Event listeners
textSubmit.addEventListener("click", correctTextInput);
fileSubmit.addEventListener("click", correctFileUpload);
