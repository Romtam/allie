#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, sys, random, re, urllib2, json, time, platform, os, string, HTMLParser, ssl

#functions

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def privmsg(to, message):
    return irc.send("PRIVMSG "+to+" :"+message+"\r\n")

def reply(to, message):
    return irc.send("PRIVMSG "+to+" :"+sender+": "+message+"\r\n")

def notice(to, message):
    return irc.send("NOTICE "+to+" :"+message+"\r\n")

def done():
    return irc.send("PRIVMSG "+sendto+" :"+sender+": Done.\r\n")

def error(to, message, msgtype="PRIVMSG"):
    return irc.send(msgtype+" "+to+" :"+sender+": An error has occurred - "+message+" - Try again.\r\n")

def translate(to_translate, to_language="auto", language="auto"):
	agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
	before_trans = 'class="t0">'
	link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, language, to_translate.replace(" ", "+"))
	request = urllib2.Request(link, headers=agents)
	page = urllib2.urlopen(request).read()
	result = page[page.find(before_trans)+len(before_trans):]
	result = result.split("<")
	result = result[0].strip()
	result = result.decode("utf8", "ignore")
	result = result.encode('utf8')
	h = HTMLParser.HTMLParser()
	return h.unescape(result)

if os.path.isfile("config.json"):
    conf = json.load(open('config.json'))
    try:
        server = conf['server']
        server = server.encode('utf8')
        botnick = conf['botnick']
        botnick = botnick.encode('utf8')
        password = conf['password']
        password = password.encode('utf8')
        owner = conf['owner']
        admins = conf['admins']
        prefix = conf['prefix']
        prefix = prefix.encode('utf8')
        channels = conf['channels']
        ignored = conf['ignored']
        port = conf['port']
        invitejoin = conf['settings']['invitejoin']
        use_ssl = conf['settings']['use_ssl']
    except Exception, e:
        print "Error with the config, please check it. - "+str(e)
        sys.exit()

    ##command info
    try:
        cmd_action = conf['settings']['commandconfig']['action']
    except Exception:
        cmd_action = True
        pass
    try:
        cmd_coin = conf['settings']['commandconfig']['coin']
    except Exception:
        cmd_coin = True
        pass
    try:
        cmd_github = conf['settings']['commandconfig']['github']
    except Exception:
        cmd_github = True
        pass
    try:
        cmd_lastfm = conf['settings']['commandconfig']['lastfm']
    except Exception:
        cmd_lastfm = True
        pass
    try:
        cmd_pwn = conf['settings']['commandconfig']['pwn']
    except Exception:
        cmd_pwn = True
        pass
    try:
        cmd_say = conf['settings']['commandconfig']['say']
    except Exception:
        cmd_say = True
        pass
    try:
        cmd_stupid = conf['settings']['commandconfig']['stupid']
    except Exception:
        cmd_stupid = True
        pass
    try:
        cmd_translate = conf['settings']['commandconfig']['translate']
    except Exception:
        cmd_translate = True
        pass
    try:
        cmd_weather = conf['settings']['commandconfig']['weather']
    except Exception:
        cmd_weather = True
        pass
    try:
        cmd_yt = conf['settings']['commandconfig']['youtube']
    except Exception:
        cmd_yt = True
        pass
else:
    print "A config file was not found, are you sure you renamed config.example.json to config.json?"
    sys.exit()

#connect
if use_ssl == True:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc = ssl.wrap_socket(irc)
    print "Connecting to:", server
    irc.connect((server, int(port)))
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :https://github.com/Snowstormer/allie\n")
    irc.send("NICK "+ botnick +"\n")
    if password != "":
        irc.send("PRIVMSG NICKSERV :IDENTIFY "+botnick+" "+password+"\r\n") 
    for channel in channels:
        irc.send("JOIN "+ channel +"\n")
else:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to:", server
    irc.connect((server, int(port)))
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :https://github.com/Snowstormer/allie\n")
    irc.send("NICK "+ botnick +"\n")
    if password != "":
        irc.send("PRIVMSG NICKSERV :IDENTIFY "+botnick+" "+password+"\r\n") 
    for channel in channels:
        irc.send("JOIN "+ channel +"\n")

