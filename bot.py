#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import random
import re
import urllib
import urllib2
import json
import time

##Change these!
server = ""                                                     ##IRC Server - example: "irc.freenode.net" for Freenode
botnick = "PyAllie"                                             ##Bot's nick - example: "PyAllie"
password = "replaceme"                                          ##Bot's NickServ password - example: "replaceme"
owner = "Your name"                                             ##Bot's owner's name - example: "myname"
admins = ["Your name"]                                          ##List of bot administrators (Must put owner here as well) - example: ["myname", "yourname"]
ignored = []                                                    ##List of ignored people - Add people here if you wish.
prefix = "!"                                                    ##Bot's command prefix - example: "!"
channels = ["#python"]                                          ##Channels to join - example: ["#python", "#freenode"]

"""Command config.
Change "True" to "False" to disable a command. Can also be disabled/enabled later while bot is online.
"""

global cmd_say
cmd_say = True
global cmd_stupid
cmd_stupid = True
global cmd_yt
cmd_yt = True
global cmd_pwn
cmd_pwn = True
global cmd_weather
cmd_weather = True
global cmd_coin
cmd_coin = True
global cmd_action
cmd_action = True
global cmd_lastfm
cmd_lastfm = True

##--------------------------------------------------------##
##Only edit below this line if you know what you're doing.##
##--------------------------------------------------------##

#connect
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Connecting to:", server
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :https://github.com/Snowstormer/allie\n")
irc.send("NICK "+ botnick +"\n")
irc.send("PRIVMSG NICKSERV :IDENTIFY "+botnick+" "+password+"\r\n") 
for channel in channels:
    irc.send("JOIN "+ channel +"\n")

#functions

def privmsg(to, message):
    return irc.send("PRIVMSG "+to+" :"+message+"\r\n")

def reply(to, message):
    return irc.send("PRIVMSG "+to+" :"+sender+": "+message+"\r\n")

def notice(to, message):
    return irc.send("NOTICE "+to+" :"+message+"\r\n")

def done():
    return irc.send("PRIVMSG "+sendto+" :"+sender+": Done.\r\n")

#body
readbuffer = ''
while 1:                                                                            #puts it in a loop
    text=irc.recv(2040)                                                             #receive the text
    print text                                                                      #print text to console
    sender = text.split(" ")
    sender = sender[0]
    sender = sender.split("!")
    sender = sender[0]
    sender = sender.strip(":")
    sendchan = text.split(" ")
    try:
        sendchannel = sendchan[2]
    except Exception:
        pass
    ##Find where command is sent
    sendto = '' # can be a user's nick(from query) or a channel

    if text.find('PRIVMSG ' +botnick+ ' :') != -1: #the command comes from a query
        sendto = sender
    else:
        sendto = sendchannel

    if text.find('PING') != -1:                                                     #check if 'PING' is found
        try:
            irc.send('PONG \r\n')                                                   #returns 'PONG' back to the server (prevents pinging out!)
        except Exception:
            pass

