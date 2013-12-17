import urllib,urllib2,re,xbmcplugin,xbmcgui
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urlresolver
import socket
import tempfile,os
#print "socket: " + socket.getdefaulttimeout() 
socket.setdefaulttimeout(60)
net = Net()


_addon = Addon('plugin.video.filmovizija', sys.argv)
VK_user = _addon.get_setting('VK_user')
VK_pass = _addon.get_setting('VK_pass')

#print VK_user, VK_pass

def HOME():
        addDir( 'Movies','http://www.filmovizija.com/browse-movies-videos-1-artist.html','1','')
        addDir( 'EX-YU Movies','http://www.filmovizija.com/browse-ex-yu_movies-videos-1-artist.html','2','')
        addDir( 'Series','http://www.filmovizija.com/browse-Series-videos-1-artist.html','1','')
        addDir( 'EX-YU Series','http://www.filmovizija.com/browse-ex-yu_series-videos-1-artist.html','1','')
        addDir( 'Cartoon','http://www.filmovizija.com/browse-cartoon-videos-1-artist.html','1','')
        addDir( 'Animated','http://www.filmovizija.com/browse-animated-videos-1-artist.html','2','')
        addDir( 'Documentary','http://www.filmovizija.com/browse-Documetary-videos-1-date.html','2','')
        addDir( 'Search','none','0','')
        ###Movies EX-YU Movies Series EX-YU Series Documetary Animated Cartoon


def SEARCH():
        print "search()"
        #http://www.filmovizija.com/search.php?keywords=ana
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search:')
        keyboard.setDefault('')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_string = keyboard.getText()
                search_url = "http://www.filmovizija.com/search.php?keywords=" + urllib.quote_plus(search_string) + "&page=1"
       	       	html = gethtml(search_url)
       	       	try:
       	       	       	listpages  = re.compile ('<div class="pagination">(.+?)</div>', re.DOTALL,).findall(html)[0]
       	       	       	pages = re.compile ('<a href=".+?">([0-9]*?)</a>', re.DOTALL,).findall(listpages)
       	       	       	lastpage = pages[len(pages) -1]
       	       	except:
       	       	       	lastpage = 1

       	       	if int(lastpage) > 11:
       	       	       	lastpage = 10
       	       	movies = []
    
       	       	for z in range(1, int(lastpage) +1):
       	       	       	xurl = re.sub("&page=1", "&page=" + str(z), search_url)
       	       	       	print xurl
       	       	       	html = gethtml(xurl)
       	       	       	restring = '''<div class="video_i">
			<a href="(.+?)">
			<img src="(.+?)"  alt="(.+?)" class="imag" width="116" height="87" />.+?
			</a>
			<span class="artist_name">(.+?)</span> <span class="song_name">(.+?)</span>'''
       	       	       	moviesx = re.compile (restring, re.DOTALL,).findall(html)
       	       	       	movies = movies + moviesx
       	       	
       	       	for url,thumbnail,name,x,y in movies:
       	       	       	addDir(name + " " + x,url,3,thumbnail)
       	       	


def CATEGORIES(url):
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        #response = urllib2.urlopen(req)
        #html=response.read()
        #response.close()
        html = gethtml(url)
        listcats  = re.compile ('<div id="list_subcats">(.+?)</div>', re.DOTALL,).findall(html)[0]
        match = re.compile ('<a href="(.+?)">(.+?)</a>', re.DOTALL,).findall(listcats)
        for url,name in match:
                addDir(name,url,2,"")
                
