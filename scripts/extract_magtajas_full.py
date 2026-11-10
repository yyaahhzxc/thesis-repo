import urllib.request
from bs4 import BeautifulSoup

url = 'https://lawphil.net/judjuris/juri1994/jul1994/gr_111097_1994.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    print('Fetched characters:', len(text))
    # Look for Ordinance No. 3353 and 3375
    pos1 = text.find('3353')
    if pos1 != -1:
        print('Found 3353 at:', pos1)
        print(text[pos1-200:pos1+1500])
    pos2 = text.find('3375')
    if pos2 != -1:
        print('Found 3375 at:', pos2)
        print(text[pos2-200:pos2+1500])
except Exception as e:
    print('Error:', e)

