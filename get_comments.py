#!/usr/bin/python3

import argparse
import requests
import sys
from bs4 import BeautifulSoup, Comment


def get_soup(html):
    try:
        soup = BeautifulSoup(html, features='html.parser')
    except Exception as e:
        print('exception while parsing html:', format(e))
        sys.exit()
    
    return soup

def get_soup_from_file(file_name):
    print('[*] looking for comments in', file_name)
    with open(file_name) as fp:
        soup = get_soup(fp)
    return soup

def get_soup_from_site(url):
    print('[*] looking for comments in', url)
    try:
        r = requests.get(url)
    except Exception as e:
        print('exception while making request to site:', format(e))
        sys.exit()

    soup = get_soup(r.text)
    return soup

def print_comments(soup):
    comments = soup.find_all(string=lambda x: isinstance(x, Comment))
    num_comments = len(comments)
    
    if num_comments == 0:
        print('[-] no comments found')
        return
    
    print('[+] %s comments found:' % num_comments)
    print('-' * 25)
    for comment in comments:
        print(comment)
        print('-' * 25)
    print('[*] all comments printed')

def arg_parse():
    parser = argparse.ArgumentParser(
                        prog='comment extractor',
                        description='extracts comments from html files and webpages')
    parser.add_argument('-u', '--url', action='store')
    parser.add_argument('-f', '--file', action='store')
    
    return parser.parse_args()


def main():
    args = arg_parse()
    if args.file:
        soup = get_soup_from_file(args.file)
    elif args.url:
        soup = get_soup_from_site(args.url)
    else:
        print('run "%s --help" for usage' % sys.argv[0])
        sys.exit()
        
    print_comments(soup)

if __name__ == '__main__':
    main()


