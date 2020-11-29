from pydub import AudioSegment
import pysrt as ps
from moviepy.editor import *

AudioSegment.converter = "ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe ="ffmpeg\\bin\\ffprobe.exe"

subs  = ps.open("upload_sub/rick.srt")
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

sample = AudioSegment.from_file("mp3/my_audio.mp3")
sample.export("mp3/sample.wav", format="wav")

part1 = AudioSegment.from_file("mp3/fixed_conv/changed0.wav")
part2 = AudioSegment.from_file("mp3/sample.wav")

part3 = part2[:total_tym[0][0]]

for i in range(len(total_tym)-2):
    part1 = AudioSegment.from_file("mp3/fixed_conv/changed{}.wav".format(i))
    part3 += part1 + part2[(total_tym[i][1]+1):(total_tym[i+1][0])]

part1 = AudioSegment.from_file("mp3/fixed_conv/changed{}.wav".format(len(total_tym)-1))
part3 += part1 + part2[(total_tym[len(total_tym)-1][1]+1):]
part3.export("mp3/stitch.mp3", format="mp3")

file = os.listdir('upload_video/')
videoclip = VideoFileClip("upload_video/"+file[0])
audioclip = AudioFileClip("mp3/stitch.mp3")

videoclip.audio = audioclip
videoclip.write_videofile("final/final.mp4")
