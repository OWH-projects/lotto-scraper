# -*- encoding: utf-8 -*-

import requests
from bs4 import *
import datetime
import smtplib
import re 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

apmonths = [ "Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec." ]
todays_date = datetime.date.today() - datetime.timedelta(days=1)
this_day = todays_date.strftime("%d").lstrip('0')
this_month = apmonths[int(todays_date.strftime("%m"))-1]
this_weekday = todays_date.weekday()
year = todays_date.strftime("%Y")

# fetch pages, soup 'em
nelot = 'http://www.nelottery.com/homeapp/landing'
ialot = 'http://www.ialottery.com/default1.asp'
ne = requests.get(nelot)
ia = requests.get(ialot)
nesoup = BeautifulSoup(ne.text)
iasoup = BeautifulSoup(ia.text)

# common elements
newrapper = nesoup.find('div', {'class': 'lotto_wrapper'})
boxes = newrapper.find_all('div', {'class': 'transBox round numbersbox'})
iawrapper = iasoup.find('div', {'id': 'mygallery'})

# mega millions
def mm():
    if "mega millions" in boxes[1].div.a.img['src'].lower():
        try:
            jackpot_str = boxes[1].find('div', {'class': 'jackpot_text'}).string
            jackpot_date_burst = jackpot_str.split("/")
            jackpot_month = jackpot_date_burst[0][-2:]
            jackpot_day = jackpot_date_burst[1]
            jackpot_year = jackpot_date_burst[2]
            jackpot_date = datetime.datetime(int(jackpot_year), int(jackpot_month), int(jackpot_day))
            jackpot_weekday = jackpot_date.strftime("%A")        
            jackpot = boxes[1].find('div', {'class': 'jackpot'}).string
            numslist = []
            for span in boxes[1].find_all('span'):
                if span.text.isnumeric():
                    numslist.append(str(int(span.text)))
                if "MB" in span.text:
                    megaball = str(int(span.text.strip().replace("MB: ","")))
                if "MP" in span.text:
                    megaplier = str(int(span.text.strip().replace("MP: ","")))
            nums = "-".join(numslist)
            datesplosion = boxes[1].find('div', {'class': 'mmdate'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            return "<p>MEGA MILLIONS<br/>" + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + nums + ". Megaball: " + megaball + ". Megaplier: " + megaplier + ". No jackpot winner. Jackpot for " + jackpot_weekday + ", " + apmonths[int(jackpot_month)-1] + " " + jackpot_day + ": " + jackpot.lower() + ".</p>"
        except:
            return "<p>====== Mega Millions didn't work. ======</p>"
    else:
        return "<p>====== Mega Millions didn't work. ======</p>"

# pick 5 (ne)
def nepick5():
    if "pick 5" in boxes[2].div.a.img['src'].lower():
        try:
            jackpot_str = boxes[2].find('div', {'class': 'jackpot_text'}).string
            jackpot_date_burst = jackpot_str.split("/")
            jackpot_month = jackpot_date_burst[0][-2:]
            jackpot_day = jackpot_date_burst[1]
            jackpot_year = jackpot_date_burst[2]
            jackpot_date = datetime.datetime(int(jackpot_year), int(jackpot_month), int(jackpot_day))
            jackpot_weekday = jackpot_date.strftime("%A")        
            jackpot = boxes[2].find('div', {'class': 'jackpot'}).string
            numslist = []
            for span in boxes[2].find_all('span'):
                numslist.append(str(int(span.text)))
            nums = "-".join(numslist)
            datesplosion = boxes[2].find('div', {'class': 'p5date'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            return "<p>Pick 5 &mdash; " + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + nums + ". No jackpot winner. Jackpot for " + jackpot_weekday + ", " + apmonths[int(jackpot_month)-1] + " " + jackpot_day + ": " + jackpot + "</p>"
        except:
            return "<p>====== Pick 5 (NE) didn't work. ======</p>"
    else:
        return "<p>====== Pick 5 (NE) didn't work. ======</p>"

# myday (ne)
def myday():
    if "myday" in boxes[4].div.a.img['src'].lower():
        try:
            numslist = []
            for span in boxes[4].find_all('span'):
                if span.text.replace(" ","").strip().isnumeric():
                    numslist.append(str(int(span.text.replace(" ","").strip())))
            nums = "-".join(numslist)
            datesplosion = boxes[4].find('div', {'class': 'mydate'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            return "<p>MyDay &mdash; " + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + nums + ".</p>"
        except:
            return "<p>====== MyDay didn't work. ======</p>"
    else:
        return "<p>====== MyDay didn't work. ======</p>"

# 2by2 (ne)
def twoby2():
    if "2by2" in boxes[5].div.a.img['src'].lower():
        try:
            rednums = []
            whitenums = []
            for span in boxes[5].find_all('span'):
                if span.has_attr('class'):
                    rednums.append(str(int(span.text)))
                else:
                    whitenums.append(str(int(span.text)))
            datesplosion = boxes[5].find('div', {'class': 'twodate'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            red = "-".join(rednums)
            white = "-".join(whitenums)
            return "<p>2by2 &mdash; " + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": red " + red + "; white " + white + ".</p>"
        except:
            return "<p>====== 2by2 didn't work. ======</p>"
    else:
        return "<p>====== 2by2 didn't work. ======</p>"

# pick 3 (ne)
def nepick3():
    if "pick 3" in boxes[3].div.a.img['src'].lower():
        try:
            numslist = []
            for span in boxes[3].find_all('span'):
                numslist.append(str(int(span.text)))
            nums = "-".join(numslist)
            datesplosion = boxes[3].find('div', {'class': 'p3date'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            return "<p>Pick 3 &mdash; " + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + nums + ".</p>"
        except:
            return "<p>====== Pick 3 (NE) didn't work. ======</p>"
    else:
        return "<p>====== Pick 3 (NE) didn't work (couldn't find the box). ======</p>"

# all or nothing (ia)
def aon():
    target = iawrapper.find_all('div', {'class': 'panel'})[3]
    spans = target.find_all('span')
    midday_weekday = ''
    midday_month = ''
    midday_day = ''
    mid = ''
    ev = ''
    try:
        for dude in spans:
            if "midday" in dude.text.lower():
                ugh = dude.next_sibling.next_sibling.next_sibling.next_sibling.find_all('span')
                midday = []
                for thing in ugh:
                    if thing.text.isnumeric():
                        midday.append(thing.text.strip())
                mid = "-".join(midday)
                midday_date_splosion = dude.text.split("/")
                midday_date = datetime.datetime(int(year), int(midday_date_splosion[0]), int(midday_date_splosion[1][:2]))
                midday_weekday = midday_date.strftime("%A")
                midday_month = apmonths[int(midday_date.strftime("%m"))-1]
                midday_day = midday_date.strftime("%d").lstrip('0')
            if "evening" in dude.text.lower():
                calabash = dude.next_sibling.next_sibling.find_all('span')
                evening = []
                for gulp in calabash:
                    if gulp.text.isnumeric():
                        evening.append(gulp.text.strip())
                ev = "-".join(evening)
        return "<p>All or Nothing &mdash; " + midday_weekday + ", " + midday_month + " " + midday_day + ": midday " + mid + "; evening " + ev + ".</p>"
    except:
        return "<p>====== All or nothing (IA) didn't work. ======</p>"

# pick 3 (ia)
def iapick3():
    target = iawrapper.find_all('div', {'class': 'panel'})[4]
    spans = target.find_all('span')
    midday_weekday = ''
    midday_month = ''
    midday_day = ''
    mid = ''
    ev = ''
    try:
        for dude in spans:
            if "midday" in dude.text.lower():
                midday_date_splosion = dude.text.split("/")
                midday_date = datetime.datetime(int(year), int(midday_date_splosion[0]), int(midday_date_splosion[1][:2]))
                midday_weekday = midday_date.strftime("%A")
                midday_month = apmonths[int(midday_date.strftime("%m"))-1]
                midday_day = midday_date.strftime("%d").lstrip('0')
                calabash = dude.next_sibling.next_sibling.find_all('span')
                midlist = []
                for gulp in calabash:
                    midlist.append(gulp.text.strip())
                mids = "-".join(midlist)
            if "evening" in dude.text.lower():
                evspanset = dude.next_sibling.next_sibling.find_all('span')
                evlist = []
                for crunk in evspanset:
                    evlist.append(crunk.text.strip())
                evs = "-".join(evlist)
        return "<p>Pick 3 &mdash; " + midday_weekday + ", " + midday_month + " " + midday_day + ": midday " + mids + "; evening " + evs + ".</p>"
    except:
        return "<p>====== Pick 3 (IA) didn't work. ======</p>"
        
# pick 4 (ia)
def iapick4():
    target = iawrapper.find_all('div', {'class': 'panel'})[5]
    spans = target.find_all('span')
    midday_weekday = ''
    midday_month = ''
    midday_day = ''
    mid = ''
    ev = ''
    try:
        for dude in spans:
            if "midday" in dude.text.lower():
                midday_date_splosion = dude.text.split("/")
                midday_date = datetime.datetime(int(year), int(midday_date_splosion[0]), int(midday_date_splosion[1][:2]))
                midday_weekday = midday_date.strftime("%A")
                midday_month = apmonths[int(midday_date.strftime("%m"))-1]
                midday_day = midday_date.strftime("%d").lstrip('0')
                spanset = dude.next_sibling.next_sibling.find_all('span')
                midlist = []
                for mario in spanset:
                    midlist.append(mario.text.strip())
                mids = "-".join(midlist)
            if "evening" in dude.text.lower():
                evspanset = dude.next_sibling.next_sibling.find_all('span')
                evlist = []
                for crunk in evspanset:
                    evlist.append(crunk.text.strip())
                evs = "-".join(evlist)
        return "<p>Pick 4 &mdash; " + midday_weekday + ", " + midday_month + " " + midday_day + ": midday " + mids + "; evening " + evs + ".</p>"
    except:
        return "<p>====== Pick 4 (IA) didn't work. ======</p>"  

# powerball
def pb():
    if "powerball" in boxes[0].div.a.img['src'].lower():
        try:
            jackpot_str = boxes[0].find('div', {'class': 'jackpot_text'}).string
            jackpot_date_burst = jackpot_str.split("/")
            jackpot_month = jackpot_date_burst[0][-2:]
            jackpot_day = jackpot_date_burst[1]
            jackpot_year = jackpot_date_burst[2]
            jackpot_date = datetime.datetime(int(jackpot_year), int(jackpot_month), int(jackpot_day))
            jackpot_weekday = jackpot_date.strftime("%A")        
            jackpot = boxes[0].find('div', {'class': 'jackpot'}).string
            numslist = []
            for span in boxes[0].find_all('span'):
                if span.text.isnumeric():
                    numslist.append(str(int(span.text)))
                if "pb" in span.text.lower():
                    powerball = str(int(span.text.strip().replace("PB: ","")))
                if "pp" in span.text.lower():
                    powerplay = str(int(span.text.strip().replace("PP: ","")))
            nums = "-".join(numslist)
            datesplosion = boxes[0].find('div', {'class': 'pbdate'}).text.strip().split("/")
            drawdate = datetime.datetime(int(datesplosion[2]), int(datesplosion[0]), int(datesplosion[1]))
            drawdate_weekday = drawdate.strftime("%A")
            drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
            drawdate_day = drawdate.strftime("%d").lstrip('0')
            return "<p>POWERBALL<br>" + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + nums + ". Powerball: " + powerball + ". Powerplay: " + powerplay + ". No jackpot winner. Jackpot for " + jackpot_weekday + ", " + apmonths[int(jackpot_month)-1] + " " + jackpot_day + ": " + jackpot.lower() + ".</p>"
        except:
            return "<p>====== Powerball didn't work. ======</p>"
    else:
        return "<p>====== Powerball didn't work. ======</p>"

# hot lotto (ia)
def hotlotto():
    target = iawrapper.find_all('div', {'class': 'panel'})[2]
    spans = target.find_all('span')
    weekday = ''
    month = ''
    day = ''
    jackpot = ''
    drawdate_weekday = ''
    drawdate_month = ''
    drawdate_day = ''
    try:
        for dude in spans:
            if "next estimated jackpot" in dude.text.lower():
                datesplosion = dude.text.split("/")
                jackpotdate = datetime.datetime(int(datesplosion[2].replace(":","")), int(datesplosion[0][-2:]), int(datesplosion[1]))
                weekday = jackpotdate.strftime("%A")
                month = apmonths[int(jackpotdate.strftime("%m"))-1]
                day = jackpotdate.strftime("%d").lstrip('0')
            if "$" in dude.text:
                jackpot = dude.text
            if "drawing" in dude.text.lower():
                drawdate_splosion = dude.text.split("/")
                drawdate = datetime.datetime(int(year), int(drawdate_splosion[0]), int(drawdate_splosion[1][:2]))
                drawdate_weekday = drawdate.strftime("%A")
                drawdate_month = apmonths[int(drawdate.strftime("%m"))-1]
                drawdate_day = drawdate.strftime("%d").lstrip('0')
                srsly = dude.next_sibling.next_sibling.next_sibling.next_sibling.find_all('span')
                numslist = []
                for yob in srsly[:-1]:
                    numslist.append(str(int(yob.text)))
                regnums = "-".join(numslist)
                hotball = str(int(srsly[-1].text))
        return "<p>Hot Lotto &mdash; " + drawdate_weekday + ", " + drawdate_month + " " + drawdate_day + ": " + regnums + ". Hot Ball: " + hotball + ".</p>"
    except:
        return "<p>====== Hot Lotto didn't work. ======</p>"

# weekday dict (0 = Monday)
lottery = {
    0: ["NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4()],
    1: [mm(), "NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4()],
    2: [pb(), "NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4(), hotlotto()],
    3: ["NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4()],
    4: [mm(), "NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4()],
    5: [pb(), "NEBRASKA", nepick5(), myday(), twoby2(), nepick3(), "IOWA", aon(), iapick3(), iapick4(), hotlotto()],
    6: ["NEBRASKA", twoby2(), "IOWA", aon(), iapick3(), iapick4()]
}

def sendEmail():
    me = 'worldheraldbot@gmail.com'
    you = ['cody.winchester@owh.com']
    pw = # password here
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Lottery numbers for ' + this_month + ' ' + this_day + ', ' + year
    msg['From'] = "World-Herald Lottery Bot"
    msg['To'] = you
    html = "<html><body><h2>Today's lottery numbers</h2><div>" + "".join(lottery[this_weekday]) + "</div></body></html>"
    wut = MIMEText(html, 'html')
    msg.attach(wut)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(me, pw)
    server.sendmail(me, you, msg.as_string())
    server.quit()

sendEmail()