#body
readbuffer = ''
while 1:
    text=irc.recv(2040)
    print text
    sender = text.split(" ")[0].split("!")[0].strip(":")
    try:
        sendchannel = text.split(" ")[2]
    except Exception:
        pass
    try:
        hostmask = text.split(" ")[0].split("@")[1]
    except Exception:
        pass
    sendto = ''

    if text.find('PRIVMSG ' +botnick+ ' :') != -1:
        sendto = sender
    else:
        sendto = sendchannel

    if text.find('PING') != -1:
        irc.send('PONG \r\n')    
    elif text.find("VERSION") != -1:
        irc.send("NOTICE "+sender+" :\x01VERSION "+botnick+", based on allie - The Python IRC Bot @ https://github.com/Snowstormer/allie / Running on "+platform.system()+" "+platform.release()+"\x01\r\n")
    elif text.find('INVITE') != -1:
        if invitejoin.lower() == "true":
            invited = text.split(botnick+" :")
            invited = invited[1]
            irc.send("JOIN "+str(invited)+"\n")
        elif invitejoin.lower() == "admin":
            if sender in admins or hostmask in admins or sender in owner or hostmask in owner:
                invited = text.split(botnick+" :")
                invited = invited[1]
                irc.send("JOIN "+str(invited)+"\n")
        elif invitejoin.lower() == "owner":
            if sender in owner or hostmask in owner:
                invited = text.split(botnick+" :")
                invited = invited[1]
                irc.send("JOIN "+str(invited)+"\n")               

    if text.find(':'+prefix+'help') != -1:
        if sender not in ignored and hostmask not in ignored:
            t = text.split(':'+prefix+'help')
            cmd = t[1].strip().lower()
            if cmd == "help":
                notice(sender, ''+prefix+'help: Help for help...really?')
            elif cmd == "stupid":
                if cmd_stupid == True:
                    notice(sender, ''+prefix+'stupid: Produces a 5 word "stupid" sentence on random from a list of defined entries.')
                else:
                    notice(sender, ''+prefix+'stupid is currently disabled.')
            elif cmd == "yt":
                if cmd_yt == True:
                    notice(sender, ''+prefix+'yt: Produces information on a YouTube video.')
                    notice(sender, ''+prefix+'yt: Syntax: '+prefix+'yt <ID>')
                    notice(sender, ''+prefix+'yt: Example: '+prefix+'yt FaMTedT6P0I')
                    notice(sender, ''+prefix+'yt: Alternatively you can post a simple YouTube link.')
                else:
                    notice(sender, ''+prefix+'yt is currently disabled.')
            elif cmd == "say":
                if cmd_say == True:
                    notice(sender, ''+prefix+'say: Says a specified line.')
                    notice(sender, ''+prefix+'say: Syntax: '+prefix+'say <line>')
                    notice(sender, ''+prefix+'say: Example: '+prefix+'say Hello.')
                else:
                    notice(sender, ''+prefix+'say is currently disabled.')
            elif cmd == "action":
                if cmd_action == True:
                    notice(sender, ''+prefix+'action: Does an action.')
                    notice(sender, ''+prefix+'action: Syntax: '+prefix+'action <line>')
                    notice(sender, ''+prefix+'action: Example: '+prefix+'action eats everyone.')
                else:
                    notice(sender, ''+prefix+'action is currently disabled.')
            elif cmd == "pwn":
                if cmd_pwn == True:
                    notice(sender, ''+prefix+'pwn: Pwns someone.')
                    notice(sender, ''+prefix+'pwn: Syntax: '+prefix+'pwn <string>')
                    notice(sender, ''+prefix+'pwn: Example: '+prefix+'pwn Everyone')
                else:
                    notice(sender, ''+prefix+'pwn is currently disabled.')
            elif cmd == "weather":
                if cmd_pwn == True:
                    notice(sender, ''+prefix+'weather: Shows the weather of a location.')
                    notice(sender, ''+prefix+'weather: Syntax: '+prefix+'weather <location>')
                    notice(sender, ''+prefix+'weather: Example: '+prefix+'weather New York')
                else:
                    notice(sender, ''+prefix+'weather is currently disabled.')
            elif cmd == "coin":
                if cmd_coin == True:
                    notice(sender, ''+prefix+'coin: Flips a coin.')
                else:
                    notice(sender, ''+prefix+'coin is currently disabled.')
            elif cmd == "github":
                if cmd_github == True:
                    notice(sender, ''+prefix+'github: Shows information of a GitHub user.')
                    notice(sender, ''+prefix+'github: Syntax: '+prefix+'github <username>')
                    notice(sender, ''+prefix+'github: Example: '+prefix+'github MyGitHub')
                else:
                    notice(sender, ''+prefix+'github is currently disabled.')
            elif cmd == "lastfm":
                if cmd_lastfm == True:
                    notice(sender, ''+prefix+'lastfm: Shows the recent track of a Last.fm user.')
                    notice(sender, ''+prefix+'lastfm: Syntax: '+prefix+'lastfm <username>')
                    notice(sender, ''+prefix+'lastfm: Example: '+prefix+'lastfm MyLastFm')
                else:
                    notice(sender, ''+prefix+'lastfm is currently disabled.')
            elif cmd == "translate":
                if cmd_translate == True:
                    notice(sender, ''+prefix+'translate: Translates a message from one language to another.')
                    notice(sender, ''+prefix+'translate: Syntax: '+prefix+'translate <language from> <language to> <message>')
                    notice(sender, ''+prefix+'translate: Example: '+prefix+'translate en es How are you?')
                else:
                    notice(sender, ''+prefix+'translate is currently disabled.')
            elif cmd == "quit":
                notice(sender, ''+prefix+'quit: Makes the bot quit.')
            elif cmd == "nick":
                notice(sender, ''+prefix+'nick: Changes the bot\'s nick.')
                notice(sender, ''+prefix+'nick: Syntax: '+prefix+'nick <name>')
                notice(sender, ''+prefix+'nick: Example: '+prefix+'nick allie')
            elif cmd == "join":
                notice(sender, ''+prefix+'join: Joins a channel.')
                notice(sender, ''+prefix+'join: Syntax: '+prefix+'join <channel>')
                notice(sender, ''+prefix+'join: Example: '+prefix+'join ##allie')
            elif cmd == "part":
                notice(sender, ''+prefix+'part: Parts a channel.')
                notice(sender, ''+prefix+'part: Syntax: '+prefix+'part <channel>')
                notice(sender, ''+prefix+'part: Example: '+prefix+'part ##allie')
            elif cmd == "raw":
                notice(sender, ''+prefix+'raw: Sends a raw message.')
                notice(sender, ''+prefix+'raw: Syntax: '+prefix+'raw <string>')
                notice(sender, ''+prefix+'raw: Example: '+prefix+'raw PRIVMSG ##allie :I am cool!')
            elif cmd == "eval":
                notice(sender, ''+prefix+'eval: Executes a raw Python string.')
                notice(sender, ''+prefix+'eval: Syntax: '+prefix+'eval <Python string>')
                notice(sender, ''+prefix+'eval: Example: '+prefix+'eval print "hi"')
            elif cmd == "promote":
                notice(sender, ''+prefix+'promote: Promotes a person to a specified right list. Available rights: admin, ignored.')
                notice(sender, ''+prefix+'promote: Syntax: '+prefix+'promote <right> <name>')
                notice(sender, ''+prefix+'promote: Example: '+prefix+'promote admin allie')
            elif cmd == "demote":
                notice(sender, ''+prefix+'demote: Demotes a person from a specified right list. Available rights: admin, ignored.')
                notice(sender, ''+prefix+'demote: Syntax: '+prefix+'demote <right> <name>')
                notice(sender, ''+prefix+'demote: Example: '+prefix+'demote admin allie-hator')
            elif cmd == "rights":
                notice(sender, ''+prefix+'rights: Displays the specified right list. Available rights: owner, admin, ignored.')
                notice(sender, ''+prefix+'rights: Syntax: '+prefix+'rights <right>')
                notice(sender, ''+prefix+'rights: Example: '+prefix+'rights owner')
            elif cmd == "topic":
                notice(sender, ''+prefix+'topic: Modifies the topic.')
                notice(sender, ''+prefix+'topic: Syntax: '+prefix+'topic <command>')
                notice(sender, ''+prefix+'topic: Commands: '+prefix+'topic append <string> - appends to the topic')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic prepend <string> - prepends to the topic')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic change <string> - changes the topic')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic del - deletes the topic')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic reset - resets the topic / useless right now')
                notice(sender, ''+prefix+'topic: Examples: '+prefix+'topic append Hi.')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic prepend Hi.')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic change Hi.')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic del')
                notice(sender, ''+prefix+'topic:           '+prefix+'topic reset')
            elif cmd == "enable":
                notice(sender, ''+prefix+'enable: Enables a command.')
                notice(sender, ''+prefix+'enable: Syntax: '+prefix+'enable <command>')
                notice(sender, ''+prefix+'enable: Example: '+prefix+'enable stupid')
            elif cmd == "disable":
                notice(sender, ''+prefix+'disable: Disables a command.')
                notice(sender, ''+prefix+'disable: Syntax: '+prefix+'disable <command>')
                notice(sender, ''+prefix+'disable: Example: '+prefix+'disable stupid')
            else:
                notice(sender, 'Commands available to you:')
                cmds = []
                cmds.append(prefix+'help')
                if cmd_say == True:
                    cmds.append(prefix+'say')
                if cmd_action == True:
                    cmds.append(prefix+'action')
                if cmd_stupid == True:
                    cmds.append(prefix+'stupid')
                if cmd_yt == True:
                    cmds.append(prefix+'yt')
                if cmd_pwn == True:
                    cmds.append(prefix+'pwn')
                if cmd_weather == True:
                    cmds.append(prefix+'weather')
                if cmd_coin == True:
                    cmds.append(prefix+'coin')
                if cmd_lastfm == True:
                    cmds.append(prefix+'lastfm')
                if cmd_github == True:
                    cmds.append(prefix+'github')
                if cmd_translate == True:
                    cmds.append(prefix+'translate')
                cmds.append(prefix+'rights')
                if hostmask in owner or sender in owner:
                    cmds.append(prefix+'join')
                    cmds.append(prefix+'part')
                    cmds.append(prefix+'quit')
                    cmds.append(prefix+'nick')
                    cmds.append(prefix+'raw')
                    cmds.append(prefix+'eval')
                if hostmask in owner or sender in owner or sender in admins or hostmask in admins:
                    cmds.append(prefix+'promote')
                    cmds.append(prefix+'demote')
                    cmds.append(prefix+'topic')
                    cmds.append(prefix+'enable')
                    cmds.append(prefix+'disable')
                notice(sender, ', '.join(cmds))
                notice(sender, 'For help on a specific command say '+prefix+'help [command]')
                if not text.find('PRIVMSG ' +botnick+ ' :') != -1:
                    reply(sendto, 'The help message should show as a notice, if not, check your query.')

