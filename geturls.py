import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

def find_http_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for anchor in soup.find_all('a', href=True):
        href = anchor['href']

        full_url = urljoin(base_url, href)
        parsed_full_url = urlparse(full_url)
        if parsed_full_url.netloc == urlparse(base_url).netloc:
            links.add(full_url)

    return sorted(links)

def main():
    parser = argparse.ArgumentParser(description="Find all HTTP links")
    parser.add_argument('-u', '--url', action='append', required=True, help="The URLs to search for links")
    parser.add_argument('-o', '--output', choices=['stdout', 'json'], default='stdout', help="Output format")

    args = parser.parse_args()
    all_links = set()
    result = {}

    for base_url in args.url:
        links = find_http_links(base_url)
        result[base_url] = [urlparse(link).path for link in links]
        all_links.update(links)

    if args.output == 'stdout':
        for link in sorted(all_links):
            print(link)
    elif args.output == 'json':
        unique_paths = {}
        for base_url in result:
            unique_paths[base_url] = list(set(urlparse(link).path for link in result[base_url]))
        
        print(json.dumps(unique_paths, indent=4))
if __name__ == "__main__":
    main()

