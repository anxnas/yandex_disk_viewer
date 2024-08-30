document.addEventListener('DOMContentLoaded', function() {
    const fileItems = document.querySelectorAll('.file-item[data-file-type="file"]');
    const downloadSelectedButton = document.querySelector('.download-selected-button');

    fileItems.forEach(item => {
        item.addEventListener('click', function() {
            const checkbox = item.querySelector('.file-checkbox');
            checkbox.style.display = 'inline-block';
            checkbox.checked = !checkbox.checked;
            updateDownloadButtonVisibility();
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