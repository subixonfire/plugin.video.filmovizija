import urllib, urllib2, re, socket, jsunpack, os,time
from cookielib import CookieJar
from jsunpack import unpack
import resvk

def getRedirect(url, referer ='', cj = ''):
    req = urllib2.Request(url)
    if not referer == '':
        req.add_header('Host', referer.split('/')[2])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    f = opener.open(req)
    return f.url

def gethtml(url, data ='', referer = ''):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        if not referer == '':
            req.add_header('Referer', referer)
        if data == '':
            response = urllib2.urlopen(req)
        else:
            response = urllib2.urlopen(req, data)     
        htmldoc = str(response.read())
        response.close()
        return htmldoc 
    except :
        print "jebiga gethtml"

def resolve(video, VK_user="", VK_pass=""):

    if True:
        print video
#hosts (filmovizija)
        if video.find("180upload") > -1:
            print "add 180upload support"
        
        if video.find("2gb-hosting") > -1:
            
            html = gethtml(video)
            #print html
            #time.sleep(10)
            k = re.search('<input type="hidden" name="k" value="(.+?)" />', html).group(1)
            data = "k=" + k + "&submit=Continue" 
            html = gethtml(video, data)
            #print html
            js = re.compile ("<script type='text/javascript'>.+?(eval.+?).+?\n</script>", re.DOTALL,).findall(html)[0]
            jsstr = unpack(js)
            print jsstr
            video = re.search("addVariable\('file','(.+?)'\)" , jsstr).group(1)
            
        if video.find("dailymotion") > -1:
            
            html = gethtml(video)
            
            fv = re.search('var flashvars = {"(.+?)"};', html).group(1)
            fvu = urllib.unquote_plus(fv)
            video = re.search('"video_url":"(.+?)"', fvu).group(1)
            video = urllib.unquote_plus(video)
            video = getRedirect(video)
        
        
        if video.find("boojour") > -1 or video.find("colenak") > -1 or video.find("loombo") > -1:
        
            video = video.replace("loombo.pm" , "colenak.eu")
            
            html = gethtml(video)
            
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            furl = video
            #string = re.search('<input type="hidden" value="(.+?)" class="textbox" name="(.+?)" id="a" disabled="disabled">', html)
            string =re.compile ('<input type="hidden" value="(.+?)" class="textbox" name="(.+?)".+?>', ).findall(html)
            #if string:
                #stringvalue = string.group(1)
                #stringname = string.group(2)
            print string
            data = string[0][1] + "=" + string[0][0] + "&"  + "&x=201&y=127" 
            html = gethtml(video, data, video)
            #print html
            video = re.search("url: '(.+?)'," , html).group(1)
            print video
            bjcookie = ""
            for cookie in cj:
                print cookie.name, cookie.value
                if bjcookie == "":
                    bjcookie = cookie.name + "=" + cookie.value
                else:
                    bjcookie = bjcookie + ";" + cookie.name + "=" + cookie.value     
            #urllib.urlretrieve (video, "video.avi")
            cmd = "wget --header='Cookie:" + bjcookie + "' -O \"/tmp/video.avi\" \"" + video + "\""
            print cmd
            os.system(cmd)
            video = "/tmp/video.avi" 
        
        if video.find("faststream") > -1:
            
            html = gethtml(video)
            time.sleep(5)
            
            fid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
            fhash = re.search('<input type="hidden" name="hash" value="(.+?)">', html).group(1)
            
            data = "op=download1&usr_login=&id=" + fid + "&fname=" + fname + "&referer=&hash=" + fhash + "&imhuman=Proceed+to+video" 
            html = gethtml(video, data)
            
            video = re.search('file: "(.+?)",' , html).group(1)
            
        if video.find("filebox") > -1: #nedovrsen treba cookie ali jos nesto fali http://www.filebox.com/41p19tl47dj0
            
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            html = gethtml(video)
            time.sleep(15)
            
            fid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            frand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
            
            data = "op=download2&id=" + fid + "&rand=" + frand + "&referer=" + video + "&method_free=&method_premium=&down_direct=1" 
            html = gethtml(video, data, video)
            print html
            video = re.search("play\('(.+?)'\)" , html).group(1)
            
        if video.find("flashx.tv") > -1:
            
            if not video.find("play.flashx.tv") > -1:
                html = gethtml(video)
                video = re.search('<iframe width="620" height="400" src="(.+?)" frameborder="0" allowfullscreen></iframe>', html).group(1)
            html = gethtml(video)
            data = re.search('<span class="auto-style6">\n\t\t<a href="(.+?)"', html).group(1)
            html = gethtml(data)
            print html
            data1 = re.search('data="http\:\/\/play\.flashx\.tv\/nuevo\/player\/player\.swf\?config=(.+?)"', html).group(1)
            html = gethtml(data1)
            print html
            video = re.search('<file>(.+?)</file>', html).group(1)
        
        if video.find("fliiby") > -1:
            html = gethtml(video)
            video = re.search("'file','(.+?)'", html).group(1)
        
        if video.find("limevideo") > -1:
            html = gethtml(video)
            fid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
            data = "op=download1&usr_login=&id=" + fid + "&fname=" + fname + "&referer=&method_free=Continue+to+Video"
            fid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
            data = "op=download2&id=" + fid + "&rand=" + rand + "&referer=&method_free=Continue+to+Video&method_premium=&down_direct=1"
            js = re.compile ("<script type='text/javascript'>(eval.+?)\n</script>", re.DOTALL,).findall(html)[0]
            jsstr = unpack(js)
            video = re.search("'file','(.+?)'" , jsstr).group(1)
            
            
            
        if video.find("movzap") > -1:
            html = gethtml(video)
            video = re.search('file: "(.+?)",', html).group(1)
        
        if video.find("nosvideo") > -1:
            html = gethtml(video)
            fid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
            data = "op=download1&id=" + fid + "&rand=&referer=&usr_login=&fname=" + fname + "&method_free=&method_premium=&down_script=1&method_free=Continue+to+Video" 
            html = gethtml(video,data)
            js = re.compile ("<script type='text/javascript'>(eval.+?)\n</script>", re.DOTALL,).findall(html)[0]
            jsstr = unpack(js)
            playlist = re.search('playlist=(.+?)&', jsstr).group(1)
            html = gethtml(playlist)
            video = re.search('<file>(.+?)</file>', html).group(1)
                  
