import urllib.request, urllib.error

url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52020PC0595&from=EN'

try:
    print(f'Getting content from {url} ...')
    resource = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    print('HTTPError: {}'.format(e.code))
except urllib.error.URLError as e:
    print('URLError: {}'.format(e.reason))
else:
    print('Decoding content...')
    content = resource.read().decode(resource.headers.get_content_charset())

    print('Write to file...')
    f = open('htmlCode.html', 'w')

    f.write(content)
    f.close()
    print('Done.')