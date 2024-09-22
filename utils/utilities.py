import os
import random
from colorama import Fore, Style, init

# Inisialisasi colorama (agar warna bekerja di berbagai platform)
init(autoreset=True)

# Warna tetap untuk string tertentu
fixed_colors = {
    #"Akun": Fore.GREEN,  # Warna hijau tetap untuk "Akun"
    #"Nama": Fore.CYAN,  # Warna cyan tetap untuk "Nama"
    #"QuackTime": Fore.YELLOW,  # Warna kuning tetap untuk "QuackTime"
    #"GifBox": Fore.MAGENTA,  # Warna magenta tetap untuk "GifBox"
    #"Decibels": Fore.RED,  # Warna merah tetap untuk "Decibels"
    #"Record": Fore.BLUE,  # Warna biru tetap untuk "Record"
}

# Warna acak yang tersedia
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

def colored_string(text):
    
    #Memberikan warna acak pada teks yang diberikan.

    return f"{random.choice(colors)}{text}{Style.RESET_ALL}"

def colorize_text(text, keyword):

    #Memberikan warna tetap jika keyword ditemukan dalam text,
    #atau warna acak jika tidak ada keyword yang cocok.

    for key, color in fixed_colors.items():
        if key in text:
            return f"{color}{text}{Style.RESET_ALL}"
    return f"{random.choice(colors)}{text}{Style.RESET_ALL}"

def format_result(result):

    #Memformat string hasil yang dipisahkan oleh '|' dan memberi warna
    #pada bagian yang sesuai berdasarkan keyword.

    formatted = []
    parts = result.split('|')
    for part in parts:
        keyword = part.split(':')[0].strip()  # Mendapatkan kata kunci dari sebelum ":"
        formatted.append(colorize_text(part.strip(), keyword))
    return ' | '.join(formatted)


def show_banner():                                             
    banner = """
       ____          _   _____ _       _       
      |    \ _ _ ___| |_|     | |_ ___|_|___  ┃ Develop By:
      |  |  | | |  _| '_|   --|   | .'| |   | ┃ Copycatcodex
      |____/|___|___|_,_|_____|_|_|__,|_|_|_| ┃ https://github.com/copycatcodex
      =========================================================================="""
    print(banner)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_headers(account):
    """
    Mengembalikan headers umum yang digunakan untuk berbagai request.
    """
    return {
        'authority': 'preapi.duckchain.io',
        'method': 'GET',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'tma {account["Authorization"]}',
        'origin': 'https://tgdapp.duckchain.io',
        'priority': 'u=1, i',
        'referer': 'https://tgdapp.duckchain.io/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': account["UserAgent"]
    }

                                                     
