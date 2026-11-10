import urllib.request
from bs4 import BeautifulSoup

url = 'https://lawphil.net/judjuris/juri2005/apr2005/gr_118127_2005.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    print('Fetched characters:', len(text))
    # Look for Ordinance No. 7783
    pos = text.find('7783')
    if pos != -1:
        print('Found 7783 at:', pos)
        print(text[pos-200:pos+3500])
except Exception as e:
    print('Error:', e)

