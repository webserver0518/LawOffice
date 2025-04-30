
document.addEventListener("DOMContentLoaded", () => {
    const localTimeInput = document.getElementById("local_time");
    const now = new Date();
    const pad = n => n.toString().padStart(2, '0');
    const formatted = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
    localTimeInput.value = formatted;
});


document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    if (form) {
        form.addEventListener('submit', async e => {
            e.preventDefault();

            const formData = new FormData(form);
            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.status === 401) {
                alert("⛔ שם משתמש או סיסמה שגויים");
            } else {
                const html = await response.text();
                document.getElementById('dynamicContent').innerHTML = html;
            }
        });
    }
});