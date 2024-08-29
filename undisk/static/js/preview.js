document.addEventListener('DOMContentLoaded', function() {
    const previewContainer = document.getElementById('preview-container');
    if (previewContainer && previewContainer.innerText.startsWith('http')) {
        const fileUrl = previewContainer.innerText;
        const url = new URL(fileUrl);
        const fileName = url.searchParams.get('filename');
        const fileExtension = fileName.split('.').pop().toLowerCase();

        let viewerUrl;
        if (fileExtension === 'docx' || fileExtension === 'xlsx') {
            viewerUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(fileUrl)}`;
        }

        if (viewerUrl) {
            previewContainer.innerHTML = `<iframe src="${viewerUrl}" width="100%" height="600px"></iframe>`;
        } else {
            previewContainer.innerHTML = 'Предварительный просмотр недоступен';
        }
    } else if (previewContainer && previewContainer.innerText.startsWith('data:')) {
        const dataUrl = previewContainer.innerText;
        const fileExtension = dataUrl.split(';')[0].split('/')[1];

        if (fileExtension === 'zip') {
            fetch(dataUrl)
                .then(res => res.arrayBuffer())
                .then(buffer => {
                    JSZip.loadAsync(buffer).then(zip => {
                        const fileList = Object.keys(zip.files).join('<br>');
                        previewContainer.innerHTML = `<pre class="text-view">${fileList}</pre>`;
                    });
                })
                .catch(err => {
                    previewContainer.innerHTML = 'Предварительный просмотр недоступен';
                });
        } else {
            previewContainer.innerHTML = 'Предварительный просмотр недоступен';
        }
    }
});