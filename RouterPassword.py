#!/usr/bin/python3
import RouterScrape
import argparse
import platform
import sys
import os
import re

parser = argparse.ArgumentParser(description="Search and download default router usernames and passwords")
p = parser.add_mutually_exclusive_group()
p.add_argument("--listall", help="Lists all available router vendors", action="store_true")
p.add_argument("--search", help="Search for information on a router vendor")
p.add_argument("--download", "--update", help="Update/download list with all router information", action="store_true")
args = vars(parser.parse_args())

LIST_ALL = args["listall"]
SEARCH = args["search"]
DOWNLOAD = args["download"]

if not LIST_ALL and not SEARCH and not DOWNLOAD:
    parser.error('No action requested, add --listall, --search or --download')

if platform.system() == "Windows":
	PASSWORD_FILE = os.path.dirname(os.path.realpath(__file__)) + "\\RouterPasswords.txt"
else:
	PASSWORD_FILE = os.path.dirname(os.path.realpath(__file__)) + "/RouterPasswords.txt"


def download():
    """Download a file containing all information about the routers"""
    try:
        os.remove(PASSWORD_FILE)  # Remove old file (if it exists)
    except FileNotFoundError:
        pass

    router_names = RouterScrape.get_router_names()
    progress = len(router_names)

    for n, name in enumerate(router_names):
        sys.stdout.write("\rGrabbing: %-30s (%d%%)" % (name, int(n / progress * 100)))
        sys.stdout.flush()
        RouterScrape.download_router_info(name, PASSWORD_FILE)


def list_all():
    """List all available router vendors"""
    file_search = open(PASSWORD_FILE, "r").readlines()
    duplicates = []

    for manufacturer in file_search:
        manuf = manufacturer.split(",")[0]

        if manuf in duplicates:  # Skip duplicates
            continue

        duplicates.append(manuf)
        print(manuf)

    print("Total amount: " + str(len(duplicates)))


def search(search_term):
    """Search for keywords and display all matches (comma-separated format)"""
    manuf_list = []
    model_list = []
    protocol_list = []
    username_list = []
    password_list = []

    with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
        file_search = f.read()

    # Match lines containing the search term (case-insensitive)
    search_match = re.findall(rf"(^.*?{re.escape(search_term)}.*?$)", file_search, re.MULTILINE | re.IGNORECASE)

    if not search_match:
        print("[!] Search gave no results")
        return

    print("\nMANUFACTURER,MODEL,PROTOCOL,USERNAME,PASSWORD")
    print("--------------------------------------------------")

    for match in search_match:
        # Split by commas instead of spaces
        match = match.strip().split(",")

        # Fill missing values
        while len(match) < 5:
            match.append("(empty)")

        manuf_list.append(match[0].strip())
        model_list.append(match[1].strip())
        protocol_list.append(match[2].strip())
        username_list.append(match[3].strip())
        password_list.append(match[4].strip())

    # Align columns dynamically
    for i in range(len(manuf_list)):
        print("%-*s   %-*s   %-*s   %-*s   %-*s" %
              (len(max(manuf_list, key=len)), manuf_list[i],
               len(max(model_list, key=len)), model_list[i],
               len(max(protocol_list, key=len)), protocol_list[i],
               len(max(username_list, key=len)), username_list[i],
               len(max(password_list, key=len)), password_list[i]))


if __name__ == "__main__":
    if LIST_ALL:
        if os.path.exists(PASSWORD_FILE):
            list_all()
        else:
            print("[!] RouterPasswords.txt not found. Please use the --download option to get it")

    if SEARCH:
        if os.path.exists(PASSWORD_FILE):
            search(SEARCH)
        else:
            print("[!] RouterPasswords.txt not found. Please use the --download option to get it")

    if DOWNLOAD: download()
