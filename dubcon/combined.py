import pysrt as ps
from moviepy.editor import *
from gtts import gTTS
from pydub import AudioSegment
import librosa
import soundfile as sf
import os



AudioSegment.converter = "ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe ="ffmpeg\\bin\\ffprobe.exe"

# get time and subs corresponding to it(with milliseconds)
def subsTime(filename):
    subs  = ps.open(filename)
    d,total_tym,total_subs,t = [],[],[],0
    for i in range(len(subs)):
        a = str(subs[i])
        a = a.split()
        d = a[4:]
        b = " ".join(d)
        c,timestamp = [],[]
        c.append(a[1])
        c.append(a[3])
        for j in c:
            temp = j.replace(",",":")
            #converting in milliseconds so that it can be used in audio cutter
            t = int(temp[0:2])*3600*1000+int(temp[3:5])*60*1000 +int(temp[6:8])*1000 + int(temp[9:])
            timestamp.append(t)
        total_tym.append(timestamp)
        total_subs.append(b)
    return total_tym,total_subs

def audioExtract(total_tym):
    #converting video to audio
    file = os.listdir('upload_video/')
    audioclip = AudioFileClip("upload_video/"+file[0])
    audioclip.write_audiofile("mp3/my_audio.mp3")

    # Opening file and extracting segment
    song = AudioSegment.from_mp3("mp3/my_audio.mp3")
    x=0
    for i in total_tym:
        startTime = i[0]
        endTime = i[1]
        extract = song[startTime:endTime]
        # Saving
        extract.export("mp3/wav/sub{}.wav".format(x), format="wav")
        x += 1

def convert_audio(total_subs):
    for i in range(len(total_subs)):
        mytext = total_subs[i]
        myobj = gTTS(text=mytext, lang='en', slow=False)
        myobj.save("mp3/converted_wav/conv{}.wav".format(i))
        converted = AudioSegment.from_mp3("mp3/converted_wav/conv{}.wav".format(i))
        subbed = AudioSegment.from_mp3("mp3/wav/sub{}.wav".format(i))
        sample_rate = int(converted.frame_rate * (len(converted) / len(subbed)))
        y, sr = librosa.load('mp3/converted_wav/conv{}.wav'.format(i), sr=None)
        sf.write('mp3/fixed_conv/changed{}.wav'.format(i), y, sample_rate)


file = os.listdir('upload_sub/')
files = os.listdir('upload_video/')
y = "upload_video/" + files[0]
x = "upload_sub/" + file[0]
total_tym,total_subs = [],[]
total_tym,total_subs = subsTime(x)
audioExtract(total_tym)
convert_audio(total_subs)
import Integrated
files_wav = os.listdir("mp3/wav/")
file_con = os.listdir("mp3/converted_wav/")
file_fix = os.listdir("mp3/fixed_conv/")
for i in file_con:
    os.remove("mp3/converted_wav/"+i)

for j in files_wav:
    os.remove("mp3/wav/"+j)

for k in file_fix:
    os.remove("mp3/fixed_conv/"+k)

os.remove(x)
os.remove(y)
os.remove("mp3/my_audio.mp3")
os.remove("mp3/sample.wav")
os.remove("mp3/stitch.mp3")


#exec(Integrated.py)
#audioExtract(total_tym)
