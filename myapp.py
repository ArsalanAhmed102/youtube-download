from flask import Flask, request, jsonify, url_for, send_file
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url')
    
    try:
        yt = YouTube(url)
        video_info = {
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "download_links": {
                "mp4": url_for('download_mp4', video_id=yt.video_id, _external=True),
                "mp3": url_for('download_mp3', video_id=yt.video_id, _external=True)
            }
        }
        
        return jsonify(video_info)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download_mp4/<video_id>', methods=['GET'])
def download_mp4(video_id):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video = yt.streams.get_highest_resolution()
        output_path = video.download()
        
        return send_file(output_path, as_attachment=True, download_name=f"{yt.title}.mp4")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download_mp3/<video_id>', methods=['GET'])
def download_mp3(video_id):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video = yt.streams.get_highest_resolution()
        output_path = video.download()
        
        clip = VideoFileClip(output_path)
        mp3_path = output_path.replace(".mp4", ".mp3")
        clip.audio.write_audiofile(mp3_path)
        clip.close()
        
        os.remove(output_path)
        
        return send_file(mp3_path, as_attachment=True, download_name=f"{yt.title}.mp3")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
