# Crawl baidu baike
from bs4 import BeautifulSoup
from urllib import error,request,parse
initurl="http://baike.baidu.com/item/R/3041133"
urlold=set()
urlnew=set()
urlnew.add(initurl)
count=0
results=list()
fout=open("baike.txt",'w')
# connect
while len(urlnew)!=0:
	url=urlnew.pop()
	if url in urlold:
		continue
	try:
		contents=request.urlopen(url).read().decode()
		soup1=BeautifulSoup(contents,'html.parser')
		soup=soup1.find("div",class_="content")
		title=soup.find("h1")
		title=title.get_text()
		summary=soup.find("div",class_="lemma-summary").get_text()
		url1=soup.find_all("a")
	except:
		continue
	if len(summary)==0 or summary is None:
		continue
	for i in url1:
		try:
			url2=i["href"]
		except:
			continue
		if not url2.startswith("/item"):
			continue
		url2="http://baike.baidu.com"+url2
		if url2 in urlold:
			continue
		elif url2 not in urlnew:
			urlnew.add(url2)
	count=count+1
	fout.write("==========================crawl ")
	fout.write(str(count))
	fout.write(" times======================\n")
	urlold.add(url)
	fout.write("url: ")
	fout.write(url)
	fout.write("\n")
	fout.write("title: ")
	fout.write(title)
	fout.write("\n")
	fout.write("summary: ")
	fout.write(summary)
	fout.write("\n")
	results.append({"url":url,"title":title,"summary":summary})
	if count==1000:
		break