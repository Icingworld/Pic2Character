import cv2
import os
import pygame

global crop, size
block = 10
path = ""  # path of raw pic
character_list = []
character_list_weight = []
test = []


def pic2thr(path_):
    global crop, size
    # 图片灰度化，并进行裁剪
    img = cv2.imread(path_, 0)
    size = img.shape
    if (size[1] % block) != 0:
        zuo = int(size[1] % block / 2)
        you = int(size[1] % block / 2) + size[1] % block % 2
    else:
        zuo = 0
        you = 0
    if (size[0] % block) != 0:
        shang = int(size[0] % block / 2)
        xia = int(size[0] % block / 2) + size[0] % block % 2
    else:
        shang = 0
        xia = 0
    crop = img[0 + shang:size[0] - xia, 0 + zuo:size[1] - you]
    cv2.imwrite("Cut.jpg", crop)
    crop = cv2.transpose(crop, crop)
    size = (size[1] - zuo - you, size[0] - shang - xia)
    return crop, size


def make_list():
    with open("list.txt", "r") as f:
        characters = f.read()
        f.close()
    for k in range(0, len(characters)):
        character_list.append(characters[k])
    with open("character.txt", "r") as f:
        characters = f.readlines()
        f.close()
    for k in range(0, len(characters)):
        character_list_weight.append(float(characters[k].strip()))


make_list()
pic2thr(path)
weight = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.005, 0.004]
charge = 1
change = 0
min_ = max_ = 0
sum_all = []
real = []
pygame.init()
pygame.font.init()
font = pygame.font.Font("Keyboard.ttf", block)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("图片转字符")
back_color = (255, 255, 255)
raw = pygame.image.load("Cut.jpg")


def screenshot():
    rect = pygame.Rect(0, 0, size[0], size[1])
    shot = screen.subsurface(rect)
    pygame.image.save(shot, "trans.jpg")


def write(content, x, y):
    position = (x, y, block, block)
    text = font.render(content, True, (0, 0, 0), (255, 255, 255))
    pygame.draw.rect(screen, (255, 255, 255), position, 0)
    draw(text, x, y)


def draw(_path, x, y):
    screen.blit(_path, (x, y))
    pygame.display.update()


while True:
    if change != 2:
        draw(raw, 0, 0)
        if change == 1:
            os.remove("Cut.jpg")
        for ii in range(0, int(size[0] / block)):
            for jj in range(0, int(size[1] / block)):
                for i in range(0, len(weight)):
                    sum_ = 0
                    for j in range(0, block-2*i):
                        sum_ = crop[ii*block+i, jj*block+j] + sum_
                        sum_ = crop[(ii+1)*block-i-1, jj*block+j] + sum_
                        sum_ = crop[ii*block+j, jj*block+i] + sum_
                        sum_ = crop[ii*block+j, (jj+1)*block-i-1] + sum_
                    sum_ = sum_-crop[ii*block+i, jj*block+i]
                    sum_ = sum_-crop[ii*block+i, (jj+1)*block-i-1]
                    sum_ = sum_-crop[(ii+1)*block-i-1, jj*block+i]
                    sum_ = sum_-crop[(ii+1)*block-i-1, (jj+1)*block-i-1]
                    sum_ *= weight[i]
                    sum_all.append(sum_)
                weight_all = sum(sum_all)
                test.append(weight_all)
                sum_all.clear()
                if change == 1:
                    weight_all -= min_
                    weight_all /= max_
                    character_list_backup = []
                    for num in character_list_weight:
                        num -= weight_all
                        character_list_backup.append(num)
                    for cha in character_list_backup:
                        if cha <= 0:
                            cha *= -1
                            real.append(cha)
                        else:
                            real.append(cha)
                    min_num = min(real)
                    index_ = real.index(min_num)
                    character = character_list[index_]
                    write(character, ii*block, jj*block)
                    real.clear()
        change += 1
        min_ = min(test)
        max_ = max(test)
        screenshot()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
