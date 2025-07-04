
if (location.protocol == 'https:') {
    wsStart = 'wss://'
}
else{
    wsStart = 'ws://'
}

const chatSocket = new WebSocket(wsStart+location.host+'/ws/');
const welcomeMessage = document.querySelector('.welcome-message');
let sendButton = document.querySelector('.chat-submit-button');

let currentFileKey = null;
let currentFileElement = null;

// function to send a message to the websocket when send button is clicked
document.querySelector('.chat-submit-button').addEventListener('click', function() {
    sendMessage();
});


function displayUserMessage(message) {
    // Select the response-message div
    let responseDiv = document.querySelector('.response-message');

    // Create a new div to hold the user's message
    let messageDiv = document.createElement('div');
    messageDiv.classList.add('user-message');
    messageDiv.textContent = message;

    // Append the user's message to the response-message div
    responseDiv.appendChild(messageDiv);
}

// function to display animation
function displayThinkingAnimation() {
    // Select the response-message div
    let responseDiv = document.querySelector('.response-message');

    // Create a new div for thinking animation
    let thinkingDiv = document.createElement('div');
    thinkingDiv.classList.add('thinking-dots');

    for(let i = 0; i < 3; i++) {
        let dot = document.createElement('span');
        thinkingDiv.appendChild(dot);
    }

    // Append the thinking animation to the response-message div
    responseDiv.appendChild(thinkingDiv);
}

// Function to send the message over the WebSocket
function sendMessage() {
    // Get the message from the input field
    let messageInput = document.querySelector('.chat-input-field');
    let messageText = messageInput.value;

    // Send the message over the WebSocket
    if (messageText) {
        chatSocket.send(JSON.stringify({ 
            'message': messageText,
            'file_key': currentFileKey
        }));

        // Display the user's message on the frontend
        displayUserMessage(messageText);
    }

    // Clear the input field after sending
    messageInput.value = '';

    // Display the thinking animation
    displayThinkingAnimation();
}

// Event listener to detect when Enter is pressed in the input field
document.querySelector('.chat-input-field').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
        event.preventDefault();  // Prevent the default action (form submission, newline addition, etc.)
    }
});


// Listen for messages from the server
chatSocket.onmessage = function(event) {
    // Remove the thinking animation
    removeThinkingAnimation();

    let receivedData = JSON.parse(event.data);
    console.log(receivedData.message); 
};


// function to show the message to the frontend
function displayReceivedMessage(message) {
    // Select the response-message div
    let responseDiv = document.querySelector('.response-message');

    // Create a new div to hold the received message
    let messageDiv = document.createElement('div');
    messageDiv.classList.add('received-message'); // Adding a class for possible styling purposes
    messageDiv.textContent = message;

    // Append the message to the response-message div
    responseDiv.appendChild(messageDiv);
    responseDiv.appendChild('<hr>')
}

// function to receive response from websocket
chatSocket.onmessage = function(event) {
    let receivedData = JSON.parse(event.data);
    console.log(receivedData.message);

    // Display the received message on the frontend
    displayReceivedMessage(receivedData.message);
};


// When a document-option is selected
function document_option_clicked(documentElement) {
    
    // Change background of currently selected elemnet
    if (currentFileElement) {
        currentFileElement.style.backgroundColor = 'black';
        currentFileElement.style.color = 'white';
    }

    // Remove welcome message
    welcomeMessage.style.display = 'none';



    // Enable search button
    sendButton.removeAttribute('disabled');

    // change current document file key and element
    currentFileKey = documentElement.getAttribute('data-value');
    currentFileElement = documentElement;

    currentFileElement.style.backgroundColor = '#FB8B24';
    currentFileElement.style.color = 'black';

}

document.addEventListener('DOMContentLoaded', function() {
    let documentOptions = document.querySelectorAll('.document-option');

    documentOptions.forEach(function(documentLink) {
        documentLink.addEventListener('click', function(event) {
            document_option_clicked(documentLink);
        });
    });
});



// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
// helper function for handling file upload
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// AJAX/JavaScript function to upload file to Django Session
function handleFileChange(inputElement) {
    if (inputElement.files && inputElement.files[0]) {
        var formData = new FormData();
        formData.append('file', inputElement.files[0]);

        
        fetch('/upload', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            },
            mode: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                // Add a button for the uploaded file to the DOM

                //Get documents list
                const documentsList = document.querySelector('.documents-list');

                // Step 2: Create the new <a> element
                const newDocument = document.createElement('a');
                
                // Step 3: Set the properties for the <a> element
                newDocument.href = "#";
                newDocument.className = "py-2 px-3 my-2 border-bottom document-option";
                newDocument.textContent = data.filename;

                newDocument.addEventListener('click', function() {
                    document_option_clicked(newDocument);
                });
                
                // Step 4: Append the new <a> element to the documents-list container
                documentsList.appendChild(newDocument);

            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            alert("There was an error uploading the file.");
        });
    }
}

