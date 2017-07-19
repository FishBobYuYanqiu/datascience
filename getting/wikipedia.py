#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 # Crawl baidu baike
from bs4 import BeautifulSoup
from urllib import error,request,parse
import pickle
try:
	urlold=pickle.load(open("urlold.txt",'rb'))
	urlnew=pickle.load(open("urlnew.txt","rb"))
	count1=pickle.load(open("count.txt","rb"))
	count=count1
except:
	initurl="https://en.wikipedia.org/wiki/R_(programming_language)"
	urlold=set()
	urlnew=set()
	urlnew.add(initurl)
	count=0
	count1=0
fout=open("wikipedia.txt",'a')
# connect
while len(urlnew)!=0:
	url=urlnew.pop()
	body=str()
	if url in urlold:
		continue
	try:
		contents=request.urlopen(url).read().decode()
		soup=BeautifulSoup(contents,'html.parser')
		title=soup.find("h1")
		title=title.get_text()
		bodies=soup.find_all("div",class_="mw-body-content")
		summary=soup.find("p").get_text()
		for item in bodies:
			body=body+item.get_text()
		url1=soup.find_all("a")
	except:
		continue
	if len(body)==0 or body is None:
		continue
	for i in url1:
		try:
			url2=i["href"]
		except:
			continue
		if not url2.startswith("/wiki/"):
			continue
		url2="https://en.wikipedia.org"+url2
		if url2 in urlold:
			continue
		elif url2 not in urlnew:
			urlnew.add(url2)
	count=count+1
	fout.write("==========================")
	fout.write(str(count))
	fout.write(". ")
	fout.write(title)
	fout.write("======================\n")
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
	fout.write("\n")
	print("=========================",str(count),".",title,"==========================\ntitle:",title,"\nurl:",url,"\nsummary:",summary)
	if count==1000+count1:
		break
pickle.dump(urlold, open('urlold.txt', 'wb'))
pickle.dump(urlnew, open('urlnew.txt', 'wb'))
pickle.dump(count, open('count.txt', 'wb'))