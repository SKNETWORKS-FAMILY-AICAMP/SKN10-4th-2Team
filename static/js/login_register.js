document.addEventListener('DOMContentLoaded', () => {
	console.log('JS loaded and DOM ready');

	const signUpForm = document.querySelector('.sign-up-container form');
	if (!signUpForm) {
		console.warn('Sign up form not found');
		return;
	}

	// 기본 제출 방지
	signUpForm.addEventListener('submit', async (e) => {
		e.preventDefault(); // 무조건 폼 제출 막음

		const roleAdmin = document.getElementById('role-admin');
		const isAdmin = roleAdmin && roleAdmin.checked;

		if (isAdmin) {
			// 관리자 선택 시 SweetAlert로 코드 입력
			const { value: code } = await Swal.fire({
				title: '관리자 코드 입력',
				input: 'text',
				inputLabel: '관리자 인증 코드',
				inputPlaceholder: '코드를 입력하세요',
				showCancelButton: true,
				confirmButtonText: '확인',
				cancelButtonText: '취소',
			});

			if (code === '777') {
				const hiddenInput = document.createElement('input');
				hiddenInput.type = 'hidden';
				hiddenInput.name = 'is_superuser';
				hiddenInput.value = 'true';
				signUpForm.appendChild(hiddenInput);

				signUpForm.submit(); // 조건 만족 시 수동 제출
			} else if (code !== undefined) {
				await Swal.fire('실패', '잘못된 관리자 코드입니다.', 'error');
			}
		} else {
			// 일반 사용자라면 바로 제출
			signUpForm.submit();
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
