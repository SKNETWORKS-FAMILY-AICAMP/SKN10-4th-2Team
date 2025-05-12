document.addEventListener('DOMContentLoaded', () => {
	const input = document.getElementById('user-input');
	const button = document.querySelector('button');

	input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') addMessage();
	});
	button.addEventListener('click', addMessage);
});

function addMessage() {
	const input = document.getElementById('user-input');
	const message = input.value.trim();
	if (!message) return;

	const chatBox = document.getElementById('chat-box');

	const userMessage = document.createElement('div');
	userMessage.className = 'message user';
	userMessage.innerHTML = `<div class="message-content">${message}</div>`;
	chatBox.appendChild(userMessage);

	input.value = '';
	chatBox.scrollTop = chatBox.scrollHeight;

	sendMessage(message);
}

function sendMessage(message) {
	// 기본 로딩 모달 (처리 방식 추후 업데이트 가능)
	showLoadingModal('⏳ 답변을 생성 중입니다...');

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
			const responseText = data.response;
			const chatBox = document.getElementById('chat-box');

			// ✅ 처리 방식에 따라 설명 메시지 구분
			let loadingDetail = '';
			if (responseText.includes('🧠')) loadingDetail = 'LLM 기반으로 생성 중...';
			else if (responseText.includes('📁'))
				loadingDetail = '내부 문서를 분석하고 있습니다...';
			else if (responseText.includes('🌐')) loadingDetail = '외부 문서를 검색 중입니다...';

			// ✅ 로딩 모달 갱신 (짧고 작게)
			updateLoadingModal(`⏳ ${loadingDetail}`);

			// ✅ 약간의 딜레이 후 닫기 (자연스럽게)
			setTimeout(() => {
				Swal.close();

				const botMessage = document.createElement('div');
				botMessage.className = 'message bot';
				botMessage.innerHTML = `<div class="message-content">${responseText}</div>`;
				chatBox.appendChild(botMessage);
				chatBox.scrollTop = chatBox.scrollHeight;
			}, 500); // 0.5초 후 닫기
		})
		.catch((error) => {
			Swal.close();
			console.error('서버 오류:', error);
			Swal.fire('오류 발생', '답변을 가져오는 중 문제가 발생했습니다.', 'error');
		});
}

// ✅ CSRF
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

// SweetAlert2 로딩 모달
function showLoadingModal(message) {
	Swal.fire({
		title: message,
		allowOutsideClick: false,
		showConfirmButton: false,
		backdrop: true, // 필요하면 false로 변경 가능
		width: '600px',
		heightAuto: false, // 레이아웃 흔들림 방지
		willOpen: () => {
			// SweetAlert2가 강제로 넣는 스타일을 즉시 복구
			document.body.style.overflow = 'auto';
			document.body.style.paddingRight = '0px';
		},
		didOpen: () => {
			Swal.showLoading();
		},
	});
}

// ✅ 메시지 갱신 (title만 바꾸기)
function updateLoadingModal(newMessage) {
	const titleEl = Swal.getTitle();
	if (titleEl) titleEl.textContent = newMessage;
}