##Help
    if text.find(':'+prefix+'help') != -1:
        if sender in ignored:
            pass
        else:
                t = text.split(':'+prefix+'help')
                cmd = t[1].strip()
                if cmd == "help":
                    privmsg(sender, prefix+'help: Help for help...really?')
                elif cmd == "stupid":
                    if cmd_stupid == True:
                        privmsg(sender, prefix+'stupid: Produces a 5 word "stupid" sentence on random from a list of defined entries.')
                    else:
                        pass
                elif cmd == "yt":
                    if cmd_yt == True:
                        privmsg(sender, prefix+'yt: Produces information on a YouTube video.')
                        privmsg(sender, prefix+'yt: Syntax: '+prefix+'yt <ID>')
                        privmsg(sender, prefix+'yt: Example: '+prefix+'yt FaMTedT6P0I')
                        privmsg(sender, prefix+'yt: Alternatively you can post a simple YouTube link.')
                    else:
                        pass
                elif cmd == "say":
                    if cmd_say == True:
                        privmsg(sender, prefix+'say: Says a specified line.')
                        privmsg(sender, prefix+'say: Syntax: '+prefix+'say <line>')
                        privmsg(sender, prefix+'say: Example: '+prefix+'say Hello.')
                    else:
                        pass
                elif cmd == "action":
                    if cmd_action == True:
                        privmsg(sender, prefix+'action: Does an action.')
                        privmsg(sender, prefix+'action: Syntax: '+prefix+'action <line>')
                        privmsg(sender, prefix+'action: Example: '+prefix+'action eats everyone.')
                    else:
                        pass
                elif cmd == "pwn":
                    if cmd_pwn == True:
                        privmsg(sender, prefix+'pwn: Pwns someone.')
                        privmsg(sender, prefix+'pwn: Syntax: '+prefix+'pwn <string>')
                        privmsg(sender, prefix+'pwn: Example: '+prefix+'pwn Everyone')
                    else:
                        pass
                elif cmd == "weather":
                    if cmd_pwn == True:
                        privmsg(sender, prefix+'weather: Shows the weather of a location.')
                        privmsg(sender, prefix+'weather: Syntax: '+prefix+'weather <location>')
                        privmsg(sender, prefix+'weather: Example: '+prefix+'weather New York')
                    else:
                        pass
                elif cmd == "coin":
                    if cmd_coin == True:
                        privmsg(sender, prefix+'coin: Flips a coin.')
                    else:
                        pass
                elif cmd == "quit":
                    privmsg(sender, prefix+'quit: Makes the bot quit.')
                elif cmd == "nick":
                    privmsg(sender, prefix+'nick: Changes the bots nick.')
                    privmsg(sender, prefix+'nick: Syntax: '+prefix+'nick <name>')
                    privmsg(sender, prefix+'nick: Example: '+prefix+'nick Pystormer')
                elif cmd == "join":
                    privmsg(sender, prefix+'join: Joins a channel.')
                    privmsg(sender, prefix+'join: Syntax: '+prefix+'join <channel>')
                    privmsg(sender, prefix+'join: Example: '+prefix+'join #channel')
                elif cmd == "part":
                    privmsg(sender, prefix+'part: Parts a channel.')
                    privmsg(sender, prefix+'part: Syntax: '+prefix+'part <channel>')
                    privmsg(sender, prefix+'part: Example: '+prefix+'part #channel')
                elif cmd == "raw":
                    privmsg(sender, prefix+'raw: Sends a raw message.')
                    privmsg(sender, prefix+'raw: Syntax: '+prefix+'raw <string>')
                    privmsg(sender, prefix+'raw: Example: '+prefix+'raw PRIVMSG #channel :I am cool!')
                elif cmd == "eval":
                    privmsg(sender, prefix+'eval: Executes a raw Python string.')
                    privmsg(sender, prefix+'eval: Syntax: '+prefix+'eval <Python string>')
                    privmsg(sender, prefix+'eval: Example: '+prefix+'eval print "hi"')
                elif cmd == "add_admin":
                    privmsg(sender, prefix+'add_admin: Adds a person to the global adminlist.')
                    privmsg(sender, prefix+'add_admin: Syntax: '+prefix+'add_admin <name>')
                    privmsg(sender, prefix+'add_admin: Example: '+prefix+'add_admin Pystormer')
                elif cmd == "remove_admin":
                    privmsg(sender, prefix+'remove_admin: Removes a person from the global adminlist.')
                    privmsg(sender, prefix+'remove_admin: Syntax: '+prefix+'remove_admin <name>')
                    privmsg(sender, prefix+'remove_admin: Example: '+prefix+'remove_admin Pystormer')
                elif cmd == "ignore":
                    privmsg(sender, prefix+'ignore: Adds a person to the global ignorelist.')
                    privmsg(sender, prefix+'ignore: Syntax: '+prefix+'ignore <name>')
                    privmsg(sender, prefix+'ignore: Example: '+prefix+'ignore Pystormer')
                elif cmd == "remove_admin":
                    privmsg(sender, prefix+'unignore: Removes a person from the global ignorelist.')
                    privmsg(sender, prefix+'unignore: Syntax: '+prefix+'unignore <name>')
                    privmsg(sender, prefix+'unignore: Example: '+prefix+'unignore Pystormer')
                elif cmd == "ignorelist":
                    privmsg(sender, prefix+'ignorelist: Displays global ignorelist.')
                elif cmd == "adminlist":
                    privmsg(sender, prefix+'ignorelist: Displays global adminlist.')
                elif cmd == "topic":
                    privmsg(sender, prefix+'topic: Modifies the topic.')
                    privmsg(sender, prefix+'topic: Syntax: '+prefix+'topic <command>')
                    privmsg(sender, prefix+'topic: Commands: '+prefix+'topic append <string> - appends to the topic')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic prepend <string> - prepends to the topic')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic change <string> - changes the topic')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic lock <on or off> - locks/unlocks the topic')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic del - deletes the topic')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic reset - resets the topic')
                    privmsg(sender, prefix+'topic: Examples: '+prefix+'topic append Hi.')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic prepend Hi.')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic change Hi.')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic lock on')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic del')
                    privmsg(sender, prefix+'topic:           '+prefix+'topic reset')
                elif cmd == "enable":
                    privmsg(sender, prefix+'unignore: Enables a command.')
                    privmsg(sender, prefix+'unignore: Syntax: '+prefix+'enable <command>')
                    privmsg(sender, prefix+'unignore: Example: '+prefix+'enable stupid')
                elif cmd == "disable":
                    privmsg(sender, prefix+'unignore: Disables a command.')
                    privmsg(sender, prefix+'unignore: Syntax: '+prefix+'disable <command>')
                    privmsg(sender, prefix+'unignore: Example: '+prefix+'disable stupid')
                elif cmd == "lastfm":
                    privmsg(sender, prefix+'lastfm: Shows the recent track of a Last.fm user.')
                    privmsg(sender, prefix+'lastfm: Syntax: '+prefix+'lastfm <username>')
                    privmsg(sender, prefix+'lastfm: Example: '+prefix+'lastfm MyLastFm')
                else:
                    privmsg(sender, 'Commands available to you:')
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
                    cmds.append(prefix+'adminlist')
                    cmds.append(prefix+'ignorelist')
                    if sender == owner:
                        cmds.append(prefix+'join')
                        cmds.append(prefix+'part')
                        cmds.append(prefix+'quit')
                        cmds.append(prefix+'nick')
                        cmds.append(prefix+'raw')
                        cmds.append(prefix+'eval')
                        cmds.append(prefix+'add_admin')
                    if sender in admins:
                        cmds.append(prefix+'remove_admin')
                        cmds.append(prefix+'ignore')
                        cmds.append(prefix+'unignore')
                        cmds.append(prefix+'topic')
                        cmds.append(prefix+'enable')
                        cmds.append(prefix+'disable')
                    privmsg(sender, ', '.join(cmds))
                    privmsg(sender, 'For help on a specific command say '+prefix+'help [command]')
                    if not text.find('PRIVMSG ' +botnick+ ' :') != -1:
                        reply(sendto, 'The help message should show up in your query.')

