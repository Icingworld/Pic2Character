import pygame
import cv2
import os

global removed

block = 15

character_list = []
weight = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.005, 0.004]
sum_all = []
weight_list = []
weight_list_changed = []
pygame.init()
pygame.font.init()
font = pygame.font.Font("Keyboard.ttf", block)
screen = pygame.display.set_mode((block, block))
pygame.display.set_caption("字符取模")
back_color = (255, 255, 255)


def draw(path, x, y):
    screen.blit(path, (x, y))
    pygame.display.update()


def make_list():
    with open("list.txt", "r") as f:
        character = f.read()
        f.close()
    for i in range(0, len(character)):
        character_list.append(character[i])


def write(content):
    text = font.render(content, True, (0, 0, 0), (255, 255, 255))
    draw(text, 0, -1)


def screenshot():
    rect = pygame.Rect(0, 0, block, block)
    shot = screen.subsurface(rect)
    pygame.image.save(shot, "screenshot.jpg")
    count("screenshot.jpg")


def count(content):
    pic = cv2.imread(content, 0)
    for i in range(0, len(weight)):
        sum_ = 0
        for j in range(0, block - 2 * i):
            sum_ = pic[i, j] + sum_
            sum_ = pic[block - i - 1, j] + sum_
            sum_ = pic[j, i] + sum_
            sum_ = pic[j, block - i - 1] + sum_
        sum_ = sum_ - pic[i, i] - pic[i, block - i - 1] - pic[block - i - 1, i] - pic[block - i - 1, block - i - 1]
        sum_ *= weight[i]
        sum_all.append(sum_)
    weight_all = sum(sum_all)
    sum_all.clear()
    weight_list.append(weight_all)


def gui_yi_hua():
    try:
        os.remove("character.txt")
    except IOError:
        pass
    min_ = min(weight_list)
    for num in weight_list:
        num -= min_
        weight_list_changed.append(num)
    max_ = max(weight_list_changed)
    for weight_ in weight_list_changed:
        with open("character.txt", "a+") as f1:
            f1.write(str(weight_/max_) + "\n")
            sum_all.clear()
            f1.close()


while True:
    make_list()
    for h in range(0, len(character_list)):
        screen.fill(back_color)
        write(character_list[h])
        screenshot()
    gui_yi_hua()
    os.remove("screenshot.jpg")
    exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
