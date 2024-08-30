import base64

class PreviewHandler:
    def __init__(self, path, file_content, download_link):
        self.path = path
        self.file_content = file_content
        self.download_link = download_link

    def get_preview_content(self):
        file_extension = self.path.split('.')[-1].lower()
        encoded_content = base64.b64encode(self.file_content).decode('utf-8')
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            return f'<img src="data:image/{file_extension};base64,{encoded_content}" alt="Image Preview" style="max-width: 100%;">'
        elif file_extension in ['mp4', 'webm']:
            return f'<video controls style="max-width: 100%;"><source src="data:video/{file_extension};base64,{encoded_content}" type="video/{file_extension}">Your browser does not support the video tag.</video>'
        elif file_extension in ['mp3', 'wav', 'ogg']:
            return f'<audio controls style="max-width: 100%;"><source src="data:audio/{file_extension};base64,{encoded_content}" type="audio/{file_extension}">Your browser does not support the audio element.</audio>'
        elif file_extension in ['txt', 'csv']:
            return f'<pre class="text-view">{self.file_content.decode("utf-8")}</pre>'
        elif file_extension in ['pdf']:
            return f'<embed src="data:application/pdf;base64,{encoded_content}" type="application/pdf" width="100%" height="600px" />'
        elif file_extension in ['docx', 'xlsx']:
            return self.download_link
        elif file_extension in ['zip']:
            return f'data:application/{file_extension};base64,{encoded_content}'
        else:
            return "Предварительный просмотр недоступен"