import os
import re
from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

# Define the directory where videos will be saved within the Flask main folder
download_dir = os.path.join(app.root_path, 'downloaded_videos')

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '', filename)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/paste_url', methods=['GET', 'POST'])
def paste_url():
    if request.method == 'POST':
        submitted_url = request.form['url']
        try:
            yt = YouTube(submitted_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_title = yt.title

            # Sanitize the video title to remove invalid characters
            sanitized_title = sanitize_filename(video_title)

            # Specify the full path to save the video to the download directory
            save_path = os.path.join(download_dir, f'{sanitized_title}.mp4')

            stream.download(output_path=download_dir, filename=sanitized_title)
            
            return f'Video downloaded to {save_path}', 200
        except Exception as e:
            return str(e), 400  # You can handle errors gracefully
    return render_template('paste_url.html')

if __name__ == '__main__':
    app.run(debug=True)









