import urllib.request
from bs4 import BeautifulSoup

url = 'https://lawphil.net/judjuris/juri2016/aug2016/gr_189185_2016.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as response:
    html = response.read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

start = text.find('ORDINANCE NO. 0309-07')
end = text.find('Mayor Rodrigo R. Duterte', start)
if end == -1:
    end = start + 5000

print(text[start:end+500])

