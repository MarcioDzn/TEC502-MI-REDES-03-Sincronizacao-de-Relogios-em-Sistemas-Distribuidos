import asyncio
import aiohttp
import os
import threading
import requests

URLS = ["172.16.103.9:8088", "172.16.103.8:8088", "172.16.103.7:8088"]

async def getTime(session, url):
    try:
        async with session.get(f'http://{url}/v1/api') as response:
            data = await response.json()
            return (data["node"], data["time"], data["leader"], data["drift"])
    except Exception as e:
        return (url, "DESLIGADO", "", "")


async def fetch_all_times(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(getTime(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


async def interface():
    results = await fetch_all_times(URLS)
    print("================== RELÓGIOS ==================")
    for result in results:
        node, time, leader, drift = result
        print(f"MAQUINA: {node} | TEMPO: {time} | DRIFT: {drift}", end=' ')
        if leader:
            print(f"| LIDER")
        else:
            print("")


def changeDrift():
    infos = input("Digite dois valores separados por espaço: ")
    id, drift = infos.split()

    id = int(id)
    url = URLS[id]

    try:
        response = requests.patch(f'http://{url}/v1/api')
    except:
        pass


async def main():
    while True:
        await interface()
        await asyncio.sleep(0.25)
        os.system('clear')

if __name__ == "__main__":
    threading.Thread(target=changeDrift).start()
    asyncio.run(main())
