import requests
from threading import Thread


def get_places():
    places = requests.get(
        "http://localhost:8000/places",
    ).json()
    print(places)


if __name__ == "__main__":
    threads = []
    for i in range(0,10):
        for i in range(0, 50):
            threads += [Thread(target=get_places())]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        threads.clear()
