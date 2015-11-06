import socks
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
import socket
socket.socket = socks.socksocket
import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')]

from lxml import html
import json
import os


from multiprocessing import Pool


def getURL(url):
	print(url)
	try:
		j = opener.open(url)
	except:
		return False

	html_text = j.read()
	tree = html.fromstring(html_text)

	scholar = []
	for elt in tree.xpath("//div[@class='gs_ri']"):
		try:
			title = elt.xpath(".//h3[@class='gs_rt']")[0].text_content().replace('[HTML]','').replace('[CITATION]','').replace('[PDF]','').strip()
			title = unicode(title.encode('utf-8'), 'ascii', 'ignore')
			abstract = elt.xpath(".//div[@class='gs_rs']")[0].text_content().replace('[HTML]','').strip()
			abstract = unicode(abstract.encode('utf-8'), 'ascii', 'ignore').replace('Abstract ','')
			author_list = elt.xpath(".//div[@class='gs_a']")[0].text_content()
			authors = author_list.split('-')[0].strip()
			year = [int(s) for s in author_list.split() if s.isdigit()][0]
			authors = unicode(authors.encode('utf-8'), 'ascii', 'ignore')
                        try:
                            citations = int(elt.xpath(".//div[@class='gs_fl']/a")[0].text_content().split('Cited by')[1])
                        except:
                            citations = 0
                        data = {'title': title, 'authors': authors, 'citations': citations, 'year':year, 'abstract': abstract, 'url':url}
                        scholar.append(data)
		except:
			print('EXCEPTION')
			print(elt.text_content())

	if len(scholar) == 0:
		return False

	with open('data.json','a') as f:
		f.write(json.dumps(scholar) + '\n')
	with open('urls.json','a') as f:
		f.write(json.dumps(url) + '\n')

	return True


urls = []
journals = ['science','nature','plos%20one']
for year in range(2000,2016):
	for start in range(0,1000,10):
		for journal in journals:
			urls.append('http://scholar.google.com/scholar?start=%(start)s&lr=lang_en&hl=en&as_publication=%(journal)s&as_ylo=%(year)s&as_yhi=%(year)s' % {'start':start,'year':year, 'journal':journal})

doneUrls = []
try:
	with open('urls.json','r') as f:
		for line in f:
			doneUrls.append(json.loads(line))
except:
	pass

print(len(urls))
urls = list(set(urls) - set(doneUrls))
print(len(urls))

#print(getURL('http://scholar.google.com/scholar?start=40&lr=lang_en&hl=en&as_publication=nature&as_ylo=2000&as_yhi=2000'))
for i in range(0,len(urls),1):
	#p = Pool(2)
	#tryUrls = urls[i:i+4]
	#results = p.map(getURL,tryUrls)
	results = [getURL(urls[i])]
	if (sum(results)==0):
		print('restarting tor')
		os.system('/etc/init.d/tor restart')
		j = opener.open('http://icanhazip.com')
		print(j.read())
