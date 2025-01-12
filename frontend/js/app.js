document.addEventListener("DOMContentLoaded", () => {
    const textSubmit = document.getElementById("textSubmit");
    const fileSubmit = document.getElementById("fileSubmit");
    const textResult = document.getElementById("textResult");
    const fileResult = document.getElementById("fileResult");
    const fileInput = document.getElementById("fileInput");
    const progressBar = document.getElementById("progressBar");

    // Clear result when a new file is selected
    fileInput.addEventListener("change", () => {
        fileResult.style.display = "none"; // Hide the result
        fileResult.innerHTML = ""; // Clear the content
    });

    // Text Correction
    textSubmit.addEventListener("click", async () => {
        const textInput = document.getElementById("textInput").value;
        if (!textInput.trim()) {
            alert("Please enter some text.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/correct_text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: textInput }),
            });

            const result = await response.json();
            if (response.ok) {
                textResult.textContent = `Corrected Text: ${result.corrected_text}`;
                textResult.style.display = "block";
            } else {
                alert(result.error || "An error occurred.");
            }
        } catch (error) {
            console.error(error);
            alert("Failed to connect to the server.");
        }
    });

    // File Correction
    fileSubmit.addEventListener("click", async () => {
        const selectedFile = fileInput.files[0];
        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }

        if (selectedFile.type !== "text/plain") {
            alert("Only .txt files are allowed!");
            return;
        }

        // Clear previous results before uploading the new file
        fileResult.style.display = "none";
        fileResult.innerHTML = "";

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            progressBar.style.display = "block"; // Show progress bar
            const response = await fetch("http://127.0.0.1:5000/upload_file", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                fileResult.innerHTML = `Corrected file saved: <a href="${result.corrected_file_url}" target="_blank" download>Download Here</a>`;
                fileResult.style.display = "block";
            } else {
                alert(result.error || "An error occurred.");
            }
        } catch (error) {
            console.error(error);
            alert("Failed to connect to the server.");
        } finally {
            progressBar.style.display = "none"; // Hide progress bar after processing
            fileInput.value = ""; // Reset the file input
        }
    });

    function showAlert(message) {
        const alertBox = document.getElementById("alertBox");
        alertBox.textContent = message;
        alertBox.style.display = "block";
        setTimeout(() => (alertBox.style.display = "none"), 3000);
    }
});
