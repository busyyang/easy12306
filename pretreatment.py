#! env python
# coding: utf-8
# 功能：对图像进行预处理，将文字部分单独提取出来
# 并存放到ocr目录下
# 文件名为原验证码文件的文件名
import hashlib
import os
import pathlib

import cv2
import numpy as np
import requests
import scipy.fftpack
import json
import base64
import threading
import time

PATH = 'imgs'


def download_image():
    # 抓取验证码
    # 存放到指定path下
    # 文件名为图像的MD5
    try:
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
        r = requests.get(url)
        fn = hashlib.md5(r.content).hexdigest()
        img_str = json.loads(r.content)['image']
        with open(f'{PATH}/{fn}.jpg', 'wb') as fp:
            fp.write(base64.b64decode(img_str))
    except:
        print('获取图片失败......')


def download_images():
    pathlib.Path(PATH).mkdir(exist_ok=True)
    idx = 0
    while idx < 40000:
        if len(threading.enumerate()) < 6:
            t = threading.Thread(target=download_image)
            t.start()
            print(idx)
            idx = idx + 1
        else:
            time.sleep(1)


def get_text(img, offset=0):
    # 得到图像中的文本部分
    return img[:25, 120 + offset:177 + offset]


def avhash(im):
    im = cv2.resize(im, (8, 8), interpolation=cv2.INTER_CUBIC)
    avg = im.mean()
    im = im > avg
    im = np.packbits(im)
    return im


def phash(im):
    im = cv2.resize(im, (32, 32), interpolation=cv2.INTER_CUBIC)
    im = scipy.fftpack.dct(scipy.fftpack.dct(im, axis=0), axis=1)
    im = im[:8, :8]
    med = np.median(im)
    im = im > med
    im = np.packbits(im)
    return im


def _get_imgs(img):
    interval = 5
    length = 67
    for x in range(40, img.shape[0] - length, interval + length):
        for y in range(interval, img.shape[1] - length, interval + length):
            yield img[x:x + length, y:y + length]


def get_imgs(img):
    imgs = []
    for img in _get_imgs(img):
        imgs.append(phash(img))
    return imgs

def get_imgs_original(img):
    imgs = []
    for img in _get_imgs(img):
        imgs.append(img)
    return imgs


def pretreat():
    if False:
        download_images()
    texts, imgs, imgs_color = [], [], []
    for img in os.listdir(PATH):
        img = os.path.join(PATH, img)
        img = cv2.imread(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        texts.append(get_text(img_gray))
        imgs.append(get_imgs(img_gray))
        imgs_color.append(get_imgs_original(img))
    return texts, imgs, imgs_color


def load_data(path='./data/data.npz'):
    if not os.path.isfile(path):
        texts, imgs, imgs_color = pretreat()
        np.savez(path, texts=texts, images=imgs, images_original=imgs_color)
    f = np.load(path)
    return f['texts'], f['images'], f['images_original']


class thread_getImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        download_image()


if __name__ == '__main__':
    texts, imgs, imgs_nohash = load_data()
    print(texts.shape)
    print(imgs.shape)
    print(imgs_nohash.shape)
    imgs = imgs.reshape(-1, 8)
    print(np.unique(imgs, axis=0).shape)
