document.addEventListener('DOMContentLoaded', function () {
    const toggleIcon = document.getElementById('togglePassword');
    const passwordInput = document.querySelector('input[type="password"]');

    if (toggleIcon && passwordInput) {
      toggleIcon.addEventListener('click', function () {
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';
        toggleIcon.classList.toggle('bi-eye');
        toggleIcon.classList.toggle('bi-eye-slash');
      });
    }
  });