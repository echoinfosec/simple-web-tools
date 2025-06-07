import argparse
import io
import json
from sys import stderr
import requests
from bs4 import BeautifulSoup

def check_file(url):
    try:
        r = requests.get(url, timeout=10)
        buf = io.BytesIO(r.content)
        data = buf.getvalue().decode()
    except requests.Timeout:
        print(f'[!] request for file timed out: {url}', file=stderr)
        return None
    except requests.RequestException as e:
        print(f'[!] exception while making request for file: {url}: {str(e)}', file=stderr)
        return None
    except UnicodeDecodeError:
        print(f'[*] file not unicode, skipping: {url}', file=stderr)
        return None

    results = []
    keywords = ['password', 'email', 'account']
    for keyword in keywords:
        f = data.lower().find(keyword)
        if f > -1:
            start = f - 50
            end = f + len(keyword) + 50
            sample = data[start:end]
            print(f'\n[!] found match for keyword "{keyword}" at {url}', file=stderr)
            print(sample, file=stderr)
            print(file=stderr)
            results.append({'keyword': keyword, 'url': url, 'sample': sample})

    return results

def get_links(url, text):
    directories = []
    files = []

    soup = BeautifulSoup(text, features="html.parser")
    for a_tag in soup.find_all('a'):
        href = a_tag['href']
        if href == '/' or href.startswith('?'):
            continue
        if a_tag.get_text() == 'Parent Directory':
            continue

        full_path = url + href
        if full_path.endswith('/'):
            directories.append(full_path)
        else:
            files.append(full_path)

    return directories, files

def write_output(file_name, data):
    if file_name:
        with open(file_name, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(data, indent=2))
    else:
        print(json.dumps(data, indent=2))

def format_url(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + '/'
    return url

def arg_parse():
    """Handle command line arguments."""
    parser = argparse.ArgumentParser(
            prog='directory spider',
            description='spider open directories for loot')
    parser.add_argument('-u', '--url', required=True, help='url to spider')
    parser.add_argument('-o', '--output', help='output file name')
    parser.add_argument('-v', action='store_true', help='also show file discoveries')
    parser.add_argument('-vv', action='store_true', help='also show directory discoveries')
    parser.add_argument('-vvv', action='store_true', help='also show url requests')

    return parser.parse_args()

def main():
    args = arg_parse()
    results = []
    queue = [format_url(args.url)]
    history = []

    while queue:
        url = queue.pop()
        history.append(url)

        if args.vvv:
            print(f'[*] visiting: {url}', file=stderr)

        try:
            r = requests.get(url, timeout=10)
            text = r.text
        except requests.Timeout:
            print(f'[!] request to site timed out: {url}', file=stderr)
            continue
        except requests.RequestException as e:
            print(f'[!] exception while making request to site: {str(e)}', file=stderr)
            continue


        directories, files = get_links(url, text)
        for directory in directories:
            if directory not in queue and directory not in history:
                if args.vv:
                    print(f'[*] found new directory: {directory}', file=stderr)
                queue.append(directory)

        for file in files:
            if file not in history:
                if args.v or args.vv:
                    print(f'[*] found new file: {file}', file=stderr)
                result = check_file(file)
                if result:
                    results.extend(result)
                history.append(file)

    write_output(args.output, results)


if __name__ == '__main__':
    main()
