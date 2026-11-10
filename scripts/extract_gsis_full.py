import urllib.request
from bs4 import BeautifulSoup

url = 'https://lawphil.net/judjuris/juri2005/aug2005/gr_127383_2005.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    print('Fetched characters:', len(text))
    # Look for ordinance or tax assessment
    pos = text.find('Ordinance')
    if pos != -1:
        print('Found Ordinance at:', pos)
        print(text[pos-200:pos+1500])
    else:
        print('First 1500 chars:')
        print(text[:1500])
except Exception as e:
    print('Error:', e)

