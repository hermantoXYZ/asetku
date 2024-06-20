document.addEventListener('DOMContentLoaded', (event) => {
    const qrCodeImage = document.getElementById('qrCodeImage');
    const popup = document.getElementById('popup');
    const closeBtn = document.querySelector('.close');

    qrCodeImage.addEventListener('click', () => {
        popup.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        popup.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == popup) {
            popup.style.display = 'none';
        }
    });
});
