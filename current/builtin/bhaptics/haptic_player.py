import json
from websocket import create_connection
from enum import Enum

class HapticPlayer:
    def __init__(self):
        try:
            self.ws = create_connection("ws://localhost:15881/v2/feedbacks")
        except:
            print("Couldn't connect")
            return


    def submit(self, key, frame):
        submit = {
            "Submit": [{
                "Type": "frame",
                "Key": key,
                "Frame": frame
            }]
        }

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    def submit_dot(self, key, position, dot_points, duration_millis):
        front_frame = {
            "position": position,
            "dotPoints": dot_points,
            "durationMillis": duration_millis
        }
        self.submit(key, front_frame)

    def submit_path(self, key, position, path_points, duration_millis):
        front_frame = {
            "position": position,
            "pathPoints": path_points,
            "durationMillis": duration_millis
        }
        self.submit(key, front_frame)

    def __del__(self):
        self.ws.close()
