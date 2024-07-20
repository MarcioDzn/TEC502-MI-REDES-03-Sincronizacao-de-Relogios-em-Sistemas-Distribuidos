import requests, threading

URLS = ["172.16.103.9:8088", "172.16.103.8:8088", "172.16.103.7:8088"]

def changeDrift():
    while True:
        infos = input("Digite dois valores separados por espaço: ")
        id, drift = infos.split()

        id = int(id)
        drift = float(drift)
        print(type(drift))
        url = URLS[id]

        try:
            response = requests.patch(f'http://{url}/v1/api', json={"drift": drift})
        except:
            pass


if __name__ == "__main__":
    threading.Thread(target=changeDrift).start()