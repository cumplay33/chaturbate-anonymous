# Chaturbate Anonymous Freechat RTMP Recorder v.1.0.3 by horacio9a for Python 2.7.13

import sys, os, urllib, urllib3, ssl, re, time, datetime, requests, random, command
urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')
from colorama import init, Fore, Back, Style
from termcolor import colored
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.cfg')

init()
print
print(colored(" => START <= ", 'yellow', 'on_blue'))
print

while True:
     try:
         modellist = open(config.get('files', 'model_list'),'r')
         for (num,value) in enumerate(modellist):
            print ' =>',(num+1),value[:-1]
         print
         mn = int(raw_input(colored(" => Select CB Model URL => ", 'yellow', 'on_blue')))
         print
         break
     except ValueError:
         print
         print(colored(" => Input must be a number <= ", 'yellow', 'on_red'))
         print
model_url = open(config.get('files', 'model_list'), 'r').readlines()[mn-1][:-1]
model0 = model_url.split('://')[1]
model1 = model0.split('/')[1]
model = re.sub('/', '', model1)
print (colored(' => Selected CB Model => {} <=', 'white', 'on_blue')).format(model)
print

url ='https://chaturbate.com/{}/'.format(model)
http_pool = urllib3.connection_from_url(url)
r = http_pool.urlopen('GET',url)
enc = (r.data)
dec=urllib.unquote(enc).decode()

if "HTTP 404" not in dec:
 pwd0 = dec.split(' password: ')[1]
 pwd = pwd0.split("'")[0]

 if "currently offline" not in dec:
   hlsurl0 = dec.split("source src='")[1]
   hlsurl1 = hlsurl0.split("'")[0]

   if len(hlsurl1) > 1:
      rp0 = hlsurl1.split('rp=')[1]
      rp = rp0.split('&')[0]
      hlsurl2 = hlsurl1.split('&amp')[0]
      hlsurl = re.sub('_fast_', '_', hlsurl2)

      if "_aac" not in hlsurl:
        urlf = 'amlst'
      else:
        urlf = 'aac'

      edge0 = dec.split('//edge')[1]
      edge = edge0.split('.')[0]
      fv0 = dec.split('CBV_2p')[1]
      fv = fv0.split('.')[0]
      bg0 = dec.split("gender: '")[1]
      bg = bg0.split("'")[0]
      origin = random.randint(3,15)
      swf = 'https://chaturbate.com/static/flash/CBV_2p{}.swf'.format(fv)
      print (colored(' => INFO => HLS_URL: ({}) * BG: ({}) * EDGE: {} * ORIGIN: {} <= ', 'white', 'on_blue')).format(urlf,bg,edge,origin)

      while True:
           try:
               print
               mode = int(raw_input(colored(" => Select mode (1) REC or (0) PLAY => ", 'yellow', 'on_blue')))
               break
           except ValueError:
               print(colored("\n => Input must be a number <= ", 'yellow', 'on_red'))
      if mode == 0:
              mod = 'PLAY'
      if mode == 1:
              mod = 'REC'
      else:
              mod = 'PLAY'

      timestamp = str(time.strftime("%d%m%Y-%H%M%S"))
      path = config.get('folders', 'output_folder')
      filename = model + '_CB_' + timestamp + '.flv'
      pf = (path + filename)

      if mod == 'PLAY':
         print
         print (colored(' => Start ffplay => PLAY => {} <=', 'white', 'on_magenta')).format(filename)
         command = ('ffplay -hide_banner -loglevel panic -i {} -infbuf -autoexit -x 640 -y 480 -window_title "{} * {}"'.format(hlsurl,filename,mn))
         os.system(command)

      if mod == 'REC':
         print
         print (colored(' => Start rtmpdump => RECORD => {} <=', 'white', 'on_red')).format(filename)
         command = 'rtmpdump -r"rtmp://edge{}.stream.highwebmedia.com/live-edge" -a"live-edge" -W"{}" -p"{}" -CS:AnonymousUser -CS:{} -CS:2.{} -CS:anonymous -CS:{} --live -y"mp4:rtmp://origin{}.stream.highwebmedia.com/live-origin/{}" -o"{}" -q'.format(edge,swf,url,model,fv,rp,origin,model,pf)
         os.system(command)
         print
         time.sleep(1)    # pause 1 second
         print(colored(" => END <= ", 'yellow','on_blue'))
         sys.exit()

      else:
         time.sleep(1)    # pause 1 second
         print(colored(" => END <= ", 'yellow','on_blue'))
         sys.exit()

   else:
      print(colored(" => Model is PVT/HIDDEN or AWAY ", 'yellow','on_red'))
      print
      time.sleep(1)    # pause 1 second
      print(colored(" => END <= ", 'yellow','on_blue'))
      sys.exit()

 else:
   print(colored(" => Model is OFFLINE <= ", 'yellow','on_red'))
   print
   time.sleep(1)    # pause 1 second
   print(colored(" => END <= ", 'yellow','on_blue'))
   sys.exit()

else:
   print(colored(" => Page Not Found <= ", 'yellow','on_red'))
   print
   print(colored(" => Waiting for 3 seconds <= ", 'yellow','on_blue'))
   time.sleep(3)    # pause 3 second
   sys.exit()
