document.addEventListener("DOMContentLoaded", () => {
    const textSubmit = document.getElementById("textSubmit");
    const fileSubmit = document.getElementById("fileSubmit");
    const textResult = document.getElementById("textResult");
    const fileResult = document.getElementById("fileResult");

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
        const fileInput = document.getElementById("fileInput").files[0];
        if (!fileInput) {
            alert("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput);

        try {
            const response = await fetch("http://127.0.0.1:5000/upload_file", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                fileResult.innerHTML = `Corrected file saved: <a href="${result.corrected_file}" download>Download Here</a>`;
                fileResult.style.display = "block";
            } else {
                alert(result.error || "An error occurred.");
            }
        } catch (error) {
            console.error(error);
            alert("Failed to connect to the server.");
        }
    });
});
