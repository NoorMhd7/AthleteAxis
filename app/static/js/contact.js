const form = document.getElementById('contact-form');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    const firstName = document.getElementById('first-name');
    const lastName = document.getElementById('last-name');
    const email = document.getElementById('email');
    const message = document.getElementById('message');
    const button = document.querySelector('.send-button');  // Updated class name

    let isValid = true;

    if (!firstName.value.trim()) {
        firstName.classList.add('invalid');
        isValid = false;
    } else {
        firstName.classList.remove('invalid');
    }

    if (!lastName.value.trim()) {
        lastName.classList.add('invalid');
        isValid = false;
    } else {
        lastName.classList.remove('invalid');
    }

    if (!email.value.trim()) {
        email.classList.add('invalid');
        isValid = false;
    } else {
        email.classList.remove('invalid');
    }

    if (!message.value.trim()) {
        message.classList.add('invalid');
        isValid = false;
    } else {
        message.classList.remove('invalid');
    }

    if (isValid) {
        button.textContent = 'RECEIVED';  // Keep caps to match design
        form.reset();
        setTimeout(() => {
            button.textContent = 'SEND';  // Keep caps to match design
        }, 2000);
    }
});