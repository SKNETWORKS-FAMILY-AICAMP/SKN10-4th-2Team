document.addEventListener('DOMContentLoaded', () => {
	console.log('JS loaded and DOM ready');

	const signUpForm = document.querySelector('.sign-up-container form');
	if (!signUpForm) {
		console.warn('Sign up form not found');
		return;
	}

	// 기본 제출 방지
	signUpForm.addEventListener('submit', async (e) => {
		e.preventDefault();

		const roleAdmin = document.getElementById('role-admin');
		const isAdmin = roleAdmin && roleAdmin.checked;

		const passwordInput = signUpForm.querySelector('input[name="password"]');
		const usernameInput = signUpForm.querySelector('input[name="username"]');
		const password = passwordInput.value.trim();
		const username = usernameInput.value.trim();

		// 공통 유효성 검사 필요시 여기에 추가

		if (isAdmin) {
			// ✅ 관리자 비밀번호 규칙 검사
			const isTooShort = password.length < 8;
			const isNumericOnly = /^\d+$/.test(password);
			const isCommon = ['password', '12345678', 'qwerty', username].includes(
				password.toLowerCase()
			);

			if (isTooShort || isNumericOnly || isCommon) {
				await Swal.fire({
					icon: 'error',
					title: '비밀번호가 너무 약합니다.',
					text: '8자 이상, 일반적이지 않은 비밀번호를 사용하세요.',
					confirmButtonColor: '#ff4b2b',
				});
				return;
			}

			// 관리자 코드 입력
			const { value: code } = await Swal.fire({
				title: '관리자 코드 입력',
				input: 'text',
				inputPlaceholder: '코드를 입력하세요',
				showCancelButton: true,
				confirmButtonText: '확인',
				cancelButtonText: '취소',
				confirmButtonColor: '#ff4b2b',
			});

			if (code === '777') {
				const hiddenInput = document.createElement('input');
				hiddenInput.type = 'hidden';
				hiddenInput.name = 'is_superuser';
				hiddenInput.value = 'true';
				signUpForm.appendChild(hiddenInput);

				signUpForm.submit();
			} else if (code !== undefined) {
				await Swal.fire('실패', '잘못된 관리자 코드입니다.', 'error');
			}
		} else {
			signUpForm.submit(); // 일반 사용자: 규칙 검사 없이 바로 가입
		}
	});

	// 로그인/회원가입 폼 전환 로직 추가
	const signUpButton = document.getElementById('signUp');
	const signInButton = document.getElementById('signIn');
	const container = document.querySelector('.container');

	if (signUpButton && signInButton && container) {
		signUpButton.addEventListener('click', () => {
			container.classList.add('right-panel-active');
		});

		signInButton.addEventListener('click', () => {
			container.classList.remove('right-panel-active');
		});
	}
});