##Base commands
    if text.find(':'+prefix+'say') != -1:
        if cmd_say == True:
            if sender in ignored:
                pass
            else:
                try:
                    t = text.split(':'+prefix+'say ')
                    msg = t[1].strip()
                    privmsg(sendto, str(msg).encode('utf8'))
                except Exception:
                    pass

    if text.find(':'+prefix+'action') != -1:
        if cmd_action == True:
            if sender in ignored:
                pass
            else:
                try:
                    t = text.split(':'+prefix+'action ')
                    action = t[1].strip()
                    privmsg(sendto, '\x01ACTION '+str(action).encode('utf8')+'\x01')
                except Exception, e:
                    print e
                    pass
	
    if text.find(':'+prefix+'stupid') != -1:
        if cmd_stupid == True:
            if sender in ignored:
                pass
            else:
                w1 = ["Angela Merkel", "Vladimir Putin", "Ke$ha", "Justin Bieber", "Rebecca Black", "Violetta", "I", "You", "He", "She", "They", "We", "The girls", "The boys", "Students", "Teachers", "The teacher"]
                w2 = ["farted", "danced", "flew", "turned into an octopus", "sang 'My Slowianie'", "became a narwhal", "bounced on a trampoline", "took a shower", "pooped", "was sick", "read"]
                w3 = ["while", "after", "before"]
                w4 = ["the school", "Russia", "the hospital", "a toilet", "a house", "everyone", "I", "he", "she", "we", "they", "you", "a person", "elephants"]
                w5 = ["blew up", "turned into a cucumber", "made noise", "danced like crazy", "died", "moaned"]
                privmsg(sendto, random.choice(w1)+' '+random.choice(w2)+' '+random.choice(w3)+' '+random.choice(w4)+' '+random.choice(w5)+'.')
        else:
            pass
            
    if text.find(':'+prefix+'yt') != -1:
        if cmd_yt == True:
            if sender in ignored:
                pass
            else:
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
                            notice(sender, 'Could not look up video, check your ID.')
                            print "Error",e
                            pass
                    else:
                        notice(sender, 'Could not look up video, check your ID.')
                except Exception:
                    pass
        else:
            pass

    if text.find("v=") != -1:
        if cmd_yt == True:
            if sender in ignored:
                pass
            else:
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
                            likes = jsonvid['entry']['yt$rating']['numLikes']
                            dislikes = jsonvid['entry']['yt$rating']['numDislikes']
                            title = title.encode("utf8")
                            author = author.encode("utf8")
                            privmsg(sendto, '\"'+str(title)+'\" by '+str(author)+' | '+str(viewcount)+' views | 03'+str(likes)+' likes | 04'+str(dislikes)+' dislikes | 02http://youtu.be/'+str(videoid)+'')
                        except Exception, e:
                            notice(sender, 'Could not look up video, check your ID.')
                            print "Error",e
                            pass
                    else:
                        notice(sender, 'Could not look up video, check your ID.')
        else:
            pass

    if text.find(':'+prefix+'pwn') != -1:
        if cmd_pwn == True:
            if sender in ignored:
                pass
            else:
                try:
                    t = text.split(':'+prefix+'pwn ')
                    pwn = t[1].strip()
                    if pwn == botnick:
                        privmsg(sendto, 'Error: Cannot pwn self.')
                    else:
                        if sender in admins:
                            privmsg("ChanServ", 'OP '+sendto)
                            time.sleep(1)
                            privmsg(sendto, '\x01ACTION pwns '+str(pwn)+'\x01')
                            irc.send('MODE '+sendto+' +b '+str(pwn)+'\n')
                            irc.send('KICK '+sendto+' '+str(pwn)+'\n')
                            time.sleep(3)
                            irc.send('MODE '+sendto+' -b '+str(pwn)+'\n')
                            time.sleep(1)
                            privmsg("ChanServ", 'DEOP '+sendto)
                        else:
                            privmsg(sendto, '\x01ACTION pwns '+str(pwn)+'\x01')
                except Exception, e:
                    print e
                    pass
        else:
            pass

    if text.find(':'+prefix+'ignorelist') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if not ignored:
                    privmsg(sendto, 'Global ignorelist is empty.')
                else:
                    privmsg(sendto, 'Global ignorelist: '+str(ignored).translate(None, "[]'")+'.')
            except Exception:
                pass

    if text.find(':'+prefix+'adminlist') != -1:
        if sender in ignored:
            pass
        else:
            if not admins:
                privmsg(sendto, 'Global adminlist is empty.')
            else:
                privmsg(sendto, 'Global adminlist: '+str(admins).translate(None, "[]'")+'.')

    if text.find(':'+prefix+'weather') != -1:
        if cmd_weather == True:
            if sender in ignored:
                pass
            else:
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
                                privmsg(sendto, 'The current weather in your desired location is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                            else:
                                privmsg(sendto, 'The current weather in '+str(country)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                        elif len(country) == 0:
                            if len(name) == 0:
                                privmsg(sendto, 'The current weather in your desired location is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                            else:
                                privmsg(sendto, 'The current weather in '+str(name)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                        else:
                            privmsg(sendto, 'The current weather in '+str(name)+', '+str(country)+' is: '+str(cond)+'. Temperature: '+str(temp)+'C. Wind speed: '+str(wind)+' km/h. Cloud coverage: '+str(clouds)+'%.')
                    else:
                        privmsg(sendto, 'Insufficent parameters.')
                except Exception:
                    privmsg(sendto, 'Location not found, try again.')
                    pass
        else:
            pass

    if text.find(':'+prefix+'coin') != -1:
        if cmd_coin == True:
            if sender in ignored:
                pass
            else:
                lands = ["heads", "tails"]
                privmsg(sendto, sender+' flips a coin...')
                time.sleep(1)
                privmsg(sendto, 'It lands on '+random.choice(lands)+'.')
        else:
            pass

    if text.find(':'+prefix+'lastfm') != -1:
        if cmd_lastfm == True:
            if sender in ignored:
                pass
            else:
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
                    print e
                    pass

##Admin commands
    if text.find(':'+prefix+'quit') != -1:
        if sender in ignored:
            pass
        else:
            if sender == owner:
                quitmsg = ["Critical error.", "Sorry, we're closed.", "Shutting down...", "I don't blame you.", "I don't hate you.", "Goodbye!", "Disconnecting..."]
                privmsg(sendto, random.choice(quitmsg))
                irc.send('QUIT\n')
                sys.exit()
            else:
                notice(sender, 'You are not authorised to perform this command.')
            
    if text.find(':'+prefix+'nick') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender == owner:
                    t = text.split(':'+prefix+'nick ')
                    nick = t[1].strip()
                    irc.send('NICK '+str(nick)+'\n')
                    botnick = str(nick)
                    done()
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass
            
    if text.find(':'+prefix+'join') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender == owner:
                    t = text.split(':'+prefix+'join ')
                    chan = t[1].strip()
                    if chan.startswith("#"):
                        irc.send('JOIN '+str(chan)+'\n')
                        done()
                    else:
                        notice(sender, 'Bad parameters, channel names start with #')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass
            
    if text.find(':'+prefix+'part') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender == owner:
                    t = text.split(':'+prefix+'part ')
                    chan = t[1].strip()
                    if chan.startswith("#"):
                        irc.send('PART '+str(chan)+'\n')
                        done()
                    else:
                        notice(sender, 'Bad parameters, channel names start with #')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'eval') != -1:
        if sender in ignored:
            pass
        else:
            if sender == owner:
                try:
                    t = text.split(':'+prefix+'eval ')
                    evalcmd = t[1].strip()
                    exec(str(evalcmd))
                except Exception, e:
                    print e
                    pass
            else:
                notice(sender, 'You are not authorised to perform this command.')

    if text.find(':'+prefix+'raw') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender == owner:
                    t = text.split(':'+prefix+'raw ')
                    rawcode = t[1].strip()
                    if rawcode == "":
                        notice(sender, 'Raw command cannot be empty.')
                    else:
                        irc.send(str(rawcode)+'\r\n')
                        done()
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'add_admin') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender == owner:
                    t = text.split(':'+prefix+'add_admin ')
                    usr = t[1].strip()
                    if usr == "":
                        privmsg(sendto, 'Cannot add no one.')
                    elif usr == botnick:
                        privmsg(sendto, 'Cannot add self to adminlist.')
                    else:
                        if str(usr) in admins:
                            privmsg(sendto, str(usr)+' already on global adminlist.')
                        else:
                            admins.append(str(usr))
                            privmsg(sendto, str(usr)+' added to global adminlist.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'remove_admin') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
                    t = text.split(':'+prefix+'remove_admin ')
                    usr = t[1].strip()
                    if usr == "":
                        privmsg(sendto, 'Cannot remove no one.')
                    elif usr == botnick:
                        privmsg(sendto, 'Cannot remove self from adminlist.')
                    elif usr == owner:
                        privmsg(sendto, 'Cannot remove owner from adminlist.')
                    else:
                        if str(usr) in admins:
                            admins.remove(str(usr))
                            privmsg(sendto, str(usr)+' removed from global adminlist.')
                        else:
                            privmsg(sendto, str(usr)+' not on global adminlist.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'ignore') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
                    t = text.split(':'+prefix+'ignore ')
                    usr = t[1].strip()
                    if usr == "":
                        privmsg(sendto, 'Cannot ignore no one.')
                    elif usr == botnick:
                        privmsg(sendto, 'Cannot ignore self.')
                    elif usr == owner:
                        privmsg(sendto, 'Cannot ignore owner.')
                    else:
                        if str(usr) in ignored:
                            privmsg(sendto, str(usr)+' already on global ignorelist.')
                        else:
                            ignored.append(str(usr))
                            privmsg(sendto, str(usr)+' added to global ignorelist.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'unignore') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
                    t = text.split(':'+prefix+'unignore ')
                    usr = t[1].strip()
                    if usr == "":
                        privmsg(sendto, 'Cannot unignore no one.')
                    elif usr == botnick:
                        privmsg(sendto, 'Cannot unignore self.')
                    elif usr == owner:
                        privmsg(sendto, 'Cannot unignore owner.')
                    else:
                        if str(usr) in ignored:
                            ignored.remove(str(usr))
                            privmsg(sendto, str(usr)+' removed from global ignorelist.')
                        else:
                            privmsg(sendto, str(usr)+' not on global ignorelist.')
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'topic') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
                    if text.find(':'+prefix+'topic append') != -1:
                        t1 = text.split(':'+prefix+'topic append ')
                        addtopic = t1[1].strip() 
                        privmsg("ChanServ", 'OP '+sendto)
                        time.sleep(1)
                        privmsg("ChanServ", 'TOPICAPPEND '+sendto+' '+str(addtopic))
                        time.sleep(1)
                        privmsg("ChanServ", 'DEOP '+sendto)
                    elif text.find(':'+prefix+'topic prepend') != -1:
                        t4 = text.split(':'+prefix+'topic prepend ')
                        pretopic = t4[1].strip()
                        privmsg("ChanServ", 'OP '+sendto)
                        time.sleep(1)
                        privmsg("ChanServ", 'TOPICPREPEND '+sendto+' '+str(pretopic))
                        time.sleep(1)
                        privmsg("ChanServ", 'DEOP '+sendto)
                    elif text.find(':'+prefix+'topic change') != -1:
                        t2 = text.split(':'+prefix+'topic change ')
                        changetopic = t2[1].strip()
                        privmsg("ChanServ", 'OP '+sendto)
                        time.sleep(1)
                        irc.send('TOPIC '+sendto+' :'+str(changetopic)+'\r\n')
                        time.sleep(1)
                        privmsg("ChanServ", 'DEOP '+sendto)
                    elif text.find(':'+prefix+'topic lock') != -1:
                        t3 = text.split(':'+prefix+'topic lock ')
                        locktopic = t3[1].strip()
                        if locktopic == "on":
                            privmsg("ChanServ", 'OP '+sendto)
                            time.sleep(1)
                            privmsg("ChanServ", 'SET '+sendto+' TOPICLOCK ON')
                            time.sleep(1)
                            privmsg("ChanServ", 'DEOP '+sendto)
                        if locktopic == "off":
                            privmsg("ChanServ", 'OP '+sendto)
                            time.sleep(1)
                            privmsg("ChanServ", 'SET '+sendto+' TOPICLOCK OFF')
                            time.sleep(1)
                            privmsg("ChanServ", 'DEOP '+sendto)
                        else:
                            privmsg(sendto, 'Insufficent parameters.')
                            pass
                    elif text.find(':'+prefix+'topic del') != -1:
                        privmsg("ChanServ", 'OP '+sendto)
                        time.sleep(1)
                        irc.send('TOPIC '+sendto+' :''\r\n')
                        time.sleep(1)
                        privmsg("ChanServ", 'DEOP '+sendto)
                    elif text.find(':'+prefix+'topic reset') != -1:
                        privmsg("ChanServ", 'OP '+sendto)
                        time.sleep(1)
                        topic = ""
                        irc.send('TOPIC '+sendto+' :'+topic+'\r\n')
                        time.sleep(1)
                        privmsg("ChanServ", 'DEOP '+sendto)
                    else:
                        notice(sender, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'enable') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
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
                    else:
                        notice(sender, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass

    if text.find(':'+prefix+'disable') != -1:
        if sender in ignored:
            pass
        else:
            try:
                if sender in admins:
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
                    else:
                        notice(sender, 'Insufficent parameters.')
                        pass
                else:
                    notice(sender, 'You are not authorised to perform this command.')
            except Exception:
                pass