def LIST(url):

       	print "# filmovizija liststart " + url 
       	
       	xurl = url.replace("-date", "-artist")
       	html = gethtml(url)
       	try:
       	       	listpages  = re.compile ('<div class="pagination">(.+?)</div>', re.DOTALL,).findall(html)[0]
       	       	pages = re.compile ('<a href=".+?">([0-9]*?)</a>', re.DOTALL,).findall(listpages)
       	       	lastpage = pages[len(pages) -1]
       	except:
       	       	lastpage = 1
       	#print lastpage
       	movies = []
    
       	for z in range(1, int(lastpage) +1):
       	#for z in range(0,1):
       	       	xurl = re.sub("-[0-9]*?-", "-" + str(z) + "-", xurl)
       	       	print xurl
       	       	html = gethtml(xurl)
       	       	restring = '''<div class="video_i">
			<a href="(.+?)">
			<img src="(.+?)"  alt="(.+?)" class="imag" width="116" height="87" />.+?
			</a>
			<a href=".+?">
			<span class="artist_name">(.+?)</span> <span class="song_name">(.+?)</span>'''
       	       	moviesx = re.compile (restring, re.DOTALL,).findall(html)
       	       	print moviesx
       	       	movies = movies + moviesx
       	       	#match=re.compile('').findall(link)
        
         #('http://www.filmovizija.com/movie/the-incredible-hulk-2008-video_b6ac5a660.html', 'http://www.filmovizija.com/omoti/IncrHulk.jpg', 'The Incredible Hulk (2008)', 'Movie', 'The Incredible Hulk (2008)')
       	for url,thumbnail,name,x,y in movies:
       	       	addDir(name + " " + x,url,3,thumbnail)
                

def VIDEO(url,name):
		
		#tmp hack, fix to use urlresolver
		from res import resolve
		
		html = gethtml(url)
		data = re.compile ('jwplayer\("Playerholder"\)\.setup\({(.+?)}\);',re.DOTALL,).findall(html)
		videohost = re.search('{link:"(.+?)"}', html).group(1)
		subtitles = re.search('{file:"(.+?)", fontsize:"22", back: true, color:".+?"}', html).group(1) 
		#print "data: " + data[0] + "\n\n\n"
		srtfile = os.path.join(tempfile.gettempdir(),"filmovizija.srt")
		try:
				srt = open(srtfile, "w")
				subtitles = gethtml(subtitles,'',url)
				srt.write(subtitles)
				srt.close()
		except:
				pass
		print "videohost: " + videohost
		print "subtitles: " + srtfile
		#videofile = resolve(videohost) 
		videofile = urlresolver.HostedMediaFile(videohost).resolve()
		if videofile == videohost or videofile == False :
				videofile = resolve(videohost, VK_user, VK_pass)		
		print "videofile: " + str(videofile)
		x = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		listitem = xbmcgui.ListItem(name)
		listitem.setInfo('video', {'Title': name })
		listitem.setProperty('IsPlayable', 'true')
		#x.setSubtitles("/tmp/filmovizija.srt")
		#x.play(videofile, listitem)
		listitem.setPath(videofile)
		listitem.setProperty('IsPlayable', 'true')
		#xbmcplugin.setResolvedUrl(videofile), True, listitem)
		x.play(videofile, listitem)
		#import time
		xbmc.sleep(1000)
		
		x.setSubtitles(srtfile)
		return True

def gethtml(url, data ='', referer = 'http://filmovizija.com/'):
       	if True:
               	req = urllib2.Request(url)
               	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36')
               	#req.add_header('Connection', 'keep-alive')
               	#Connection: keep-alive

               	if not referer == '':
       	       	       	req.add_header('Referer', referer)
       	       	if data == '':
       	       	       	response = urllib2.urlopen(req)
       	       	else:
       	       	       	response = urllib2.urlopen(req, data)     
       	       	htmldoc = str(response.read())
       	       	response.close()
       	       	return htmldoc 
       	#except :
       	       	#print "jebiga gethtml"  

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

params=get_params()
url=None
name=None
mode=None

print "filmovizija start" 
print "call: " + sys.argv[0] + sys.argv[1] + sys.argv[2]
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print "mode = 0"
        HOME()
       
elif mode==1:
        print "mode1: "+url
        CATEGORIES(url)
        
elif mode==2:
        print "mode2: "+url
        LIST(url)
        
elif mode==3:
        print "mode3: "+url
        VIDEO(url,name)
        
elif mode==0:
        print "search"
        SEARCH()         


if not mode == 3:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))                
