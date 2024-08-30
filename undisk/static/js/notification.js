// Функция для отображения уведомлений
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerText = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Показать уведомление об ошибке, если оно есть
document.addEventListener('DOMContentLoaded', function() {
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
        showNotification(errorMessage.textContent, 'error');
    }
});