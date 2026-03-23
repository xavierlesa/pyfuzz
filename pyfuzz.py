#!/usr/bin/env python3
import argparse
import fileinput
import re
import requests
from urllib.parse import urljoin
import sys

NO_FORMAT = "\033[0m"
F_BOLD = "\033[1m"
C_LIME = "\033[38;5;10m"
C_YELLOW = "\033[38;5;11m"
C_ORANGE = "\033[38;5;202m"

banner = (
    "\033[38;5;202m██████╗ ██╗   ██╗███████╗██╗   ██╗███████╗███████╗\n"
    "\033[38;5;202m██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║╚══███╔╝╚══███╔╝\n"
    "\033[38;5;166m██████╔╝ ╚████╔╝ █████╗  ██║   ██║  ███╔╝   ███╔╝ \n"
    "\033[38;5;166m██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  \n"
    "\033[38;5;130m██║        ██║   ██║     ╚██████╔╝███████╗███████╗\n"
    "\033[38;5;130m╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝"
    "\033[0m"
)


def pyfuzz():
    parser = argparse.ArgumentParser()
    parser.add_argument("uri", type=str)
    parser.add_argument(
        "-w",
        "--wordlist",
        nargs="+",
        help="Path al(los) archivo(s) de wordlist. Ej ./wordlist.txt ./fuzz.txt. La lista final es la unión de todos los archivos y palabras únicas.",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=0,
        help="Comenzar desde una línea especifica del wordlist, por defecto 0.",
    )
    parser.add_argument(
        "-R",
        "--allow-redirects",
        action="store_true",
        help="Permite seguir en caso de redirección 3xx.",
    )

    # Parseo los argumentos
    args = parser.parse_args()

    uri = args.uri
    match = re.match(r'^.*://', uri)
    if not match:
        print(f"{C_YELLOW}No se identifico un schema. es https:// ?{NO_FORMAT}")
        return

    wordlist = args.wordlist
    if not wordlist:
        print(f"{C_YELLOW}No hay wordlist?{NO_FORMAT}")
        return

    start = args.start
    allow_redirects = args.allow_redirects

    # Junto todos los wrdlist en una sola lista, y armo un set para evitar repeticiones.
    # A esta lista se le aplica un start si hay.
    unique_words = set()

    with fileinput.input(wordlist) as file:
        for line in file:
            unique_words.add(line.strip())

    # for f in wordlist:
    #     if f == "-":
    #         for line in fileinput.input('-'):
    #             unique_words.add(line.strip())
    #         continue
    #     with open(f) as file:
    #         for line in file:
    #             unique_words.add(line.strip())

    print(f"Fuzzing sobre {C_LIME}{len(unique_words)}{NO_FORMAT} words...")

    count_300 = 0
    unique_words = sorted(unique_words)

    for i, path in enumerate(unique_words, start):
        url = urljoin(uri, path)
        response = requests.head(url, allow_redirects=allow_redirects)

        print(f"{i} ", end="")

        if response.status_code >= 400:
            print(f"[fail] {url} {response.status_code}")

        elif 400 > response.status_code >= 300:
            header = response.headers.get('location', '')
            print(f"{C_YELLOW}[redirect]{NO_FORMAT} {url} {response.status_code}\r\n\t{F_BOLD}{C_YELLOW}>{NO_FORMAT} {header}")

            if count_300 >= 6:
                print(f"{C_YELLOW}Muchos 3xx!! el dominio no es www.?{NO_FORMAT} {F_BOLD}-R{NO_FORMAT} para permitir redirects.")

            count_300 += 1

        else:
            count_300 = 0
            print(f"{F_BOLD}{C_LIME}[match]{NO_FORMAT} {url} {response.status_code}")


if __name__ == "__main__":
    print(banner)
    print()
    try:
        pyfuzz()
    except KeyboardInterrupt:
        print(f"{F_BOLD}{C_ORANGE}Kill!{NO_FORMAT}")
        sys.exit(0)
