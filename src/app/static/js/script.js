document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('message-form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent form from reloading the page
        
        const prompt = document.getElementById('prompt').value;
        const messageContainer = document.getElementById('message-container');

        if (!prompt.trim()) {
            alert('Please enter a prompt');
            return;
        }

        // Display user message
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.innerHTML = `<p>${prompt}</p><div class="tokens">Tokens: Calculating...</div>`;
        messageContainer.appendChild(userMessageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight; // Auto-scroll to bottom

        // Clear input field
        document.getElementById('prompt').value = '';

        try {
            const response = await fetch("/generate_response/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrf_token')
                },
                body: JSON.stringify({ user_input: prompt })
            });

            const data = await response.json();

            if (response.ok) {
                // Display assistant's response
                const assistantMessageElement = document.createElement('div');
                assistantMessageElement.classList.add('message', 'assistant');
                assistantMessageElement.innerHTML = `<p>${data.response}</p><div class="tokens">Tokens: ${data.tokens || 0}</div>`;
                messageContainer.appendChild(assistantMessageElement);

                // Update user message token count (Assuming token count is available from the response)
                userMessageElement.querySelector('.tokens').textContent = `Tokens: ${data.user_tokens || 0}`;
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Handle Clear Cache button click
    document.getElementById('clear-cache').addEventListener('click', async function() {
        try {
            const response = await fetch("/clear_cache", { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrf_token') } });
            if (response.ok) {
                alert('Cache cleared!');
            } else {
                alert('Error clearing cache');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // New Chat 
    document.getElementById('new-chat-session').addEventListener('click', async function() {
        try {
            const response = await fetch("/session/create/", { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrf_token') } });
            if (response.ok) {
                fetchSessions(); // Refresh the session list
            } else {
                alert('Error creating new session');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Toggle side panel
    document.getElementById('toggle-button').addEventListener('click', function() {
        document.getElementById('side-panel').classList.toggle('open');
    });

    // Fetch and display chat sessions
    async function fetchSessions() {
        try {
            const response = await fetch("/get_sessions");
            const sessions = await response.json();
            const sessionList = document.getElementById('session-list');
            sessionList.innerHTML = '';

            sessions.forEach((session, index) => {
                const listItem = document.createElement('li');
                listItem.textContent = `${session.name}`;
                listItem.addEventListener('click', function() {
                    loadSession(session.id, session.name);
                });
                sessionList.appendChild(listItem);

                // Load the first session
                if (index === 0) {
                    loadSession(session.id, session.name);
                }
            });
        } catch (error) {
            console.error('Error fetching sessions:', error);
        }
    }

    // Load chat session
    async function loadSession(session_id, session_name) {
        try {
            const response = await fetch(`/session/${session_id}/`);
            const data = await response.json();
            const messageContainer = document.getElementById('message-container');
            messageContainer.innerHTML = '';
            document.getElementById('session-name').textContent = session_name;

            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', 'user');
                messageElement.innerHTML = `<p>${message.prompt}</p><div class="tokens">Tokens: ${message.prompt_tokens || 0}</div>`;
                messageContainer.appendChild(messageElement);

                if (message.completion) {
                    const completionElement = document.createElement('div');
                    completionElement.classList.add('message', 'assistant');
                    completionElement.innerHTML = `<p>${message.completion}</p><div class="tokens">Tokens: ${message.completion_tokens || 0}</div>`;
                    messageContainer.appendChild(completionElement);
                }
            });
        } catch (error) {
            console.error('Error loading session:', error);
        }
    }

    // Fetch sessions on page load
    fetchSessions();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}