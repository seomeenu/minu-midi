import pygame
import sys
import json 
import cv2
import os
import shutil

pygame.init()

clock = pygame.time.Clock()

# name = input()
name = "kick"

fps = 30

bpm = 120
notes = []
duration = 0
with open(f"midis/{name}.json") as file:
    data = json.load(file)
    bpm = data["header"]["bpm"]
    notes = data["tracks"][1]["notes"]
    duration = data["duration"]

last_time = 0

screen_width = 480
screen_height = 480
# screen_width = bar_duration*100+210
# screen_height = min(dist*height+100, 720)
screen = pygame.Surface((screen_width, screen_height))
# screen = pygame.display.set_mode((screen_width, screen_heigzht))

for note in notes:
    note["anim"] = 35

counter = 0 

# image_data = []

if os.path.exists("temp_images_folder"):
    shutil.rmtree("temp_images_folder")
os.mkdir("temp_images_folder")

# start_time = pygame.time.get_ticks()
play_time = 0

running = True
while running:
    screen.fill("#eeeeee")
    play_time += 1/fps

    for note in notes:
        if play_time >= note["time"]:
            note["anim"] *= 0.73
            if int(note["anim"]) > 0:
                pygame.draw.rect(screen, "#000000", [40+note["anim"]/2, 40+note["anim"]/2, 400-note["anim"], 400-note["anim"]], int(note["anim"]))

    # print(duration-play_time+screen_width/2/100)
    if duration-play_time < -10:
        running = False
        
    counter += 1
    pygame.image.save(screen, f"temp_images_folder/{counter}.png")
    # clock.tick(60)
    # pygame.display.update()

print("1")

video = cv2.VideoWriter(f"res/{name}.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (int(screen_width), int(screen_height)))

for file in sorted(os.listdir("temp_images_folder"), key=len):
    # print(file)
    image = cv2.imread(f"temp_images_folder/{file}")
    video.write(image)

cv2.destroyAllWindows()
video.release()

print("done!") 