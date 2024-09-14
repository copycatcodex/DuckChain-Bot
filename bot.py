# Developed by: copycatcodex (swandiary)
# Date: 2024
# Github: https://github.com/copycatcodex

import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Load authorization tokens from the file
with open('token.txt', 'r') as file:
    authorizations = [line.strip() for line in file]

previous_results = {}

def fetch_and_quack(auth, index):
    # Headers for fetching user data
    headers = {
        'authority': 'preapi.duckchain.io',
        'method': 'GET',
        'path': '/user/info',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'tma {auth}',
        'origin': 'https://tgdapp.duckchain.io',
        'priority': 'u=1, i',
        'referer': 'https://tgdapp.duckchain.io/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    # Fetch user data
    try:
        time.sleep(2)  # Adjust delay as needed
        response = requests.get('https://preapi.duckchain.io/user/info', headers=headers)
        if response.status_code == 401:
            result = f"Error: Account index {index} unauthorized"
        else:
            data = response.json()
            userdata = data.get('data', {})
            duckname = userdata.get('duckName', 'N/A')
            quacktime = userdata.get('quackTimes', 0)
            giftbox = userdata.get('boxAmount', 0)
            decibels = userdata.get('decibels', 0)
            record_full = userdata.get('quackRecords', [])
            record = record_full[-1]  

            result = (
                f"Akun: {index + 1} | "
                f"Nama: {duckname} | "
                f"QuackTime: {quacktime} | "
                f'GifBox: {giftbox} | '
                f'Decibels: {decibels} | '
                f'Record: {record} | '
            )

            if previous_results.get(index) != result:
                previous_results[index] = result
            else:
                result = None  # Avoid printing duplicate results

    except requests.exceptions.RequestException as e:
        result = f'Error for account {index + 1}: {e}'
        time.sleep(5)

    # Call quacktime function
    def quacktime(auth):
        headers = {
            "authority": "preapi.duckchain.io",
            "method": "GET",
            "path": "/quack/execute?",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"tma {auth}",
            "origin": "https://tgdapp.duckchain.io",
            "priority": "u=1, i",
            "referer": "https://tgdapp.duckchain.io/",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
        try:
            response = requests.get('https://preapi.duckchain.io/quack/execute?', headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get('code') == 200:
                print(f"🦆")
            else:
                print(f"Klik gagal dengan token , kode: {data.get('code')}")
        except requests.exceptions.RequestException as e:
            print(f'Gagal melakukan klik dengan token: {e}')

    quacktime(auth)
    
    return result

# Banner yang akan ditampilkan
banner = "================== DuckChain ==============="

while True:
    results = []

    with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
        futures = [executor.submit(fetch_and_quack, auth, index) for index, auth in enumerate(authorizations)]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    if results:
        print("\033c", end="")  # Membersihkan layar
        print(banner)  # Menampilkan banner
        print('\n'.join(results), end='', flush=True)
    
    time.sleep(1)
