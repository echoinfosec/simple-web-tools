#!/usr/bin/python3

import argparse
import requests
import sys
from bs4 import BeautifulSoup, Comment

def getSoup(html):
    try:
        soup = BeautifulSoup(html, features='html.parser')
    except Exception as e:
        print('exception while parsing html:', format(e))
        sys.exit()
    
    return soup

def getSoupFromFile(fileName):
    print('[-] looking for comments in', fileName)
    with open(fileName) as fp:
        soup = getSoup(fp)
    return soup

def getSoupFromSite(url):
    print('[-] looking for comments in', url)
    try:
        r = requests.get(url)
    except Exception as e:
        print('exception while making request to site:', format(e))
        sys.exit()

    soup = getSoup(r.text)
    return soup

def printComments(soup):
    comments = soup.find_all(string=lambda x: isinstance(x, Comment))
    numComments = len(comments)
    
    if numComments == 0:
        print('[-] no comments found')
        return
    
    print('[-] %s comments found:' % numComments)
    print('-' * 25)
    for comment in comments:
        print(comment)
        print('-' * 25)
    print('[-] all comments printed')

def argParse():
    parser = argparse.ArgumentParser(
                        prog='comment extractor',
                        description='extracts comments from html files and webpages')
    parser.add_argument('-u', '--url', action='store')
    parser.add_argument('-f', '--file', action='store')
    
    return parser.parse_args()


def main():
    args = argParse()
    if args.file:
        soup = getSoupFromFile(args.file)
    elif args.url:
        soup = getSoupFromSite(args.url)
    else:
        print('run "%s --help" for usage' % sys.argv[0])
        sys.exit()
        
    printComments(soup)

if __name__ == '__main__':
    main()


