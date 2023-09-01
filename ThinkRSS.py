
import subprocess
import feedparser
import os
from colorama import init, Fore, Style

init(autoreset=True)

def deschide_link_browser(link):
    subprocess.run(["xdg-open", link])

def reda_video_cu_mpv(link):
    subprocess.run(["mpv", link])

def deschide_articol(link):
    subprocess.run(["xdg-open", link])

def extrage_link(link):
    return link.split(' ', 1)[0]

def prelucreaza_feed_rss(link):
    while True:
        os.system('clear')  # Curăță ecranul terminalului
        feed = feedparser.parse(link)
        for idx, entry in enumerate(feed.entries, start=1):
            print(f"{Fore.BLUE}{idx}. {Fore.CYAN}{entry.title}")
        
        alegere_articol = input(f"{Fore.YELLOW}Selectează numărul articolului pe care dorești să-l deschizi (0 pentru a reveni): ")
        if alegere_articol == '0':
            return
        try:
            alegere_articol = int(alegere_articol)
            if 1 <= alegere_articol <= len(feed.entries):
                deschide_articol(feed.entries[alegere_articol - 1].link)
        except ValueError:
            print(f"{Fore.RED}Alegere invalidă.")

def prelucreaza_feed_youtube(link):
    while True:
        os.system('clear')  # Curăță ecranul terminalului
        feed = feedparser.parse(link)
        for idx, entry in enumerate(feed.entries, start=1):
            print(f"{Fore.BLUE}{idx}. {Fore.CYAN}{entry.title}")
        
        alegere_clip = input(f"{Fore.YELLOW}Selectează numărul clipului pe care dorești să-l redai în mpv (0 pentru a reveni): ")
        if alegere_clip == '0':
            return
        try:
            alegere_clip = int(alegere_clip)
            if 1 <= alegere_clip <= len(feed.entries):
                reda_video_cu_mpv(feed.entries[alegere_clip - 1].link)
        except ValueError:
            print(f"{Fore.RED}Alegere invalidă.")

if __name__ == "__main__":
    nume_fisier = "links.txt"
    try:
        with open(nume_fisier, "r") as f:
            lines = f.readlines()
            links = [line.strip() for line in lines if line.strip()]
            
        while True:
            os.system('clear')  # Curăță ecranul terminalului
            for idx, line in enumerate(links, start=1):
                if line.startswith("#"):
                    print(f"{Fore.CYAN}{line}")
                else:
                    parts = line.split('"')
                    if len(parts) >= 3:
                        print(f"{Fore.MAGENTA}{idx}. {Fore.GREEN}{parts[0]}{Fore.CYAN}\"{Fore.WHITE}{parts[1]}{Fore.CYAN}\"{Fore.MAGENTA}{parts[2]}")
                    else:
                        print(f"{Fore.MAGENTA}{idx}. {Fore.CYAN}{line}")
            
            alegere_str = input(f"{Fore.YELLOW}Selectează numărul link-ului pe care dorești să-l deschizi (0 pentru ieșire): ")
            
            try:
                alegere = int(alegere_str)
                
                if alegere == 0:
                    print(f"{Fore.YELLOW}La revedere!")
                    break
                elif alegere >= 1 and alegere <= len(links):
                    line_ales = links[alegere - 1]
                    link_ales = extrage_link(line_ales)
                    if link_ales.startswith("https://www.youtube.com/"):
                        print(f"{Fore.MAGENTA}Prelucrez feed YouTube...")
                        prelucreaza_feed_youtube(link_ales)
                    else:
                        print(f"{Fore.MAGENTA}Prelucrez feed RSS...")
                        prelucreaza_feed_rss(link_ales)
                else:
                    print(f"{Fore.RED}Alegere invalidă.")
            except ValueError:
                print(f"{Fore.RED}Te rog introdu un număr valid.")
    except FileNotFoundError:
        print(f"{Fore.RED}Fișierul nu a fost găsit.")
