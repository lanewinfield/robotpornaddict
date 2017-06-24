import httplib, urllib, base64, json

from moviepy.editor import *
from pytube import YouTube
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import random
from random import randint

from twython import Twython


from gtts import gTTS




def getDescription(img):
	headers = {
	    # Request headers
	    'Content-Type': 'application/octet-stream',
	    'Ocp-Apim-Subscription-Key': '', # KEY FOR AZURE
	}

	params = urllib.urlencode({
	    # Request parameters
	    # 'language': 'unk',
	    # 'detectOrientation ': 'true',
	})

	data = open(img, 'rb').read()
	conn = httplib.HTTPSConnection('api.projectoxford.ai')
	conn.request("POST", "/vision/v1.0/analyze?visualFeatures=Description%s" % params, data, headers)
	response = conn.getresponse()
	data = response.read()
	thejson = json.loads(data)
	conn.close()

	return thejson["description"]["captions"][0]["text"]


def deleteOldVideo():
	# DELETE OLD VIDEO 

	try:
	    os.remove('/home/brian/porn/input.mp4')
	    print "input.mp4 deleted"
	except OSError:
	    pass

	try:
	    os.remove('/home/brian/porn/video1.mp4')
	    print "video1.mp4 deleted"
	except OSError:
	    pass

	try:
	    os.remove('/home/brian/porn/video2.mp4')
	    print "video2.mp4 deleted"
	except OSError:
	    pass

	try:
	    os.remove('/home/brian/porn/video3.mp4')
	    print "video3.mp4 deleted"
	except OSError:
	    pass


deleteOldVideo()

command = "/usr/local/bin/youtube-dl -o /home/brian/porn/input.mp4 http://pornhub.com/random"

print command

os.system(command)






time_middle = int(VideoFileClip("/home/brian/porn/input.mp4").duration/2)
time_beginning = int(VideoFileClip("/home/brian/porn/input.mp4").duration*0.2)
time_end = int(VideoFileClip("/home/brian/porn/input.mp4").duration*0.8)

command = "/home/brian/tobecontinued/ffmpeg-3.2-64bit-static/ffmpeg -i /home/brian/porn/input.mp4 -ss "+str(time_beginning)+" -t 5 /home/brian/porn/video1.mp4"

print command

os.system(command)

command = "/home/brian/tobecontinued/ffmpeg-3.2-64bit-static/ffmpeg -i /home/brian/porn/input.mp4 -ss "+str(time_middle)+" -t 5 /home/brian/porn/video2.mp4"

print command

os.system(command)

command = "/home/brian/tobecontinued/ffmpeg-3.2-64bit-static/ffmpeg -i /home/brian/porn/input.mp4 -ss "+str(time_end)+" -t 5 /home/brian/porn/video3.mp4"

print command

os.system(command)



clip1 = VideoFileClip("/home/brian/porn/video1.mp4")
clip2 = VideoFileClip("/home/brian/porn/video2.mp4")
clip3 = VideoFileClip("/home/brian/porn/video3.mp4")

smallclip1 = clip1.resize((11, 6))
smallclip2 = clip2.resize((11, 6))
smallclip3 = clip3.resize((11, 6))

regularclip1 = smallclip1.resize((1280, 720))
regularclip2 = smallclip2.resize((1280, 720))
regularclip3 = smallclip3.resize((1280, 720))


screensize = clip1.size


clip1.save_frame("/home/brian/porn/frame1.png", t=0)
clip2.save_frame("/home/brian/porn/frame2.png", t=0)
clip3.save_frame("/home/brian/porn/frame3.png", t=0)

descriptions = [getDescription("/home/brian/porn/frame1.png")+"?", getDescription("/home/brian/porn/frame2.png")+"?", getDescription("/home/brian/porn/frame3.png")+"?"]



# AUDIO
i = 1
for s in descriptions:
	tts = gTTS(text=s, lang='en')
	tts.save("/home/brian/porn/audio"+str(i)+".mp3")
	i = i+1

textclip1 = TextClip(descriptions[0], fontsize=70, color="white", method="caption", align="center", font="/home/brian/porn/InputSans-Black.ttf", size=[600, 950]).set_duration(5)
textclip2 = TextClip(descriptions[1], fontsize=70, color="white", method="caption", align="center", font="/home/brian/porn/InputSans-Black.ttf", size=[600, 950]).set_duration(5)
textclip3 = TextClip(descriptions[2], fontsize=70, color="white", method="caption", align="center", font="/home/brian/porn/InputSans-Black.ttf", size=[600, 950]).set_duration(5)

audioclip1 = AudioFileClip("/home/brian/porn/audio1.mp3")
audioclip2 = AudioFileClip("/home/brian/porn/audio2.mp3")
audioclip3 = AudioFileClip("/home/brian/porn/audio3.mp3")

concClip = concatenate_videoclips([regularclip1, regularclip2, regularclip3])

comp = CompositeAudioClip([concClip.audio.volumex(0.6),audioclip1.set_start(1),audioclip2.set_start(6),audioclip3.set_start(11)])

final_clip = CompositeVideoClip([concClip, textclip1.set_pos(('center', 'center')).set_start(0), textclip2.set_pos(('center', 'center')).set_start(5), textclip3.set_pos(('center', 'center')).set_start(10)]).set_audio(comp).set_duration(15)
	




final_clip.write_videofile("/home/brian/porn/final.mp4",audio_codec='aac')


# TWEET IT


APP_KEY = ''
APP_SECRET = ''
ACCESS_KEY = ''#keep the quotes, replace this with your access token
ACCESS_SECRET = ''#keep the quotes, replace this with your access token secret

twitter = Twython(APP_KEY, APP_SECRET, ACCESS_KEY, ACCESS_SECRET)

tweetCopy = descriptions[0]
 
video = open('/home/brian/porn/final.mp4', 'rb')
response = twitter.upload_video(media=video, media_type='video/mp4')
twitter.update_status(status=tweetCopy, media_ids=[response['media_id']])