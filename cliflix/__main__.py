import logging
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue, Empty
from threading import Thread

from tabulate import tabulate

# sys.path.insert(0, str(Path.joinpath(Path(__file__).parent, "../search")))
from cliflix.search import engines

dct = []
response_queue = Queue()
executor: ThreadPoolExecutor = None
search_str = "The Kashmir Files"

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

parts = ["link", "name", "size", "seeds", "leech", "engine_url", "desc_link"]


def get_score(base: str, resp: str):
    base = tokenize_title(base).split()
    resp = tokenize_title(resp).split()
    print(f"base: {base}, resp: {resp}")
    return len(list(set(base) & set(resp))) / len(resp)


def tokenize_title(s: str):
    original = s
    stopwords = ["webrip", "x264", "x265", "1080p", "720p", "480p", "ddp5.1", "web", "h264", "h265", "web-dl", "atmos",
                 "amzn", "nf", "aac", "mp4", "xvid", "dvdrip", "cam", "hdts", "hdtv", "flac", "brrip", "hrip", "dsnp",
                 "2160p", "h.264", "h.265"]
    s = s.lower()
    for stopword in stopwords:
        s = s.replace(stopword, " ")

    s = re.sub(r"\[.*?]", " ", s)
    s = re.sub(r"\.|\(|\)|_|-|\[|]|\+", " ", s)
    s = s.lower()
    s = re.sub(' +', ' ', s)
    print(original, s)
    return s


def exit_program():
    clear_console()
    executor.shutdown(wait=False, cancel_futures=True)
    exit()


def process_choice(choice):
    clear_console()
    print("Launching VLC...", end=" ")
    process = subprocess.Popen('vlc "' + dct[choice - 1]["link"] + '"', shell=True)
    exit_program()


def process_and_display(in_progress=True):
    keys = ["S.No", "name", "size", "seeds", "leech"]
    torrents = dct[:10]
    resp = []
    for i, torrent in enumerate(torrents):
        torrent[keys[0]] = i + 1
        resp.append([torrent[key] for key in keys])

    clear_console()
    print("\n")
    print(tabulate(resp, headers=keys, tablefmt="fancy_grid"), flush=True)
    if in_progress:
        print("\nSearch in progress....")

    print("\nEnter S.No. of torrent to stream (q to exit): ", end=" ")
    # choice = int(input("\n\nEnter S.No of torrent to stream: "))
    # process_choice(choice)


def response_queue_monitor(timeout=30):
    global dct
    while True:
        try:
            data_dict = response_queue.get(timeout=timeout)
            data_dict["score"] = get_score(search_str, data_dict["name"])
            if data_dict["size"][-2:] == " B":
                bytes = int(data_dict["size"][:-2])
                if bytes / (1024 ** 2) > 1024:
                    data_dict["size"] = f"{bytes / (1024 ** 3):.2f} GB"
                else:
                    data_dict["size"] = f"{bytes / (1024 ** 2):.2f} MB"
            dct.append(data_dict)
            dct = sorted(dct, key=lambda i: (int(i["seeds"]), i["score"]), reverse=True)
            process_and_display()
        except Empty:
            process_and_display(in_progress=False)
            break

        except Exception as e:
            logging.error("Some Error Occurred", exc_info=True)


def worker(engine, search_str):
    resps = engine.search(search_str.replace(" ", "+"))
    for res in resps:
        response_queue.put(res)


def main(num_workers=4):
    global executor
    clear_console()
    search_str = input("Search for: ")
    clear_console()
    print("Searching...")
    response_consumer = Thread(target=response_queue_monitor, daemon=True)
    response_consumer.start()

    executor = ThreadPoolExecutor(num_workers)
    for engine in engines.values():
        engine = engine()
        executor.submit(worker, engine, search_str)

    choice = input("\nEnter S.No of torrent to stream (q to exit): ")
    if str(choice) == "q":
        exit_program()
    else:
        process_choice(int(choice))
    return response_consumer


if __name__ == "__main__":
    main()
