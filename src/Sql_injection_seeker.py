import argparse
import os
import signal
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from pystyle import Colors, Colorate

R = '\033[31m'
G = '\033[32m'
W = '\033[0m'

class Seeker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.queue = [base_url]
        self.sql_injection_urls = []
        self.sql_patterns = ["'"]

    def extract_links_from_page(self, url):
        try:
            response = requests.get(url)
            response_text = response.text
            soup = BeautifulSoup(response_text, "html.parser")
            links = [urljoin(url, link.get("href")) for link in soup.find_all("a")]
            return links
        except requests.RequestException as e:
            print(R + "[!]Error ->", e)
            return []

    def check_sql_injection(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            page_text = soup.get_text()

            if "SQL syntax" in page_text or "MySQL Query Error" in page_text or "Fatal error" in page_text or "Uncaught Error" in page_text:
                return True
            else:
                return False
        except requests.RequestException as e:
            print(R + "[!]Error ->", e)
            return False

    def handle_interrupt(self, signum, frame):
        print(Colorate.Vertical(Colors.green_to_blue, "**************************************************************************"))
        if self.sql_injection_urls:
            print(G + "\n[+]" + W + "Links with potential SQL injections:" + W)
            for url in self.sql_injection_urls:
                print(W + url)

        if not self.sql_injection_urls:
            print(print(R + "\n[-]" + W + "Potential SQL injection not found:" + W))
        exit()

    def seek_injections(self):
        signal.signal(signal.SIGINT, lambda signum, frame: self.handle_interrupt(signum, frame))

        while self.queue:
            current_url = self.queue.pop(0)
            if current_url in self.visited_urls:
                continue

            print(Colorate.Vertical(Colors.green_to_blue, "**************************************************************************"))
            print(G + "Scanning:" + W, current_url)
            self.visited_urls.add(current_url)

            if self.check_sql_injection(current_url):
                print(G + "[+]" + W + "Potential SQL injection found ->" + G, current_url)
                self.sql_injection_urls.append(current_url)

            links = self.extract_links_from_page(current_url)
            for link in links:
                if link not in self.visited_urls:
                    self.queue.append(link)
                    for pattern in self.sql_patterns:
                        modified_url = link + pattern
                        if self.check_sql_injection(modified_url):
                            print(G + "[+]" + W + "Potential SQL injection found ->" + G, modified_url)
                            self.sql_injection_urls.append(modified_url)
                            with open('Sql_İnjection_found.txt', 'a', encoding='utf-8', errors='ignore') as file:
                                file.write(modified_url + '\n')

        signal.signal(signal.SIGINT, signal.SIG_DFL)