##Base commands
    if text.find(':'+prefix+'say ') != -1:
        if cmd_say == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    t = text.split(':'+prefix+'say ')
                    msg = t[1].strip()
                    privmsg(sendto, str(msg))
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find(':'+prefix+'action ') != -1:
        if cmd_action == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    t = text.split(':'+prefix+'action ')
                    action = t[1].strip()
                    privmsg(sendto, '\x01ACTION '+str(action)+'\x01')
                except Exception, e:
                    error(sendto, str(e))
                    pass
	
    if text.find(':'+prefix+'stupid') != -1:
        if cmd_stupid == True:
            if sender not in ignored and hostmask not in ignored:
                w1 = ["Justin Timberlake", "Angela Merkel", "Vladimir Putin", "Ke$ha", "Justin Bieber", "Rebecca Black", "Violetta", "I", "You", "He", "She", "They", "We", "The girls", "The boys", "Students", "Teachers", "The teacher"]
                w2 = ["farted", "danced", "flew", "turned into an octopus", "sang 'My Slowianie'", "became a narwhal", "bounced on a trampoline", "took a shower", "pooped", "was sick", "read"]
                w3 = ["while", "after", "before"]
                w4 = ["the school", "Russia", "the hospital", "a toilet", "a house", "everyone", "I", "he", "she", "we", "they", "you", "a person", "elephants"]
                w5 = ["blew up", "turned into a cucumber", "made noise", "danced like crazy", "died", "moaned"]
                privmsg(sendto, random.choice(w1)+' '+random.choice(w2)+' '+random.choice(w3)+' '+random.choice(w4)+' '+random.choice(w5)+'.')
            
    if text.find(':'+prefix+'yt ') != -1:
        if cmd_yt == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    idb = text.split(':'+prefix+'yt ')
                    videoid = idb[1].strip()
                    if len(videoid) == 11:
                        try:
                            url = 'http://gdata.youtube.com/feeds/api/videos/'+videoid+'?alt=json&v=2'
                            jsonvid = json.load(urllib2.urlopen(url))
                            title = jsonvid['entry']['title']['$t']
                            author = jsonvid['entry']['author'][0]['name']['$t']
                            viewcount = jsonvid['entry']['yt$statistics']['viewCount']
                            likes = jsonvid['entry']['yt$rating']['numLikes']
                            dislikes = jsonvid['entry']['yt$rating']['numDislikes']
                            title = title.encode("utf8")
                            author = author.encode("utf8")
                            privmsg(sendto, '\"'+str(title)+'\" by '+str(author)+' | '+str(viewcount)+' views | 03'+str(likes)+' likes | 04'+str(dislikes)+' dislikes | 02http://youtu.be/'+str(videoid)+'')
                        except Exception, e:
                            error(sendto, str(e))
                            pass
                    else:
                        error(sendto, 'Could not look up video.')
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find("v=") != -1:
        if cmd_yt == True:
            if sender not in ignored and hostmask not in ignored:
                print text.find("v=")
                if text.find("youtube.com") != -1:
                    id1 = text.find("v=") + 2
                    videoid = text[id1:id1+11]
                    if len(videoid) == 11:
                        try:
                            url = 'http://gdata.youtube.com/feeds/api/videos/'+videoid+'?alt=json&v=2'
                            jsonvid = json.load(urllib2.urlopen(url))
                            title = jsonvid['entry']['title']['$t']
                            author = jsonvid['entry']['author'][0]['name']['$t']
                            viewcount = jsonvid['entry']['yt$statistics']['viewCount']
                            try:
                                likes = jsonvid['entry']['yt$rating']['numLikes']
                            except Exception:
                                likes = 0
                            try:
                                dislikes = jsonvid['entry']['yt$rating']['numDislikes']
                            except Exception:
                                dislikes = 0
                            title = title.encode("utf8")
                            author = author.encode("utf8")
                            privmsg(sendto, '\"'+str(title)+'\" by '+str(author)+' | '+str(viewcount)+' views | 03'+str(likes)+' likes | 04'+str(dislikes)+' dislikes | 02http://youtu.be/'+str(videoid)+'')
                        except Exception, e:
                            error(sendto, str(e))
                            pass
                    else:
                        error(sendto, 'Could not look up video.')

    if text.find(':'+prefix+'pwn ') != -1:
        if cmd_pwn == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    t = text.split(':'+prefix+'pwn ')
                    pwn = t[1].strip()
                    if pwn == botnick:
                        error(sendto, 'Cannot pwn self.')
                    else:
                        if hostmask in admins or sender in admins or hostmask in owner or sender in owner:
                            privmsg(sendto, '\x01ACTION pwns '+str(pwn)+'\x01')
                            irc.send('MODE '+sendto+' +b '+str(pwn)+'\n')
                            irc.send('KICK '+sendto+' '+str(pwn)+'\n')
                            time.sleep(3)
                            irc.send('MODE '+sendto+' -b '+str(pwn)+'\n')
                        else:
                            privmsg(sendto, '\x01ACTION pwns '+str(pwn)+'\x01')
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find(':'+prefix+'rights ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if text.find(':'+prefix+'rights ignored') != -1:
                    if not ignored:
                        privmsg(sendto, 'Global ignorelist is empty.')
                    elif ignored == "":
                        privmsg(sendto, 'Global ignorelist is empty.')
                    else:
                        privmsg(sendto, 'Global ignorelist: '", ".join(ignored)+'.')
                elif text.find(':'+prefix+'rights admin') != -1:
                    if not admins:
                        privmsg(sendto, 'Global adminlist is empty.')
                    elif admins == "":
                        privmsg(sendto, 'Global adminlist is empty.')
                    else:
                        privmsg(sendto, 'Global adminlist: '+", ".join(admins)+'.')
                elif text.find(':'+prefix+'rights owner') != -1:
                    if not owner:
                        privmsg(sendto, 'Global ownerlist is empty.')
                    elif owner == "":
                        privmsg(sendto, 'Global ownerlist is empty.')
                    else:
                        privmsg(sendto, 'Global ownerlist: '+", ".join(owner)+'.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'weather ') != -1:
        if cmd_weather == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    t = text.split(':'+prefix+'weather ')
                    w = t[1].strip()
                    if text.find(':'+prefix+'weather '+str(w)+''):
                        url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(w)+'&units=metric'
                        wjson = json.load(urllib2.urlopen(url))
                        name = wjson['name']
                        country = wjson['sys']['country']
                        cond = wjson['weather'][0]['main']
                        temp = wjson['main']['temp']
                        wind = wjson['wind']['speed']
                        clouds = wjson['clouds']['all']
                        if len(name) == 0:
                            if len(country) == 0:
                                privmsg(sendto, 'The current weather in your desired location is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                            else:
                                privmsg(sendto, 'The current weather in '+str(country)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                        elif len(country) == 0:
                            if len(name) == 0:
                                privmsg(sendto, 'The current weather in your desired location is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                            else:
                                privmsg(sendto, 'The current weather in '+str(name)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                        else:
                            privmsg(sendto, 'The current weather in '+str(name)+', '+str(country)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                    else:
                        error(sendto, 'Insufficent parameters.')
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find(':'+prefix+'coin') != -1:
        if cmd_coin == True:
            if sender not in ignored and hostmask not in ignored:
                lands = ["heads", "tails"]
                privmsg(sendto, sender+' flips a coin...')
                time.sleep(1)
                privmsg(sendto, 'It lands on '+random.choice(lands)+'.')

    if text.find(':'+prefix+'lastfm ') != -1:
        if cmd_lastfm.lower() == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    lstfm = text.split(':'+prefix+'lastfm ')
                    lstfmusr = lstfm[1].strip()
                    recenturl = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+str(lstfmusr)+"&api_key=af947edcf6a945248c5111c69de91264&format=json"
                    rjson = json.load(urllib2.urlopen(recenturl))
                    recentsong = rjson['recenttracks']['track'][0]['name']
                    recentartist = rjson['recenttracks']['track'][0]['artist']['#text']
                    recentalbum = rjson['recenttracks']['track'][0]['album']['#text']
                    recentsong = recentsong.encode("utf8")
                    recentartist = recentartist.encode("utf8")
                    recentalbum = recentalbum.encode("utf8")
                    if len(recentalbum) == 0:
                        privmsg(sendto, ''+str(lstfmusr)+'\'s last played track is \"'+str(recentsong)+'\" by '+str(recentartist)+'.')
                    else:
                        privmsg(sendto, ''+str(lstfmusr)+'\'s last played track is \"'+str(recentsong)+'\" by '+str(recentartist)+', from the album \"'+str(recentalbum)+'\".')
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find(':'+prefix+'github ') != -1:
        if cmd_github == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    github = text.split(':'+prefix+'github ')
                    githubusr = github[1].strip()
                    githuburl = "https://osrc.dfm.io/"+str(githubusr)+".json"
                    gitjson = json.load(urllib2.urlopen(githuburl))
                    gitname = gitjson['name']
                    gitlanguage = gitjson['usage']['languages'][0]['language']
                    gitlanguagecount = gitjson['usage']['languages'][0]['count']
                    gitevent = gitjson['usage']['events'][0]['type']
                    gitname = gitname.encode('utf8')
                    if gitevent == "GollumEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like doing wiki edits.")
                    elif gitevent == "PushEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like doing pushes.")
                    elif gitevent == "CreateEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like creating new repos or branches.")
                    elif gitevent == "WatchEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like watching.")
                    elif gitevent == "IssueCommentEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like making issue comments.")
                    elif gitevent == "PullRequestEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like doing pull requests.")
                    elif gitevent == "IssuesEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like reporting issues.")
                    elif gitevent == "ForkEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like forking.")
                    elif gitevent == "DeleteEvent":
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions). They seem to like deleting branches.")
                    else:
                        privmsg(sendto, ""+str(gitname)+"'s favourite coding language seems to be 04"+str(gitlanguage)+" ("+str(gitlanguagecount)+" contributions).")
                except Exception, e:
                    error(sendto, str(e))
                    pass

    if text.find(':'+prefix+'translate ') != -1:
        if cmd_translate == True:
            if sender not in ignored and hostmask not in ignored:
                try:
                    t = text.split(" ", 6)
                    langfrom = t[4].strip()
                    langto = t[5].strip()
                    msg = t[6].strip()
                    reply(sendto, translate(str(msg), str(langto), str(langfrom)))
                except Exception, e:
                    error(sendto, str(e))
                    pass
                    
