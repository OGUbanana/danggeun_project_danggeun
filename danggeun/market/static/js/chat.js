const chatContainer = document.getElementById('chatContainer');
      const chatInput = document.getElementById('chatInput');

      const ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/');

      ws.onopen = () => {
        console.log('Connected to the chat server.');
      };

      ws.onmessage = (event) => {
        const messageData = JSON.parse(event.data);
        chatContainer.innerHTML += `<div>${messageData.message}</div>`;
      };

      ws.onclose = () => {
        console.log('Disconnected from the chat server.');
      };

      chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && chatInput.value) {
          ws.send(JSON.stringify({'message': chatInput.value}));
          chatInput.value = '';
        }
      });