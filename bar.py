import pygame
import sys
import json 
import cv2
import os
import shutil
from pychord import Chord, find_chords_from_notes

pygame.init()

clock = pygame.time.Clock()

fps = 30

bpm = 120
bar_duration = 60/bpm*4
duration = 5

screen_width = 200
screen_height = 10
screen = pygame.Surface((screen_width, screen_height))
# screen = pygame.display.set_mode((screen_width, screen_height))

counter = 0 
play_time = 0

# image_data = []

if os.path.exists("temp_images_folder"):
    shutil.rmtree("temp_images_folder")
os.mkdir("temp_images_folder")

last_time = 0

running = True
while running:
    screen.fill("#ffffff")
    play_time += 1/fps
    
    pygame.draw.rect(screen, "#000000", [0, 0, (play_time-last_time)/bar_duration*screen_width, screen_height])

    if play_time > last_time + bar_duration:
        last_time += bar_duration
        bar = 0

    # print(duration-play_time+screen_width/2/100)
    if duration-play_time < -5:
        running = False
        
    counter += 1
    pygame.image.save(screen, f"temp_images_folder/{counter}.png")
    # clock.tick(60)
    # pygame.display.update()
 
print("1")

video = cv2.VideoWriter("res/bar.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (int(screen_width), int(screen_height)))

for file in sorted(os.listdir("temp_images_folder"), key=len):
    # print(file)
    image = cv2.imread(f"temp_images_folder/{file}")
    video.write(image)

cv2.destroyAllWindows()
video.release()

print("done!") 