import pygame
import sys
import json 
import cv2
import os
import shutil
from pychord import Chord, find_chords_from_notes

pygame.init()

clock = pygame.time.Clock()

# name = input()
name = "chords"

font = pygame.font.Font("src/GmarketSansTTFMedium.ttf", 80)
def draw_center_text(text, x, y, color="#000000", font=font, alpha=255):
    render = font.render(text, True, color)
    render.set_alpha(alpha)
    screen.blit(render, (x-render.get_width()/2, y-render.get_height()/2))

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

screen_width = 480
screen_height = 480
screen = pygame.Surface((screen_width, screen_height))
# screen = pygame.display.set_mode((screen_width, screen_height))

timings = {}
for note in notes:
    if not (note["time"] in timings):
        timings[note["time"]] = []
    timings[note["time"]].append([note["midi"], note["name"][:-1], note["duration"]])

noted_timings = {}
for timing in timings:
    new_notes = []
    dur = 0
    for note in sorted(timings[timing], key=lambda x: x[0]):
        new_notes.append(note[1])
        if note[2] > dur:
            dur = note[2]
    noted_timings[timing] = [new_notes, dur]

chord_timings = {}
for timing in noted_timings:
    chord = find_chords_from_notes(noted_timings[timing][0])
    if chord != []:
        chord_timings[timing] = [chord[0], 20, noted_timings[timing][1], 255]

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
while running:
    screen.fill("#ffffff")
    play_time += 1/fps

    for i, chord_timing in enumerate(chord_timings):
        if i+1 < len(chord_timings):
            if play_time > chord_timing:
                if list(chord_timings.keys())[i+1] > play_time:
                    chord = chord_timings[chord_timing][0]
                    chord_timings[chord_timing][1] *= 0.7
                    if chord_timing+chord_timings[chord_timing][2] < play_time:
                        chord_timings[chord_timing][3] *= 0.9
                    draw_center_text(str(chord), screen_width/2, screen_height/2+chord_timings[chord_timing][1], alpha=chord_timings[chord_timing][3])
    

    # print(duration-play_time+screen_width/2/100)
    if duration-play_time < -5:
        running = False
        
    counter += 1
    pygame.image.save(screen, f"temp_images_folder/{counter}.png")
    # clock.tick(60)
    # pygame.display.update()
 
# print("1")

video = cv2.VideoWriter(f"res/{name}.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (int(screen_width), int(screen_height)))

for file in sorted(os.listdir("temp_images_folder"), key=len):
    # print(file)
    image = cv2.imread(f"temp_images_folder/{file}")
    video.write(image)

cv2.destroyAllWindows()
video.release()

print("done!") 