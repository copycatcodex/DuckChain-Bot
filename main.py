import time
import requests
from concurrent.futures import ThreadPoolExecutor
from config import AccountList  
from utils.utilities import *

previous_results = {}

def fetch_and_quack(account, index):
    headers = get_headers(account)  # Mengambil headers dari utils/headers.py
    proxies = account.get("Proxy")  # Ambil proxy jika ada, None jika tidak

    try:
        time.sleep(0.5)  # Adjust delay as needed
        # Menggunakan proxy jika tersedia
        response = requests.get('https://preapi.duckchain.io/user/info', headers=headers, proxies=proxies)
        
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
            record = record_full[-1] if record_full else 'N/A'

            result = (
                f" {account['Name']} | "
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
    def quacktime(account):
        headers = get_headers(account)  # Mengambil headers dari utils/headers.py
        try:
            response = requests.get('https://preapi.duckchain.io/quack/execute?', headers=headers, proxies=proxies)
            response.raise_for_status()
            data = response.json()
            if data.get('code') == 200:
                return None
            else:
                print(f"Quack gagal untuk {account['Name']}, kode: {data.get('code')}")
        except requests.exceptions.RequestException as e:
            print(f'Gagal melakukan quack untuk Akun {index + 1}: {e}')

    quacktime(account)
    
    return result

try:
    while True:
        results = []

        with ThreadPoolExecutor(max_workers=len(AccountList)) as executor:
            futures = [executor.submit(fetch_and_quack, account, index) for index, account in enumerate(AccountList)]
            for future in futures:
                result = future.result()
                if result:
                    formatted_result = format_result(result)  # Format hasil dengan warna
                    results.append(formatted_result)

        if results:
            print("\033c", end="")  # Membersihkan layar
            show_banner()  # Menampilkan banner tanpa warna acak
            for res in results:
                print(res, end='', flush=True)

        time.sleep(0.5)

except KeyboardInterrupt:
    print(colored_string("\nBot dihentikan oleh pengguna (Ctrl+C)."))
