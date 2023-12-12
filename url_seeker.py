import re
import random
import urllib.error
import urllib.parse
import sys
import os
import asyncio
import requests
import argparse
from signal import SIGINT, signal
import bs4, tqdm
from glob import glob
from pathlib import Path
from codecs import lookup, register
from random import SystemRandom
from socket import *
from datetime import *
from aiohttp import web
from pystyle import Colors, Colorate
from functools import wraps
import urllib3
from src import Sql_injection_seeker


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = False
R = '\033[31m'
G = '\033[32m'
W = '\033[0m'



def parse_arguments():
    parser = argparse.ArgumentParser(description='URL Seeker - Enhanced Dorking')
    parser.add_argument('--sites', help='Target Domain Ex: .com, .org, .net')
    parser.add_argument('--dorks', type=int, default=0, help='Number of dorks (0 for all)')
    parser.add_argument('--threads', type=int, help='Number of threads')
    parser.add_argument('--pages', type=int, help='Number of search engine pages to crawl per dork')
    parser.add_argument('--rdork' ,help="'Y' if you want the dorks to be randomly selected, 'N' if not")
    parser.add_argument('--S', help='URL or .txt file')
    parser.add_argument('--O', action='store_true' ,help='for automatic sql injection scanning --O')
    return parser.parse_args()

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Vertical(Colors.blue_to_cyan,"""                 
        █    ██  ██▀███   ██▓         ██████ ▓█████ ▓█████  ██ ▄█▀▓█████  ██▀███  
        ██  ▓██▒▓██ ▒ ██▒▓██▒       ▒██    ▒ ▓█   ▀ ▓█   ▀  ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
        ▓██  ▒██░▓██ ░▄█ ▒▒██░       ░ ▓██▄   ▒███   ▒███   ▓███▄░ ▒███   ▓██ ░▄█ ▒
        ▓▓█  ░██░▒██▀▀█▄  ▒██░         ▒   ██▒▒▓█  ▄ ▒▓█  ▄ ▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
        ▒▒█████▓ ░██▓ ▒██▒░██████▒   ▒██████▒▒░▒████▒░▒████▒▒██▒ █▄░▒████▒░██▓ ▒██▒
        ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░ ▒░▓  ░   ▒ ▒▓▒ ▒ ░░░ ▒░ ░░░ ▒░ ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
        ░░▒░ ░ ░   ░▒ ░ ▒░░ ░ ▒  ░   ░ ░▒  ░ ░ ░ ░  ░ ░ ░  ░░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
        ░░░ ░ ░   ░░   ░   ░ ░      ░  ░  ░     ░      ░   ░ ░░ ░    ░     ░░   ░ 
        ░        ░         ░  ░         ░     ░  ░   ░  ░░  ░      ░  ░   ░              
            https://github.com/0MeMo07/                     URL Seeker <  2.0.0  >                      
                                                               Enhanced Dorking                                                                    
          """))
    
def f_menu():
    global args
    args = parse_arguments()
    import time
    global proxy
    logo()

    print(R +f"[1]{W} Dork Search")
    print(R +f"[2]{W} SQL injection scanning\n")
    select = input(R + "> " + W)

    if select == "1":
        f_scan(args)
    if select == "2":
        input_value = input("\nEnter a URL or txt file to scan: ")

        if input_value.lower().endswith('.txt'):
            with open(input_value, 'r', encoding='iso-8859-9') as file:
                for line in file:
                    url = line.strip()
                    seeker_instance = Sql_injection_seeker.Seeker(base_url=url)
                    seeker_instance.seek_injections()
        else:
            seeker_instance = Sql_injection_seeker.Seeker(base_url=input_value)
            seeker_instance.seek_injections()

