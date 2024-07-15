const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");

// Fetch initial greeting when the page loads
fetch('/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({message: ""})  // Send empty message to trigger initial response
})
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response, "chatbot");
    })
    .catch(error => {
        console.error('Error fetching initial message:', error);
        // Handle the error (e.g., display an error message to the user)
    });


sendButton.addEventListener("click", () => sendMessage());
userInput.addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (message !== "") {
        displayMessage("You: " + message, "user");
        userInput.value = ""; // Clear input after sending

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message }) // Shorthand for { message: message }
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                displayMessage(data.response, "chatbot");
            } else if (data.error) {
                displayMessage("Error: " + data.error, "error");
            } else {
                console.error('Unexpected response format:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Error communicating with chatbot.", "error");
        });
    }
}

function displayMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);

    // Simulate typing effect (add this part)
    if (sender === "chatbot") {
        messageElement.textContent = ""; // Start with empty content
        let i = 0;
        const typingInterval = setInterval(() => {
            if (i < message.length) {
                messageElement.textContent += message.charAt(i);
                i++;
            } else {
                clearInterval(typingInterval); // Stop typing when done
            }
        }, 15); // Adjust typing speed (milliseconds per character)
    } else { // For user messages, display immediately
        messageElement.textContent = message;
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
}
