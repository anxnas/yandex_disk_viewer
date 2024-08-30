document.addEventListener('DOMContentLoaded', function() {
    const fileItems = document.querySelectorAll('.file-item[data-file-type="file"]');
    const downloadSelectedButton = document.querySelector('.download-selected-button');

    fileItems.forEach(item => {
        const icon = item.querySelector('.icon');
        const link = item.querySelector('a');

        icon.addEventListener('click', function(event) {
            event.preventDefault(); // Предотвращаем переход по ссылке
            event.stopPropagation(); // Останавливаем всплытие события
            const checkbox = item.querySelector('.file-checkbox');
            checkbox.style.display = 'inline-block';
            checkbox.checked = !checkbox.checked;
            updateDownloadButtonVisibility();
        });

        link.addEventListener('click', function(event) {
            // Переход по ссылке происходит автоматически, ничего не нужно делать
        });
    });

    document.querySelectorAll('.file-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateDownloadButtonVisibility();
        });
    });

    function updateDownloadButtonVisibility() {
        const anyChecked = document.querySelectorAll('.file-checkbox:checked').length > 0;
        downloadSelectedButton.style.display = anyChecked ? 'inline-block' : 'none';
        document.querySelectorAll('.file-checkbox').forEach(checkbox => {
            checkbox.style.display = anyChecked ? 'inline-block' : 'none';
        });
    }
});