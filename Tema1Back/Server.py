from time import time
import socketserver
import json
import requests
from http.server import BaseHTTPRequestHandler

PORT = 8000
google_key = json.load(open("config.json", "r"))["google_api_key"]


def log_info(info):
    file = open("log.txt", "a")
    file.write(info + "\n")
    file.close()


def get_ip():
    return requests.get(
        "https://api.ipify.org?format=json",
    ).json()["ip"]


def get_details():
    ip = get_ip()
    data = requests.get("https://ipapi.co/" + ip + "/json/", ).json()
    del data["ip"]
    del data["asn"]
    return data


def get_time():
    time = requests.get("http://worldclockapi.com/api/json/utc/now", ).json()
    del time["$id"]
    del time["utcOffset"]
    del time["serviceResponse"]
    return time


def get_hour(details):
    return \
        int(requests.get("http://worldclockapi.com/api/json/utc/now", ).json()["currentDateTime"].split("T")[1].split(
            ":")[0]) + int(details["utc_offset"][1:3])


def get_places(time, location):
    if time in range(6, 12):
        type = "cafe"
    elif time in range(12, 22):
        type = "restaurant"
    else:
        type = "bar"
    places = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(location[0]) + "," + str(
            location[1]) + "&radius=1000&type=" + type + "&opennow=true&key=" + google_key).json()[
        "results"]
    for place in places:
        del place["geometry"]
        del place["icon"]
        del place["id"]
        del place["photos"]
        del place["place_id"]
        del place["plus_code"]
        del place["scope"]
        del place["reference"]
        del place["opening_hours"]
    return places


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        start = time()
        response_code = 200
        if self.path == "/ip_addr":
            message = json.dumps({"ip": get_ip()})
        elif self.path == "/details":
            message = json.dumps(get_details())
        elif self.path == "/time":
            message = json.dumps(get_time())
        elif self.path == "/places":
            details = get_details()
            t = get_hour(details)
            message = json.dumps(get_places(t, (details["latitude"], details["longitude"])))
        else:
            message = "Wrong path"
            response_code = 404
        self.send_response(response_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(message.encode())
        info = dict()
        info["request"] = self.requestline
        info["response"] = {"response_code": response_code, "response_body": message}
        info["latency"] = str(time() - start)[:4] + "s"
        log_info(json.dumps(info))
        return


if __name__ == "__main__":
    handler = HttpHandler

    with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
