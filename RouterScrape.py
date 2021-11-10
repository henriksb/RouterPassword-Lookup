import requests
from bs4 import BeautifulSoup

ROUTER_URL = "http://www.routerpasswords.com/"


def get_router_names():
    """Scrape all vendor names from routerpasswords.com"""
    name_list = []

    soup = requests.get(url=ROUTER_URL)
    soup = BeautifulSoup(soup.text, "lxml")

    for name in soup.findAll("option"):
        name_list.append(name.text)

    return name_list


def download_router_info(name, path):
    """Searches for information on a selected vendor and saves response in a text file"""
    passwords_list = []
    name = name.upper()
    #params = {"findpass": 1, "router": f"{name}", "findpassword": "Find Password"}

    soup = requests.post(url=ROUTER_URL+"/router-password/"+name)
    soup = BeautifulSoup(soup.text, "lxml")

    for tags in soup.findAll("td"):
        passwords_list.append(tags.text.replace("\n", "").replace("\r", ""))

    pass_write = open(path, "a")

    for n, info in enumerate(passwords_list):
        if len(info.split()) > 6:  # Removes random extra data I recieved from HP request
            continue
        pass_write.write("%-*s".strip("\n") % (108, info))
        if (n + 1) % 5 == 0: pass_write.write("\n")

    pass_write.close()