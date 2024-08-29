document.addEventListener('DOMContentLoaded', function() {
    const previewContainer = document.getElementById('preview-container');
    if (previewContainer && previewContainer.innerText.startsWith('data:')) {
        const dataUrl = previewContainer.innerText;
        const fileExtension = dataUrl.split(';')[0].split('/')[1];

        if (['docx', 'xlsx', 'zip'].includes(fileExtension)) {
            fetch(dataUrl)
                .then(res => res.arrayBuffer())
                .then(buffer => {
                    if (fileExtension === 'docx') {
                        const doc = new Docxtemplater().loadZip(new JSZip(buffer));
                        const text = doc.getFullText();
                        previewContainer.innerHTML = `<pre>${text}</pre>`;
                    } else if (fileExtension === 'xlsx') {
                        const workbook = XLSX.read(buffer, { type: 'array' });
                        const sheetName = workbook.SheetNames[0];
                        const sheet = workbook.Sheets[sheetName];
                        const html = XLSX.utils.sheet_to_html(sheet);
                        previewContainer.innerHTML = html;
                    } else if (fileExtension === 'zip') {
                        JSZip.loadAsync(buffer).then(zip => {
                            const fileList = Object.keys(zip.files).join('<br>');
                            previewContainer.innerHTML = `<pre>${fileList}</pre>`;
                        });
                    }
                })
                .catch(err => {
                    previewContainer.innerHTML = 'Предварительный просмотр недоступен';
                });
        }
    }
});