document.addEventListener("DOMContentLoaded", function () {
    const profileButton = document.getElementById('profile-button');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const mainContainer = document.getElementById('main-container');
    const chatInput = document.querySelector('.chat-input input');
    const chatOutput = document.querySelector('.chat-output');
    const sendButton = document.querySelector('.chat-input button');

    profileButton.addEventListener('click', function (event) {
        event.stopPropagation();
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });
    mainContainer.addEventListener('click', function () {
        dropdownMenu.style.display = 'none';
    });
    dropdownMenu.addEventListener('click', function (event) {
        event.stopPropagation();
    });
    function detectLanguage(message) {
        // Simple language detection based on input
        if (/[\u0900-\u097F]/.test(message)) { 
            return 'hi';
        } else if (/[\u0A00-\u0A7F]/.test(message)) { 
            return 'mr';
        } else {
            return 'en'; 
        }
    }
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            const messageElement = document.createElement('div');
            messageElement.className = 'message user'; 
            
            const messageText = document.createElement('div');
            messageText.className = 'message-text';
            messageText.textContent = message;
            messageElement.appendChild(messageText);
            chatOutput.appendChild(messageElement);
            chatInput.value = '';
            chatOutput.scrollTop = chatOutput.scrollHeight;

            const language = detectLanguage(message);
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: message, language: language })
            })
            .then(response => response.json())
            .then(data => {
                const responseElement = document.createElement('div');
                responseElement.className = 'message'; 
                
                const responseText = document.createElement('div');
                responseText.className = 'message-text';
                responseText.innerHTML = data.response;  // Render HTML

                responseElement.appendChild(responseText);
                chatOutput.appendChild(responseElement);
                chatOutput.scrollTop = chatOutput.scrollHeight;
            });
        }
    }
    sendButton.addEventListener('click', function () {
        sendMessage();
    });
    chatInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); 
            sendMessage();
        }
    });

    chatInput.addEventListener('focus', function () {
        chatInput.classList.add('input-focused');
    });

    chatInput.addEventListener('blur', function () {
        chatInput.classList.remove('input-focused');
    });
});