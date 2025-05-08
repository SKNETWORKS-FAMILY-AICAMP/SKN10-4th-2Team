document.addEventListener('DOMContentLoaded', () => {
	const input = document.getElementById('user-input');
	const button = document.querySelector('button');

	// Enter 키 이벤트
	input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') addMessage();
	});

	// 버튼 클릭 이벤트
	button.addEventListener('click', addMessage);
});

function addMessage() {
	const input = document.getElementById('user-input');
	const message = input.value.trim();
	if (!message) return;

	const chatBox = document.getElementById('chat-box');

	// 사용자 메시지 추가
	const userMessage = document.createElement('div');
	userMessage.className = 'message user';
	userMessage.innerHTML = `<div class="message-content">${message}</div>`;
	chatBox.appendChild(userMessage);

	input.value = '';
	chatBox.scrollTop = chatBox.scrollHeight;

	// 서버에 전송
	sendMessage(message);
}

function sendMessage(message) {
	fetch('/chat/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCSRFToken(),
		},
		body: JSON.stringify({ message }),
	})
		.then((response) => response.json())
		.then((data) => {
			const chatBox = document.getElementById('chat-box');
			const botMessage = document.createElement('div');
			botMessage.className = 'message bot';
			botMessage.innerHTML = `<div class="message-content">${data.response}</div>`;
			chatBox.appendChild(botMessage);
			chatBox.scrollTop = chatBox.scrollHeight;
		})
		.catch((error) => {
			console.error('서버 오류:', error);
		});
}

function getCSRFToken() {
	const name = 'csrftoken';
	const cookies = document.cookie.split('; ');
	for (let i = 0; i < cookies.length; i++) {
		const cookie = cookies[i].split('=');
		if (cookie[0] === name) {
			return decodeURIComponent(cookie[1]);
		}
	}
	return '';
}
