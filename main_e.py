import pygame
import sys
import json 
import cv2
import os
import shutil
from easing_functions import *

pygame.init()

clock = pygame.time.Clock()

# name = input()
name = "chords"

fps = 30

bpm = 120
notes = []
duration = 0
with open(f"midis/{name}.json") as file:
    data = json.load(file)
    bpm = data["header"]["bpm"]
    notes = data["tracks"][1]["notes"]
    duration = data["duration"]

bar_duration = 60/bpm*16
last_time = 0

max_note = max(notes, key=lambda x: x["midi"])["midi"]
min_note = min(notes, key=lambda x: x["midi"])["midi"]
middle = (max_note+min_note)//2
height = 10
dist = max_note-min_note

# screen_width = 1280
# screen_height = 720
screen_width = bar_duration*100+210
screen_height = min(dist*height+100, 720)
# screen = pygame.Surface((screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))


for note in notes:
    note["anim"] = ExponentialEaseOut(-note["duration"], 0, 2)

counter = 0 

# image_data = []

if os.path.exists("temp_images_folder"):
    shutil.rmtree("temp_images_folder")
os.mkdir("temp_images_folder")

# start_time = pygame.time.get_ticks()
play_time = 0
offset = 0
offset_vel = 0
scroll = -bar_duration*100

running = True

offset_in = QuadEaseIn(0, 1, 2)
offset_out = QuadEaseOut(-1, 0, 1)

while running:
    screen.fill("#eeeeee")
    play_time += 1/fps

    for note in notes:
        if play_time >= note["time"]:
            if bar_duration*100-10 >= note["time"]*100-scroll >= -10:
                # note["anim"] *= 0.77
                note_anim = note["anim"]((play_time-note["time"])/(note["duration"]*2))*50
                pygame.draw.rect(screen, "#000000", 
                    [
                        note["time"]*100+100+note_anim-scroll-offset,
                        (middle-note["midi"])*height+screen_height/2,
                        note["duration"]*100+note_anim,
                        10
                    ]
                )
    
    if play_time >= last_time:
        last_time += bar_duration
        scroll += bar_duration*100
        # offset = 100 

    # if play_time >= last_time-bar_duration/15.7:
    #     offset -= offset_vel/20
    #     offset_vel *= 1.7
    # else:
    #     offset_vel = 1

    # offset *= 0.9

    print(last_time-play_time)
    offset = offset_out((last_time-play_time)*2)

    # print(duration-play_time+screen_width/2/100)
    if duration-play_time < 0:
        running = False
        
    counter += 1
    # pygame.image.save(screen, f"temp_images_folder/{counter}.png")
    clock.tick(60)
    pygame.display.update()

print("1")

video = cv2.VideoWriter(f"res/{name}.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (int(screen_width), int(screen_height)))

for file in sorted(os.listdir("temp_images_folder"), key=len):
    # print(file)
    image = cv2.imread(f"temp_images_folder/{file}")
    video.write(image)

cv2.destroyAllWindows()
video.release()

print("done!") 