def f_scan(args):
    import time

    global pages_pulled_as_one
    global usearch
    global finallist
    global unsorted
    global finallist2
    global col
    global darkurl
    global sitearray
    global loaded_Dorks
    global unsorted
    global sites

    threads = []
    finallist = []
    finallist2 = []
    unsorted = []
    col = []
    darkurl = []
    loaded_Dorks = []

    if args.S:
        input_value = args.S

        if input_value.lower().endswith('.txt'):
            with open(input_value, 'r', encoding='iso-8859-9') as file:
                for line in file:
                    url = line.strip()
                    seeker_instance = Sql_injection_seeker.Seeker(base_url=url)
                    seeker_instance.seek_injections()
        else:
            seeker_instance = Sql_injection_seeker.Seeker(base_url=input_value)
            seeker_instance.seek_injections()
    else:
        sites = args.sites or input("\nTarget Domain Ex: .com, .org, .net : ")

        sitearray = list(map(str, sites.split(",")))

        dorks = args.dorks or input("Randomly select the number of dorks (0 for all of them... may take some time!) : ")
        
        random_dorks = args.rdork or input("'Y' if you want the dorks to be randomly selected, 'N' if not : ")

        d0rk = [line.strip() for line in open("src/d0rks.txt", "r", encoding="utf-8")]

        if int(dorks) == 0:
            if random_dorks == 'Y' or random_dorks == 'y':
                loaded_Dorks = random.sample(d0rk)
            else:
                loaded_Dorks = d0rk
        else:
            if random_dorks == 'Y' or random_dorks == 'y':
                loaded_Dorks = random.sample(d0rk, int(dorks))
            else:
                loaded_Dorks = d0rk[:int(dorks)]



        numthreads = args.threads or input("Enter the number of threads - 50-500 : ")

        pages_pulled_as_one = args.pages or input("Enter the number of Search Engine Pages to crawl per D0rk, between 25 and 100 @ 25 increments : ")

        print(R + "==============================")
        print(W + f"Sites           :{G}", sites)
        print(W + f"Threads         :{G}", numthreads)
        print(W + f"Dorks           :{G}", len(loaded_Dorks))
        print(W + f"Pages           :{G}", pages_pulled_as_one)
        print(W + f"Random Dork     :{G}", random_dorks)
        print(R + "==============================")
        time.sleep(5)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        usearch = loop.run_until_complete(search(pages_pulled_as_one, numthreads, loaded_Dorks, sitearray))




