from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, ALL
from models.your_ml_model import object_detection
import os

app = Flask(__name__)
Bootstrap(app)

videos = UploadSet('videos', ALL)
app.config['UPLOADED_VIDEOS_DEST'] = 'static/uploads'
configure_uploads(app, videos)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'video' in request.files:
        video = request.files['video']
        filename = videos.save(video)

        # Process the video with the object_detection function
        input_video = os.path.join(app.config['UPLOADED_VIDEOS_DEST'], filename)
        output_video = os.path.join(app.config['UPLOADED_VIDEOS_DEST'], f'processed_{filename}')
        object_detection(input_video, output_video)

        return redirect(url_for('download', filename=f'processed_{filename}'))
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return render_template('download.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOADED_VIDEOS_DEST'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
