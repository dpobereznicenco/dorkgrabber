import re,sys,time,urllib
from StringIO import StringIO
from urlparse import urlparse
found=[]
try:
	found=open('found.txt','a').read().splitlines()
except Exception,e:
	pass
foundh=[]
try:
	import pycurl
except Exception,e:
	print "I need pycurl to work"
	exit()
class scanner():
	def __init__(self):
		self.added=0
	def request(self,url):
	    for i in range(3):
	        try:
	        	
	            c=pycurl.Curl()

	            c.setopt(c.URL,url)
	            c.setopt(c.USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0')
	            c.setopt(c.SSL_VERIFYHOST,0)
	            c.setopt(c.SSL_VERIFYPEER,0)
	            c.setopt(c.FOLLOWLOCATION,True)
	            c.setopt(c.COOKIEFILE,"./cookie.txt")
	            c.setopt(c.COOKIEJAR,"./cookie.txt")
	            sHtml=StringIO()
	            c.setopt(c.TIMEOUT,40)
	            c.setopt(c.WRITEFUNCTION,sHtml.write)
	            c.perform()
	            c.close()
	            html=sHtml.getvalue()
	            sHtml.close()
	            time.sleep(1)
	            return html
	        except Exception,e:
	            print str(e)
	            continue
	    return ""
	def grab(self,html):
		global found,foundh
		rez=re.findall('\<h3 class=\"r\"\>\<a href\=\"(.*?)\"',html)
		if len(rez)==0:
			sys.exit(0)
		added=False
		for r in rez:
			url=r.replace("&amp;","&")
			if url not in found:
				added=True
				found.append(url)
				open('found.txt','a').write(url+'\n')
				u=urlparse(url)
				if u.netloc not in foundh:
					open('hosts.txt','a').write(u.netloc+'\n')
					foundh.append(u.netloc)
		if not added:
			self.added+=1
		else:
			self.added=0
		if self.added==4:
			print "[!] Nimic de adaugat in plus exit"

			sys.exit(0)
	def getFormData(self,html):
		url=""
		continue_url=re.findall('\<input type=\"hidden\" name=\"continue\" value=\"(.*?)\"\>',html)
		continueu=continue_url[0].replace("&amp;","&")
		continueu=urllib.quote_plus(continueu)
		ids=re.findall('\<input type=\"hidden\" name=\"id\" value=\"(.*?)\">',html)
		ids=ids[0]
		url="continue="+continueu+"&id="+ids
		return url
	def grabCaptchaLink(self,html):
		rez_catpcha=re.findall('<img src="/sorry/image?(.*?)"',html)
		rez_catpcha[0]=rez_catpcha[0].replace("&amp;","&")
		rez=self.request("https://ipv4.google.com/sorry/image?"+rez_catpcha[0])
		open('image.jpg','wb').write(rez)


dork=sys.argv[1]
throw=range(0,100)
if len(sys.argv)>2:
	if "-" in sys.argv[2]:
		split=sys.argv[2].split("-")
		throw=range(int(split[0]),int(split[1]))
	else:
		throw=range(0,int(sys.argv[2]))

s=scanner()




got_image=False
add=0
for i in throw:
	print "[+] Page "+str(i)
	rez=s.request("http://www.google.com/search?q="+dork+"&filter=0&start="+str(i*10))
	open('rez.html','w').write(rez)

	if '/sorry/image?' in rez:

		while '/sorry/image?' in rez:
			s.grabCaptchaLink(rez)
			cpt_url=s.getFormData(rez)
			#print cpt_url
			code=raw_input("Captcha:")
			rez=s.request("https://ipv4.google.com/sorry/CaptchaRedirect?"+cpt_url+"&captcha="+code+"&submit=send")

	links=s.grab(rez)
