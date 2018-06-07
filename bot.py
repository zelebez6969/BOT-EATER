# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
#=================================================================#
### LOGIN SETTING DISINI ###
boteater = LINE()##LOGIN LEWAT TOKEN
boteater.log("Auth Token : " + str(boteater.authToken))
#=================================================================#
### SETTINGAN INFO ###
boteaterMID = boteater.profile.mid
boteaterProfile = boteater.getProfile()
lineSettings = boteater.getSettings()
oepoll = OEPoll(boteater)
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)
botStart = time.time()
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
myProfile["displayName"] = boteaterProfile.displayName
myProfile["statusMessage"] = boteaterProfile.statusMessage
myProfile["pictureStatus"] = boteaterProfile.pictureStatus
#=================================================================#
#=================================================================#
#=================================================================#
### KUMPULAN DEF ##
#=================================================================#
def restartBot():
    print (">SELFBOT TELAH DI RESTART<")
    backupData()
    time.sleep(1)
    python = sys.executable
    os.execl(python, python, *sys.argv)

def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    boteater.log("TERJADI ERROR : " + str(text))
    time_ = datetime.now()
    with open("error.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        boteater.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
#=================================================================#
#=================================================================#
def lineBot(op):
    try:
#=================================================================#
        if op.type == 0:
            print ("DONE")
            return
#=================================================================#
        if op.type == 5:
            print ("INFO SELBOT : ADA YANG ADD")
            if settings["autoAdd"] == True:
                boteater.sendMessage(op.param1, "=== SELFBOT V1.0 === \nTERIMAKASIH {} TELAH ADD SAYA".format(str(boteater.getContact(op.param1).displayName)))
#=================================================================#
        if op.type == 13:
            print ("INFO SELBOT : ADA YANG INVITE GRUP")
            group = boteater.getGroup(op.param1)
            if settings["autoJoin"] == True:
                boteater.acceptGroupInvitation(op.param1)
#=================================================================#
        if op.type == 24:
            print ("INFO SELBOT : LEAVE ROOM")
            if settings["autoLeave"] == True:
                boteater.leaveRoom(op.param1)
#=================================================================#
        if op.type == 25:
            print ("INFO SELBOT : MENGIRIM PESAN")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != boteater.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
#=================================================================#
#=================================================================#
                if text is None:
                    return
#=================================================================#
#=================================================================#
                if text.lower() == 'help':
                    boteater.sendMessage(to, "=== SELFBOT V.1 === \nbotmenu \nsetting \nselfmenu \ngrupmenu \nmedia \ntokenlist \nanimenew \nanimelist")
                if text.lower() == 'tokenlist':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ntoken mac \ntoken ios \ntoken chrome \ntoken win10 \ntoken desktop \ntoken done")
                elif text.lower() == 'botmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nrestart \nspeed \nstatus \nabout \nruntime \nerrorlog")
                elif text.lower() == 'setting':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nautoadd(on/off) \nautoread(on/off) \nautojoin(on/off) \nautoleave(on/off) \nautochecksticker(on/off) \ndetectmention(on/off)")
                elif text.lower() == 'selfmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nme \nmymid \nmypicture \nmyvideo \nmycover \nstealcontact(mention) \nstealmid(mention) \nstealbio(mention) \nstealpicture(mention) \nstealvideoprofile(mention) \nstealcover(mention) \ncloneprofile(mention) \nrestoreprofile \nmention")
                elif text.lower() == 'grupmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ngcreator \ngpicture \nglink \nqr(on/off) \nglist \ngmember \nginfo \ncrash")
                elif text.lower() == 'media':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ninstagraminfo(username) \ninstagrampost(username) \nyoutubes(keyword) \nimage(keyword) \nssweb(link)")
#=================================================================#
### BOT MENU COMMAND ###
#=================================================================#
#=================================================================#
                elif text.lower() == 'speed':
                    start = time.time()
                    boteater.sendMessage(to, "█▒▒▒▒▒▒▒▒▒...")
                    elapsed_time = time.time() - start
                    boteater.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    boteater.sendMessage(to, "SEDANG RESTART")
                    time.sleep(5)
                    boteater.sendMessage(to, "SUKSES!!!")
                    restartBot()
                elif text.lower() == 'errorlog':
                    with open('error.txt', 'r') as er:
                        error = er.read()
                    boteater.sendMessage(to, str(error))          
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    boteater.sendMessage(to, "BOT ALREADY RUN IN \n {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        saya = "MIDMU"
                        creator = boteater.getContact(saya)
                        ret_ = ">>> INFO BOT <<<"
                        ret_ += "\nSELFBOT PYTHON 3  V1.0"
                        ret_ += "\nBOT INI MILIK SLACKBOT TIDAK UNTUK DI PERJUAL BELIKAN!!! (GRATIS)"
                        ret_ += "\nYANG BUAT : {}".format(creator.displayName)
                        boteater.sendMessage(to, str(ret_))
                    except Exception as e:
                        boteater.sendMessage(msg.to, str(e))
                elif text.lower() == 'status':
                    try:
                        ret_ = " >>> STATUS BOT <<<"
                        if settings["autoAdd"] == True: ret_ += "\nAUTO ADD ACTIVED"
                        else: ret_ += "\nAUTO ADD NOT ACTIVED"
                        if settings["autoJoin"] == True: ret_ += "\nAUTO JOIN ACTIVED"
                        else: ret_ += "\nAUTO JOIN NOT ACTIVED"
                        if settings["autoLeave"] == True: ret_ += "\nAUTO LEAVE ACTIVED"
                        else: ret_ += "\nAUTO LEAVE NOT ACTIVED"
                        if settings["autoRead"] == True: ret_ += "\nAUTO READ ACTIVED"
                        else: ret_ += "\nAUTO READ NOT ACTIVED"
                        if settings["autochecksticker"] == True: ret_ += "\nAUTO CHECK STICKER ACTIVED"
                        else: ret_ += "\nAUTO CHECK STICKER NOT ACTIVED"
                        if settings["detectMention"] == True: ret_ += "\nDETECT MENTION ACTIVED"
                        else: ret_ += "\nDETECT MENTION NOT ACTIVED"
                        ret_ += " "
                        boteater.sendMessage(to, str(ret_))
                    except Exception as e:
                        boteater.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    boteater.sendMessage(to, "AUTO ADD IS ACTIVED")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    boteater.sendMessage(to, "AUTO ADD IS NOT ACTIVED")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    boteater.sendMessage(to, "AUTO JOIN IS IS ACTIVED")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    boteater.sendMessage(to, "AUTO JOIN IS IS NOT ACTIVED")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    boteater.sendMessage(to, "AUTO LEAVE IS ACTIVED")
                elif text.lower() == 'autojoin off':
                    settings["autoLeave"] = False
                    boteater.sendMessage(to, "AUTO LEAVE IS NOT ACTIVED")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    boteater.sendMessage(to, "AUTO READ IS ACTIVED")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    boteater.sendMessage(to, "AUTO READ IS NOT ACTIVED")
                elif text.lower() == 'autochecksticker on':
                    settings["autochecksticker"] = True
                    boteater.sendMessage(to, "AUTO zautochecksticker IS ACTIVED")
                elif text.lower() == 'autochecksticker off':
                    settings["autochecksticker"] = False
                    boteater.sendMessage(to, "AUTO zautochecksticker IS NOT ACTIVED")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    boteater.sendMessage(to, "DETECT MENTION IS ACTIVED")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    boteater.sendMessage(to, "DETECT MENTION IS NOT ACTIVED")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    boteater.sendMessage(to, "SEND CONTACT TO CLONE!!!")
#=================================================================#
### SELFBOT COMMAND ###
#=================================================================#
                elif text.lower() == 'me':
                    sendMessageWithMention(to, boteaterMID)
                    boteater.sendContact(to, boteaterMID)
                elif text.lower() == 'mymid':
                    boteater.sendMessage(msg.to,"MID KAMU : " +  msg.from_)
                elif text.lower() == 'mypicture':
                    me = boteater.getContact(boteaterMID)
                    boteater.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideo':
                    me = boteater.getContact(boteaterMID)
                    boteater.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = boteater.getContact(boteaterMID)
                    cover = boteater.getProfileCoverURL(boteaterMID)    
                    boteater.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("stealcontact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            mi_d = contact.mid
                            boteater.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("stealmid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "MID : "
                        for ls in lists:
                            ret_ += "\n{}" + ls
                        boteater.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("stealname "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            boteater.sendMessage(msg.to, "NAME : \n" + contact.displayName)
                elif msg.text.lower().startswith("stealbio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            boteater.sendMessage(msg.to, "INFO BIO : \n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("stealpicture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + boteater.getContact(ls).pictureStatus
                            boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealvideoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + boteater.getContact(ls).pictureStatus + "/vp"
                            boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealcover "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = boteater.getProfileCoverURL(ls)
                                boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            boteater.cloneContactProfile(contact)
                            boteater.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                        except:
                            boteater.sendMessage(msg.to, "Gagal clone member")
                            
                elif text.lower() == 'restoreprofile':
                    try:
                        boteaterProfile.displayName = str(myProfile["displayName"])
                        boteaterProfile.statusMessage = str(myProfile["statusMessage"])
                        boteaterProfile.pictureStatus = str(myProfile["pictureStatus"])
                        boteater.updateProfileAttribute(8, boteaterProfile.pictureStatus)
                        boteater.updateProfile(boteaterProfile)
                        boteater.sendMessage(msg.to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                    except:
                        boteater.sendMessage(msg.to, "Gagal restore profile")
#=================================================================#
#=======### COMMAND GRUP ###
#=================================================================#
                elif text.lower() == 'crash':
                    boteater.sendContact(to, "ub621484bd88d2486744123db00551d5e',")
                elif text.lower() == 'gcreator':
                    group = boteater.getGroup(to)
                    GS = group.creator.mid
                    boteater.sendContact(to, GS)
                elif text.lower() == 'gpicture':
                    group = boteater.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    boteater.sendImageWithURL(to, path)
                elif text.lower() == 'glink':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            link = boteater.reissueGroupTicket(to)
                            boteater.sendMessage(to, ">> LINK GRUP <<<\nhttps://line.me/R/ti/g/{}".format(str(link)))
                        else:
                            boteater.sendMessage(to, "QR NYA DI CLOSE")
                elif text.lower() == 'qr on':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            boteater.sendMessage(to, "QR GRUP SUDAH DI OPEN!!!")
                        else:
                            group.preventedJoinByTicket = False
                            boteater.updateGroup(group)
                            boteater.sendMessage(to, "GRUP QR OPENED!!!")
                elif text.lower() == 'qr off':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            boteater.sendMessage(to, "QR GRUP SUDAH DI CLOSE!!!")
                        else:
                            group.preventedJoinByTicket = True
                            boteater.updateGroup(group)
                            boteater.sendMessage(to, "GRUP QR CLOSED!!!")
                elif text.lower() == 'ginfo':
                    group = boteater.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "GRUP CREATOR HILANG!!!"
                    if group.preventedJoinByTicket == True:
                        gQr = "CLOSED"
                        gTicket = "Tidak ada"
                    else:
                        gQr = "OPEN"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(boteater.reissueglink(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = ">>> GRUP INFO <<<"
                    ret_ += "\nNAMA GRUP : {}".format(str(group.name))
                    ret_ += "\nCREATOR GRUP : {}".format(str(gCreator))
                    ret_ += "\nJUMBLAH MEMBER : {}".format(str(len(group.members)))
                    ret_ += "\nGRUP QR : {}".format(gQr)
                    ret_ += "\nLINK JOIN : {}".format(gTicket)
                    boteater.sendMessage(to, str(ret_))
                    boteater.sendImageWithURL(to, path)
                elif text.lower() == 'gmember':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        ret_ = ">>> LIST MEMBER <<<"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\nTOTAL MEMBER: \n{}".format(str(len(group.members)))
                        boteater.sendMessage(to, str(ret_))
                elif text.lower() == 'glist':
                        groups = boteater.groups
                        ret_ = ">>> LIST GRUP <<<"
                        no = 0 + 1
                        for gid in groups:
                            group = boteater.getGroup(gid)
                            ret_ += "\n{}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\nTOTAL GRUP : \n{}".format(str(len(groups)))
                        boteater.sendMessage(to, str(ret_))
                        
                elif text.lower() == 'mention':
                    group = boteater.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u' '
                        boteater.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        boteater.sendMessage(to, "TOTAL MENTION : \n{}".format(str(len(nama))))          
#=================================================================#
###ELIF COMMAND###
#=================================================================#
                elif text.lower() == 'kalender':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    boteater.sendMessage(msg.to, readTime)                 
                elif "ssweb" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        boteater.sendImageWithURL(to, data["result"])
                elif "instagraminfo" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.instagram.com/{}/?__a=1".format(search))
                        try:
                            data = json.loads(r.text)
                            ret_ = (">>> INFO INSTAGRAM {} <<<".format(search))
                            ret_ += "\nPROFIL : {}".format(str(data["user"]["full_name"]))
                            ret_ += "\nUSERNAME : {}".format(str(data["user"]["username"]))
                            ret_ += "\nSTATUS BIO : {}".format(str(data["user"]["biography"]))
                            ret_ += "\nFOLLOWERS : {}".format(format_number(data["user"]["followed_by"]["count"]))
                            ret_ += "\nFOLLOWING : {}".format(format_number(data["user"]["follows"]["count"]))
                            if data["user"]["is_verified"] == True:
                                ret_ += "\nSTATUS VERIFIED : VERIFIED"
                            else:
                                ret_ += "\nSTATUS VERIFIED : NOT VERIFIED"
                            if data["user"]["is_private"] == True:
                                ret_ += "\nSTATUS PRIVATE : PRIVATE"
                            else:
                                ret_ += "\nSTATUS PRIVATE : NOT PRIVATE"
                            ret_ += "\nTOTAL POST : {}".format(format_number(data["user"]["media"]["count"]))
                            ret_ += "\nLINK : https://www.instagram.com/{} ]".format(search)
                            path = data["user"]["profile_pic_url_hd"]
                            boteater.sendImageWithURL(to, str(path))
                            boteater.sendMessage(to, str(ret_))
                        except:
                            boteater.sendMessage(to, "INSTAGRAM TIDAK DI TEMUKAN")
                elif "instagrampost" in msg.text.lower():
                    separate = msg.text.split(" ")
                    user = msg.text.replace(separate[0] + " ","")
                    profile = "https://www.instagram.com/" + user
                    with requests.session() as x:
                        x.headers['user-agent'] = 'Mozilla/5.0'
                        end_cursor = ''
                        for count in range(1, 999):
                            print('PAGE: ', count)
                            r = x.get(profile, params={'max_id': end_cursor})
                        
                            data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                            j    = json.loads(data)
                        
                            for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']: 
                                if node['is_video']:
                                    page = 'https://www.instagram.com/p/' + node['code']
                                    r = x.get(page)
                                    url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                                    print(url)
                                    boteater.sendVideoWithURL(msg.to,url)
                                else:
                                    print (node['display_src'])
                                    boteater.sendImageWithURL(msg.to,node['display_src'])
                            end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
                elif "image " in msg.text.lower():
                    separate = msg.text.split(" ")
                    search = msg.text.replace(separate[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(urllib.parse.quote(search)))
                        data = r.text
                        data = json.loads(data)
                        if data["result"] != []:
                            items = data["result"]
                            path = random.choice(items)
                            a = items.index(path)
                            b = len(items)
                            boteater.sendImageWithURL(to, str(path))
                elif "youtubes" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {"search_query": search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.youtube.com/results", params = params)
                        soup = BeautifulSoup(r.content, "html5lib")
                        ret_ = ">>> HASIL YOUTUBE <<<"
                        datas = []
                        for data in soup.select(".yt-lockup-title > a[title]"):
                            if "&lists" not in data["href"]:
                                datas.append(data)
                        for data in datas:
                            ret_ += "\nJUDUL : {} ".format(str(data["title"]))
                            ret_ += "\nLINK : https://www.youtube.com{}".format(str(data["href"]))
                        boteater.sendMessage(to, str(ret_))

#=================================================================#
#######################TAMBAHAN#############################
#=================================================================#

                elif text.lower() == 'animelist':
                    data = {
                        'submit2': ''
                        }
                    r = requests.post(url = 'https://boteater.com/anime/', data = data)
                    qr= r.text
                    os.system('rm {}.txt'.format(msg._from))
                    urllib.request.urlretrieve('http://149.28.137.54/animelist.json', '{}.txt'.format(msg._from))
                    links = []
                    juduls = []
                    if r.status_code == 404:
                        boteater.sendMessage(msg.to, 'FAIL!!!')
                    else:
                        j = json.loads(qr)
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        h= ('>>ANIME LIST<<')
                        number= 1
                        try:
                            for numx in range(1000):
                                xx =juduls[numx]
                                h+= ('\n{}. {}'.format(numx, xx))
                                number += 1
                        except:
                            boteater.sendMessage(msg.to, h)
                            boteater.sendMessage(msg.to, 'PLEASE TYPE = EPPLIST [NUMBER]')
                    if text.lower() == 'animenew':
                        data = {
                            'submit1': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        qr= r.text
                        os.system('rm {}.txt'.format(msg._from))
                        urllib.request.urlretrieve('http://149.28.137.54/animebaru.json', '{}.txt'.format(msg._from))
                        links = []
                        juduls = []
                        if r.status_code == 404:
                            boteater.sendMessage(msg.to, 'FAIL!!!')
                        else:
                            j = json.loads(qr)
                            for p in j['result']:
                                juduls.append(p['judul'])
                                links.append(p['link'])
                            h= ('>>ANIME LIST<<')
                            number= 1
                            try:
                                for numx in range(1000):
                                    xx =juduls[numx]
                                    h+= ('\n{}. {}'.format(numx, xx))
                                    number += 1
                            except:
                                boteater.sendMessage(msg.to, h)
                                boteater.sendMessage(msg.to, 'PLEASE TYPE = STREAMEPPZ [NUMBER]')
                elif "epplist " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link2': '{}'.format(xx),
                            'submit4': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        qr= r.text
                        f = open('{}.txt'.format(msg._from),'w')
                        f.write(qr)
                        f.close()
                        links = []
                        juduls = []
                        if r.status_code == 404:
                            boteater.sendMessage(msg.to, 'FAIL!!! SELECT YOUR ANIME FIRST!!!')
                        else:
                            j = json.loads(qr)
                            for p in j['result']:
                                juduls.append(p['epp'])
                                links.append(p['link'])
                            h= ('>>EPISODE LIST LIST<< \n>>{}<<'.format(xxx))
                            number= 1
                            try:
                                for numx in range(1000):
                                     zzz =juduls[numx]
                                     h+= ('\n{}. {}'.format(numx, zzz))
                                     number += 1
                            except:
                                boteater.sendMessage(msg.to, h)
                                boteater.sendMessage(msg.to, 'PLEASE TYPE = STREAMEPP [NUMBER]')
                                if juduls in ["", "\n", " ",  None]:
                                    boteater.sendMessage(msg.to, 'LINK ANIME IS DIED!!')
                elif "streamepp " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['epp'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link1': '{}'.format(xx),
                            'submit3': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        link= r.text
                        boteater.sendMessage(msg.to, ">> STREAM ANIME<< \n>> {} << \n{}".format(xxx, link))
                elif "streameppz " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link1': '{}'.format(xx),
                            'submit3': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        link= r.text
                        boteater.sendMessage(msg.to, ">> STREAM ANIME<< \n>> {} << \n{}".format(xxx, link))
#=================================================================#
#                                       COMMMAND TOKEN.   
#=================================================================#
                elif text.lower() == 'token mac':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit4': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token win10':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit3': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token ios':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit2': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token chrome':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit1': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token desktop':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit7': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token done':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit5': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(to, "YOUR TOKEN SEND BY PM!!")
                    boteater.sendMessage(msg.to, '{}'.format(qr))
#=================================================================#
#=================================================================#
#=================================================================#
            elif msg.contentType == 7:
                if settings["autochecksticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = ">>> INFO STICKER <<<"
                    ret_ += "\nID STICKER : {}".format(stk_id)
                    ret_ += "\nLINK STICKER : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n>>BOTEATER STICKER DETECTED<<"
                    boteater.sendMessage(to, str(ret_))
                    
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = boteater.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        boteater.sendText(msg.to, "TARGET TIDAK DI TEMUKAN")
                        pass
                    else:
                        for target in targets:
                            try:
                                boteater.cloneContactProfile(target)
                                boteater.sendMessage(msg.to, "BERHASIL MENIRU PROFIL!!!")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
#=================================================================#
#=================================================================#
#=================================================================#
#=================================================================#
        if op.type == 26:
            print ("PENSAN TELAH DI TERIMA!!!")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != boteater.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    boteater.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        boteater.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in boteaterMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if boteaterMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = boteater.getContact(sender)
                                    boteater.sendMessage(to, "sundala nu")
                                    sendMessageWithMention(to, contact.mid)
                                break
#=================================================================#
#=================================================================#
        if op.type == 55:
            print ("PESAN TELAH DI BACA!!!")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#=================================================================#
#=================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
