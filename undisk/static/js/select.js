document.addEventListener('DOMContentLoaded', function() {
    const fileItems = document.querySelectorAll('.file-item[data-file-type="file"]');
    const downloadSelectedButton = document.querySelector('.download-selected-button');
    let longPressTimer;

    fileItems.forEach(item => {
        item.addEventListener('mousedown', function() {
            longPressTimer = setTimeout(() => {
                const checkbox = item.querySelector('.file-checkbox');
                checkbox.style.display = 'inline-block';
                checkbox.checked = true;
                updateDownloadButtonVisibility();
            }, 1000); // 1 second for long press
        });

        item.addEventListener('mouseup', function() {
            clearTimeout(longPressTimer);
        });

        item.addEventListener('mouseleave', function() {
            clearTimeout(longPressTimer);
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