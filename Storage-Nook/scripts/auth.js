document.getElementById('login-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Mock authentication logic
    console.log(`Logging in with: ${email}, ${password}`);
    alert('Logged in successfully!');
});