##Admin commands
    if text.find(':'+prefix+'quit') != -1:
        if sender not in ignored and hostmask not in ignored:
            if hostmask in owner or sender in owner:
                quitmsg = ["Critical error.", "Sorry, we're closed.", "Shutting down...", "I don't blame you.", "I don't hate you.", "Goodbye!", "Disconnecting..."]
                irc.send('QUIT :'+random.choice(quitmsg)+'\n')
                sys.exit()
            else:
                notice(sender, 'You are not authorised to perform this command.')
            
    if text.find(':'+prefix+'nick ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in owner or sender in owner:
                    t = text.split(':'+prefix+'nick ')
                    nick = t[1].strip()
                    if re.match("^[A-Za-z0-9_\-\\\[\]\{\}\^\`\|]*$", nick):
                        irc.send('NICK '+str(nick)+'\n')
                        botnick = str(nick)
                        done()
                    else:
                        error(sendto, 'Invalid nickname.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass
            
    if text.find(':'+prefix+'join ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in owner or sender in owner:
                    t = text.split(':'+prefix+'join ')
                    chan = t[1].strip()
                    if chan.startswith("#"):
                        irc.send('JOIN '+str(chan)+'\n')
                        done()
                    else:
                        error(sendto, 'Bad parameters, channel names start with #.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass
            
    if text.find(':'+prefix+'part ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in owner or sender in owner:
                    t = text.split(':'+prefix+'part ')
                    chan = t[1].strip()
                    if chan.startswith("#"):
                        irc.send('PART '+str(chan)+'\n')
                        done()
                    else:
                        error(sendto, 'Bad parameters, channel names start with #.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'eval ') != -1:
        if sender not in ignored and hostmask not in ignored:
            if hostmask in owner or sender in owner:
                try:
                    t = text.split(':'+prefix+'eval ')
                    evalcmd = t[1].strip()
                    exec(str(evalcmd))
                except Exception, e:
                    error(sendto, str(e))
                    pass
            else:
                notice(sender, 'You are not authorised to perform this command.')

    if text.find(':'+prefix+'raw ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in owner or sender in owner:
                    t = text.split(':'+prefix+'raw ')
                    rawcode = t[1].strip()
                    if rawcode == "":
                        error(sendto, 'Raw command cannot be empty.')
                    else:
                        irc.send(str(rawcode)+'\r\n')
                        done()
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'promote ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if text.find(':'+prefix+'promote ignored') != -1:
                    if hostmask in owner or sender in owner or hostmask in admins or sender in admins:
                        t = text.split(':'+prefix+'promote ignored ')
                        usr = t[1].strip()
                        if re.match("^[A-Za-z0-9_\-\\\[\]\{\}\^\`\|/]*$", usr):
                            if usr == botnick:
                                error(sendto, 'Cannot ignore self.')
                            elif usr in owner:
                                error(sendto, 'Cannot ignore owner.')
                            else:
                                if str(usr) in ignored:
                                    privmsg(sendto, str(usr)+' already on global ignorelist.')
                                else:
                                    ignored.append(str(usr))
                                    privmsg(sendto, str(usr)+' added to global ignorelist.')
                        else:
                            error(sendto, 'Invalid nickname.')
                    else:
                        notice(sender, 'You are not authorised to perform this command.')
                elif text.find(':'+prefix+'promote admin') != -1:
                    if hostmask in owner or sender in owner:
                        t = text.split(':'+prefix+'promote admin ')
                        usr = t[1].strip()
                        if re.match("^[A-Za-z0-9_\-\\\[\]\{\}\^\`\|/]*$", usr):
                            if usr == botnick:
                                error(sendto, 'Cannot add self to adminlist.')
                            else:
                                if str(usr) in admins:
                                    privmsg(sendto, str(usr)+' already on global adminlist.')
                                else:
                                    admins.append(str(usr))
                                    privmsg(sendto, str(usr)+' added to global adminlist.')
                        else:
                            error(sendto, 'Invalid nickname.')
                    else:
                        notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'demote ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if text.find(':'+prefix+'demote ignored') != -1:
                    if hostmask in owner or sender in owner or hostmask in admins or sender in admins:
                        t = text.split(':'+prefix+'demote ignored ')
                        usr = t[1].strip()
                        if re.match("^[A-Za-z0-9_\-\\\[\]\{\}\^\`\|/]*$", usr):
                            if usr == botnick:
                                error(sendto, 'Cannot unignore self.')
                            else:
                                if str(usr) in ignored:
                                    ignored.remove(str(usr))
                                    privmsg(sendto, str(usr)+' removed from global ignorelist.')
                                else:
                                    privmsg(sendto, str(usr)+' not on global ignorelist.')
                        else:
                            error(sendto, 'Invalid nickname.')
                    else:
                        notice(sender, 'You are not authorised to perform this command.')
                elif text.find(':'+prefix+'demote admin') != -1:
                    if hostmask in owner or sender in owner or hostmask in admins or sender in admins:
                        t = text.split(':'+prefix+'demote admin ')
                        usr = t[1].strip()
                        if re.match("^[A-Za-z0-9_\-\\\[\]\{\}\^\`\|/]*$", usr):
                            if usr == botnick:
                                error(sendto, 'Cannot remove self from adminlist.')
                            else:
                                if str(usr) in admins:
                                    admins.remove(str(usr))
                                    privmsg(sendto, str(usr)+' removed from global adminlist.')
                                else:
                                    privmsg(sendto, str(usr)+' not on global adminlist.')
                        else:
                            error(sendto, 'Invalid nickname.')
                    else:
                        notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'topic ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in admins or sender in admins or hostmask in owner or sender in owner:
                    if text.find(':'+prefix+'topic append') != -1:
                        t1 = text.split(':'+prefix+'topic append ')
                        addtopic = t1[1].strip()
                        privmsg("ChanServ", 'TOPICAPPEND '+sendto+' '+str(addtopic))
                    elif text.find(':'+prefix+'topic prepend') != -1:
                        t4 = text.split(':'+prefix+'topic prepend ')
                        pretopic = t4[1].strip()
                        privmsg("ChanServ", 'TOPICPREPEND '+sendto+' '+str(pretopic))
                    elif text.find(':'+prefix+'topic change') != -1:
                        t2 = text.split(':'+prefix+'topic change ')
                        changetopic = t2[1].strip()
                        irc.send('TOPIC '+sendto+' :'+str(changetopic)+'\r\n')
                    elif text.find(':'+prefix+'topic del') != -1:
                        irc.send('TOPIC '+sendto+' :''\r\n')
                    elif text.find(':'+prefix+'topic reset') != -1:
                        topic = ""
                        irc.send('TOPIC '+sendto+' :'+topic+'\r\n')
                    else:
                        error(sendto, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'enable ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in admins or sender in admins or hostmask in owner or sender in owner:
                    if text.find(':'+prefix+'enable say') != -1:
                        if cmd_say == True:
                            privmsg(sendto, prefix+'say is already enabled.')
                        else:
                            cmd_say = True
                            privmsg(sendto, prefix+'say is now enabled.')
                    elif text.find(':'+prefix+'enable stupid') != -1:
                        if cmd_stupid == True:
                            privmsg(sendto, prefix+'stupid is already enabled.')
                        else:
                            cmd_stupid = True
                            privmsg(sendto, prefix+'stupid is now enabled.')
                    elif text.find(':'+prefix+'enable yt') != -1:
                        if cmd_yt == True:
                            privmsg(sendto, prefix+'yt/YouTube is already enabled.')
                        else:
                            cmd_yt = True
                            privmsg(sendto, prefix+'yt/YouTube is now enabled.')
                    elif text.find(':'+prefix+'enable pwn') != -1:
                        if cmd_pwn == True:
                            privmsg(sendto, prefix+'pwn is already enabled.')
                        else:
                            cmd_pwn = True
                            privmsg(sendto, prefix+'pwn is now enabled.')
                    elif text.find(':'+prefix+'enable weather') != -1:
                        if cmd_weather == True:
                            privmsg(sendto, prefix+'weather is already enabled.')
                        else:
                            cmd_weather = True
                            privmsg(sendto, prefix+'weather is now enabled.')
                    elif text.find(':'+prefix+'enable coin') != -1:
                        if cmd_coin == True:
                            privmsg(sendto, prefix+'coin is already enabled.')
                        else:
                            cmd_coin = True
                            privmsg(sendto, prefix+'coin is now enabled.')
                    elif text.find(':'+prefix+'enable action') != -1:
                        if cmd_action == True:
                            privmsg(sendto, prefix+'action is already enabled.')
                        else:
                            cmd_action = True
                            privmsg(sendto, prefix+'action is now enabled.')
                    elif text.find(':'+prefix+'enable lastfm') != -1:
                        if cmd_lastfm == True:
                            privmsg(sendto, prefix+'lastfm is already enabled.')
                        else:
                            cmd_lastfm = True
                            privmsg(sendto, prefix+'lastfm is now enabled.')
                    elif text.find(':'+prefix+'enable github') != -1:
                        if cmd_github == True:
                            privmsg(sendto, prefix+'github is already enabled.')
                        else:
                            cmd_github = True
                            privmsg(sendto, prefix+'github is now enabled.')
                    elif text.find(':'+prefix+'enable translate') != -1:
                        if cmd_translate == True:
                            privmsg(sendto, prefix+'translate is already enabled.')
                        else:
                            cmd_translate = True
                            privmsg(sendto, prefix+'translate is now enabled.')
                    else:
                        notice(sender, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass

    if text.find(':'+prefix+'disable ') != -1:
        if sender not in ignored and hostmask not in ignored:
            try:
                if hostmask in admins or sender in admins or hostmask in owner or sender in owner:
                    if text.find(':'+prefix+'disable say') != -1:
                        if cmd_say == False:
                            privmsg(sendto, prefix+'say is already disabled.')
                        else:
                            cmd_say = False
                            privmsg(sendto, prefix+'say is now disabled.')
                    elif text.find(':'+prefix+'disable stupid') != -1:
                        if cmd_stupid == False:
                            privmsg(sendto, prefix+'stupid is already disabled.')
                        else:
                            cmd_stupid = False
                            privmsg(sendto, prefix+'stupid is now disabled.')
                    elif text.find(':'+prefix+'disable yt') != -1:
                        if cmd_yt == False:
                            privmsg(sendto, prefix+'yt/YouTube is already disabled.')
                        else:
                            cmd_yt = False
                            privmsg(sendto, prefix+'yt/YouTube is now disabled.')
                    elif text.find(':'+prefix+'disable pwn') != -1:
                        if cmd_pwn == False:
                            privmsg(sendto, prefix+'pwn is already disabled.')
                        else:
                            cmd_pwn = False
                            privmsg(sendto, prefix+'pwn is now disabled.')
                    elif text.find(':'+prefix+'disable weather') != -1:
                        if cmd_weather == False:
                            privmsg(sendto, prefix+'weather is already disabled.')
                        else:
                            cmd_weather = False
                            privmsg(sendto, prefix+'weather is now disabled.')
                    elif text.find(':'+prefix+'disable coin') != -1:
                        if cmd_coin == False:
                            privmsg(sendto, prefix+'coin is already disabled.')
                        else:
                            cmd_coin = False
                            privmsg(sendto, prefix+'coin is now disabled.')
                    elif text.find(':'+prefix+'disable action') != -1:
                        if cmd_action == False:
                            privmsg(sendto, prefix+'action is already disabled.')
                        else:
                            cmd_action = False
                            privmsg(sendto, prefix+'action is now disabled.')
                    elif text.find(':'+prefix+'disable lastfm') != -1:
                        if cmd_lastfm == False:
                            privmsg(sendto, prefix+'lastfm is already disabled.')
                        else:
                            cmd_lastfm = False
                            privmsg(sendto, prefix+'lastfm is now disabled.')
                    elif text.find(':'+prefix+'disable github') != -1:
                        if cmd_github == False:
                            privmsg(sendto, prefix+'github is already disabled.')
                        else:
                            cmd_github = False
                            privmsg(sendto, prefix+'github is now disabled.')
                    elif text.find(':'+prefix+'disable translate') != -1:
                        if cmd_translate == False:
                            privmsg(sendto, prefix+'translate is already disabled.')
                        else:
                            cmd_translate = False
                            privmsg(sendto, prefix+'translate is now disabled.')                            
                    else:
                        notice(sender, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception, e:
                error(sendto, str(e))
                pass
