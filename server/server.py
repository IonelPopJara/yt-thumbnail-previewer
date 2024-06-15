from flask import Flask
from flask_cors import CORS
from fetch_video_data import retrieve_top_videos

# For debug only
from fetch_video_data import fetch_top_videos

app = Flask(__name__)
CORS(app)

@app.route("/")
def server_check():
    #TODO: Add a pretty message about the app and who made it :)
    return "<p>Beep Boop</p><p>The server is running</p>"

@app.route("/top-videos")
def get_top_videos():
    response = retrieve_top_videos()
    # response = fetch_top_videos()
    return response