# end
        if video.find("vk.com") > -1:
            if not video.find("video_ext.php") > -1:
                print "short vk link! " + video
                
                cj = CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)
            
                html = gethtml("http://vk.com")
                var_ip_h = re.search("ip_h: '(\d|\w*)'", html).group(1)
                var_hash = re.search("hash: '(\d|\w*)'", html).group(1)
                
                var_email = VK_user                           
                var_pass = VK_pass
                
                html = gethtml("https://login.vk.com/?act=login?", "act=login&q=1&al_frame=1&expire=&captcha_sid=&captcha_key=&from_host=login.vk.com&ip_h=" + var_ip_h + "&email=" + var_email + "&pass=" +var_pass )
                
                oid = video.split("video")[1].split("_")[0]
                vid = video.split("video")[1].split("_")[1]
                html = gethtml("http://vk.com/al_video.php","act=video_embed_box&al=1&oid=" + oid + "&vid=" + vid, video)
                
                video = re.search('iframe src=&quot;(.+?)";', html).group(1)
            
            video = resvk.getURL(video)
        
        elif video.find("noobroom") > -1:
            html = gethtml("http://noobroom.com")
            domain = re.search('<input class="tbz" type="text" size="24" value="(.+?)">',html).group(1)
            video = re.sub("http://noobroom[0-9]\.com", domain, video)
            print "Corect domain: " + domain        
            user = "saintomer1866@o2.co.uk"
            passw = "markatnoobroom"
            cj = False
            login_url = domain + "/login2.php"
            login_data = "email=" + user + "&password=" + passw + "&remember=on"
            
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            #get first cookie so you can login / print login page
            html = gethtml(domain + "/")
            
            #login to get two more cookies
            html = gethtml(login_url, login_data)
            print "Loged in as: " + user 
            
            html = gethtml(video)
            link = video
            vfile = re.search('"file": "(.+?)",', html).group(1)
            video = re.search('"streamer": "(.+?)",', html).group(1)
            video = video + "&file=" + vfile + "&start=0"
            video = getRedirect(video, link, cj)
        
        elif video.find("http://185.8.196.237") > -1:
            html = gethtml(video)
            domain = re.search('<input class="tbz" type="text" size="24" value="(.+?)">',html)
            if domain:
                print "domain change"
                domain = domain.group(1)
                video = re.sub("http://185.8.196.237", domain, video)
            
            html = gethtml(video)
            link = video
            vfile = re.search('"file": "(.+?)",', html).group(1)
            video = re.search('"streamer": "(.+?)",', html).group(1)
            video = video + "&file=" + vfile + "&start=0"
            video = getRedirect(video, link)
            
        elif video.find("movie2k.to") > -1:
            video = video.replace("2k","4k")
            html = gethtml(video,'',video)
            stream2k = re.search('<iframe .+? src="(http\://embed\.stream2k\.com.+?)"></iframe>', html)
            
            if stream2k:
                server = stream2k.group(1)
                html = gethtml(server,'', video)
                video = re.search("file: '(.+?)',", html).group(1)
                randsrv = randint(1, 60)
                video = re.sub("http://server[0-9]*?\.stream2k\.com", "http://server" + str(randsrv) + ".stream2k.com", video)
                
            else:
                print "stream2k > search for putlocker link as backup host"
                title = re.search('http://www.movie4k.to/(.+?)-watch-movie-[0-9]*?\.html', video).group(1)
                althost = re.compile ('<a href="(.+?)">.+?<img border="0" style=".+?" src=".+?" alt="Putlocker.+?" title="Putlocker.+?" width="16">',re.DOTALL,).findall(html)
                print althost
                
        elif video.find("gorillavid") > -1 or video.find("daclips") > -1 or video.find("movpod") > -1 :
            
            video = video.replace("gorillavid.com/" , "gorillavid.in/") #dodas ovo
            
            html = gethtml(video)
                
            vid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">' , html).group(1)

            data = "op=download1&usr_login=&id=" + vid + "&fname=" + fname + "&referer=&channel=cna&method_free=Free+Download"
    
            html = gethtml(video, data)
  
            video = re.search('file: "(.+?)",' , html).group(1)    
        
        elif video.find("videoweed") > -1 or video.find("novamov") > -1 or video.find("nowvideo") > -1 or video.find("divxstage") > -1 or video.find("movshare") > -1:
            
            html = gethtml(video)
            from jsunwise import unwise_process
            html = unwise_process(html)
            #print html 
            
            fvdomain = re.search('flashvars.domain="(.+?)";', html).group(1)
            fvfile = re.search('flashvars.file="(.+?)";', html).group(1)
            fvfilekey = re.search('flashvars.filekey=(.+?);', html).group(1)
            fvfilekey = re.search('var ' + fvfilekey + '="(.+?)";', html).group(1)
            api = fvdomain + "/api/player.api.php?user=undefined&codes=1&file=" + fvfile + "&pass=undefined&key=" + fvfilekey
            
            html = gethtml(api)
            
            video = re.search('url=(.+?)&', html).group(1)
            
            video = urllib.unquote_plus(video)
            
        elif video.find("allmyvideos") > -1:
        
            html = gethtml(video)
            
            vid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">' , html).group(1)
            
            data = "op=download1&usr_login=&id=" + vid + "&fname=" + fname + "&referer=&method_free=1"
            
            html = gethtml(video, data)
  
            video = re.search('"file" : "(.+?)",' , html).group(1)    
        
        elif video.find("divxhosted") > -1:
        
            html = gethtml(video)
            
            xstr = re.search("xajax_load_player_eng\('(.+?)'", html).group(1)
            xms = str(round(time.time() * 1000))
            
            api = "http://divxhosted.com/Xajax/saveaction/"
            data = "xjxfun=load_player_eng&xjxr=" + xms + "&xjxargs[]=S" + xstr + "&xjxargs[]=N2"
            
            html = gethtml(api, data)
  
            video = re.search('&file=(.+?)"' , html).group(1)
        
        elif video.find("filenuke") > -1:
            
            html = gethtml(video)
                
            vid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">' , html).group(1)

            data = "op=download1&usr_login=&id=" + vid + "&fname=" + fname + "&referer=&method_free=Free"
    
            html = gethtml(video, data)
            
            js = re.compile ("<script type='text/javascript'>(eval.+?)\n</script>", re.DOTALL,).findall(html)[1]
            
            jsstr = unpack(js)
            
            video = re.search("addVariable\('file','(.+?)'\)" , jsstr).group(1)
        
        elif video.find("watchfreeinhd") > -1:
                
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            html = gethtml(video)
           
            data = "agree=Yes%2C+let+me+watch"
            
            html = gethtml(video, data)
            
            video = re.search('<a href="(.+?)" id="player" name="player">', html).group(1)
            
        elif video.find("sockshare") > -1:
                
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            html = gethtml(video)
            
            vhash = re.search('<input type="hidden" value="(.+?)" name="hash">', html).group(1)
           
            data = "hash=" + vhash + "&confirm=Continue+as+Free+User"
            
            html = gethtml(video, data)
            
            vplaylist = "http://www.sockshare.com" + re.search("playlist: '(/get_file.php?.+?)',", html).group(1)
            
            html = gethtml(vplaylist)
            
            video = re.search('<media:content url="(.+?)" type="video/x-flv"  duration="[0-9]*?" />', html).group(1).replace("&amp;", "&")    
        
        elif video.find("putlocker") > -1:
                
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            html = gethtml(video)
            
            vhash = re.search('<input type="hidden" value="(.+?)" name="hash">', html).group(1)
           
            data = "hash=" + vhash + "&confirm=Continue+as+Free+User"
            
            html = gethtml(video, data)
            
            vplaylist = "http://www.putlocker.com" + re.search("playlist: '(/get_file.php?.+?)',", html).group(1)
            
            html = gethtml(vplaylist)
            
            video = re.search('<media:content url="(.+?)" type="video/x-flv"  duration="[0-9]*?" />', html).group(1).replace("&amp;", "&")    
        print video
        return video
    #except:
        #print "jebiga"
        
if __name__ == '__main__':
    import sys
    #try:
    x = resolve(sys.argv[1])
    print x
    os.system("vlc \"" + x + "\"") 
    #except:
        #print "jebiga main"        
