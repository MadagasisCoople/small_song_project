/**
 * Client-side Socket.IO connection to Python backend.
 * 
 * For local development:
 *   - Use: "http://localhost:8000/ws"
 * For public access:
 *   - Replace with your public IP, domain, or ngrok tunnel URL.
 *   - Example: "https://abc123.ngrok.io/ws"
 */

const socket = io("http://localhost:8000",{
    transports: ["websocket","polling"], // skip HTTP long polling
});

// Connection established
socket.on("connect", () => {
    console.log(`Connected to backend. Socket ID: ${socket.id}`);
});

// Handle incoming task messages
socket.on("chat_message", (type) => {
    if (type == "music") {
        console.log("Music added to playlist");
    }
});

// Disconnection event
socket.on("disconnect", () => {
    console.warn("Disconnected from backend");
});

socket.on("Ms.Robin", (data) => {
    console.log("Received from backend:", data);
    console.log("Message text:", data.message);
    console.log("Received:", data.message);

    let chatBox = document.getElementById("chatMessages");
    let messageBox = document.createElement("li");
    messageBox.textContent = data.message;
    chatBox.appendChild(messageBox);
});