async def search(pages_pulled_as_one, numthreads, loaded_Dorks, sitearray):
    random.shuffle(loaded_Dorks)
    urls = []
    urls_len_last = 0
    timestart = datetime.now()
    for site in sitearray:
        progress = 0
        for dork in loaded_Dorks:
            progress += 1
            page = 0
            while page < int(pages_pulled_as_one):
                query = dork + " site:" + site
                futures = []
                loop = asyncio.get_event_loop()
                for i in range(25):
                    results_web = (
                        "http://www.bing.com/search?q="
                        + query
                        + "&go=Submit&first="
                        + str((page + i) * 50 + 1)
                        + "&count=50"
                    )
                    futures.append(
                        loop.run_in_executor(None, ignoring_get, results_web)
                    )
                page += 25
                stringreg = re.compile('(?<=href=")(.*?)(?=")')
                names = []
                for future in futures:
                    result = await future
                    names.extend(stringreg.findall(result))
                domains = set()
                for name in names:
                    basename = re.search(r"(?<=(://))[^/]*(?=/)", name)
                    if basename is None:
                        basename = re.search(r"(?<=://).*", name)
                    if basename is not None:
                        basename = basename.group(0)
                    if basename not in domains and basename is not None:
                        domains.add(basename)
                        urls.append(name)
                totalprogress = len(loaded_Dorks)
                percent = int((1.0 * progress / int(totalprogress)) * 100)
                urls_len = len(urls)
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                start_time = datetime.now()
                timeduration = start_time - timestart
                ticktock = timeduration.seconds
                hours, remainder = divmod(ticktock, 3600)
                minutes, seconds = divmod(remainder, 60)
                sys.stdout.flush()
                sys.stdout.write(
                    W + "\r\x1b[ " + R + " | Thx, domain <%s> has been targeted. \n "
                    "| Collected <%s> URLs since start of scan. \n"
                    " | D0rks: %s/%s progressed so far. \n"
                    " | Percent Done: %s. \n"
                    " | Current page no.: <%s>. \n"
                    " | Dork In Progress: %s. \n"
                    " | Elapsed Time: %s. \n"
                    % (
                        R + site,
                        repr(urls_len),
                        progress,
                        totalprogress,
                        repr(percent),
                        repr(page),
                        dork,
                        "%s:%s:%s" % (hours, minutes, seconds),
                    )
                )
                sys.stdout.flush()
                if urls_len == urls_len_last:
                    page = int(pages_pulled_as_one)
                urls_len_last = urls_len
    tmplist = []
    
    for url in urls:
        unsorted.append(url)
        try:
            host = url.split("/", 3)
            domain = host[2]
            for site in sitearray:
                if (
                    domain not in tmplist
                    and "=" in url
                    and any(x in url for x in sitearray)
                ):
                    finallist.append(url)
                    tmplist.append(domain)
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
    def output():
        try:
            print(f"\n\n{R}[+] {W}URLS (unsorted): {G}", len(urls))
            print(f"{R}[+] {W}URLS (sorted) with rubbish removed: {G}", len(finallist))
            print("")
            print(R + f"[1] {W}Save current SORTED URLs to file")
            print(R + f"[2] {W}Save current UNSORTED URLs to file")
            print(R + f"[3] {W}Print all the UNSORTED URLs ")
            print(R + f"[4] {W}Print all SORTED URLs")
            print(R + f"[5] {W}SQL injection scanning SORTED URLs")
            print(R + f"[6] {W}SQL injection scanning UNSORTED URLs\n")
            sec = input(R + "> ")
            if sec == "1":
                print(G + "\nSaving sorted URLs (" + str(len(finallist)) + ") to file\n")
                listname = input("Filename: ").encode("utf-8")
                list_name = open(listname, "w", encoding="utf-8")
                finallist.sort()
                logo()
                for t in finallist:
                    list_name.write(t + "\n")
                list_name.close()
                print("URLs saved, please check", listname)
                output()
            
            if sec == "2":
                print(G + "\nSaving unsorted URLs (" + str(len(unsorted)) + ") to file\n")
                listname = input("Filename: ").encode("utf-8")
                list_name = open(listname, "w", encoding="utf-8")
                unsorted.sort()
                logo()
                for t in unsorted:
                    list_name.write(t + "\n")
                list_name.close()
                print(W + f"URLs saved, please check {G}", listname)
                output()
                
            elif sec == "3":
                logo()
                print(W + "\nPrinting unsorted URLs:\n")
                unsorted.sort()
                for t in unsorted:
                    print(G + t + W)
                output()
            elif sec == "4":
                logo()
                print(W + "\nPrinting sorted URLs:\n")
                finallist.sort()
                for t in finallist:
                    print(G + t + W)
                output()
            elif sec == "5":
                logo()
                from src import Sql_injection_seeker
                finallist.sort()
                for url in finallist:
                    seeker_instance = Sql_injection_seeker.Seeker(base_url=url)
                    seeker_instance.seek_injections()
                output()
            elif sec == "6":
                logo()
                from src import Sql_injection_seeker
                unsorted.sort()
                for url in unsorted:
                    seeker_instance = Sql_injection_seeker.Seeker(base_url=url)
                    seeker_instance.seek_injections()
                output()
             
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')

    if args.O:
        print(f"\n\n{R}[+] {W}URLS (unsorted): {G}", len(urls))
        print(f"{R}[+] {W}URLS (sorted) with rubbish removed: {G}", len(finallist))
        print("")
        from src import Sql_injection_seeker
        finallist.sort()
        for url in finallist:
            seeker_instance = Sql_injection_seeker.Seeker(base_url=url)
            seeker_instance.seek_injections()
        output()
    else: 
        output()
    return finallist

def ignoring_get(url):
    header = [line.strip() for line in open("src/header.txt", "r", encoding="utf-8")]
    ua = random.choice(header)
    headers = {"user-agent": ua}
    try:
        try:
            if proxy == True:
                response = requests.get(url, headers=headers, timeout=2)
                response.raise_for_status()
            if proxy == False:
                response = requests.get(url, headers=headers, timeout=2)
                response.raise_for_status()
        except Exception:
            return ""
        return response.text
    except Exception as verb:
        print(str(verb))
f_menu()