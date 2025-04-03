#!/usr/bin/python3

"""
Find comments in webpages and HTML files.
"""

import argparse
import requests
from bs4 import BeautifulSoup, Comment


def get_soup(html: str) -> BeautifulSoup:
    """Parse an HTML string as a BeautifulSoup object."""
    try:
        soup = BeautifulSoup(html, features='html.parser')
    except UnicodeDecodeError:
        print('[!] HTML is not UTF-8 encoded. Is this text?')
        return None

    return soup

def get_soup_from_file(file_name: str) -> BeautifulSoup:
    """Read an HTML file and parse as a BeautifulSoup object."""
    print(f'[*] looking for comments in {file_name}')
    with open(file_name, encoding='utf-8') as fp:
        soup = get_soup(fp)
    return soup

def get_soup_from_site(url: str) -> BeautifulSoup:
    """Get a website and parse as a BeautifulSoup object."""
    print(f'[*] looking for comments in {url}')
    try:
        r = requests.get(url, timeout=10)
    except requests.Timeout:
        print(f'[!] request to site timed out: {url}')
    except requests.RequestException as e:
        print(f'[!] exception while making request to site: {str(e)}')
        return None

    soup = get_soup(r.text)
    return soup

def print_comments(soup: BeautifulSoup):
    """Print comments found in a BeautifulSoup object."""
    comments = soup.find_all(string=lambda x: isinstance(x, Comment))
    num_comments = len(comments)

    if num_comments == 0:
        print('[-] no comments found')
        return

    print(f'[+] {num_comments} comments found:')
    print('-' * 25)
    for comment in comments:
        print(comment)
        print('-' * 25)
    print('[*] all comments printed')

def arg_parse():
    """Handle command line arguments."""
    parser = argparse.ArgumentParser(
                        prog='comment extractor',
                        description='extracts comments from html files and webpages')
    parser.add_argument('-u', '--url', action='store')
    parser.add_argument('-f', '--file', action='store')

    return parser.parse_args()


def main():
    """Main function."""
    args = arg_parse()
    if args.file:
        soup = get_soup_from_file(args.file)
    elif args.url:
        soup = get_soup_from_site(args.url)
    else:
        print('[x] run with --help for usage')
        return

    if soup:
        print_comments(soup)

if __name__ == '__main__':
    main()
