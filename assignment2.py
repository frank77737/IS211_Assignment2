import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        csv_data = response.read().decode('utf-8')
    return csv_data
    pass

def processData(file_content):
    pass


def displayPerson(id, personData):
    pass

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
