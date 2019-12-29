import numpy as np
import cv2
import mlearn
from keras.utils import to_categorical
import os
from pretreatment import load_data, phash


def load_true_labels(path='classify-true'):
    filelist = os.listdir(path)
    class_result = [(int(f.split('.')[0]), int(f.split('.')[1])) for f in filelist]
    class_result = sorted(class_result, key=lambda x: x[1], reverse=False)
    return np.array(class_result)[:, 0]


def learn():
    texts, imgs, imgs_nohash = load_data()
    labels = load_true_labels()

    # labels = mlearn.predict(texts)
    # labels = labels.argmax(axis=1)
    imgs.dtype = np.uint64
    imgs.shape = (-1, 8)
    imgs_nohash = imgs_nohash.reshape(-1, imgs_nohash.shape[2], imgs_nohash.shape[3], imgs_nohash.shape[4])
    unique_imgs = np.unique(imgs)
    unique_imgs_nohash = np.unique(imgs_nohash, axis=0)
    print(unique_imgs.shape)
    imgs_labels = []
    for img in unique_imgs:
        idxs = np.where(imgs == img)[0]
        counts = np.bincount(labels[idxs], minlength=80)
        imgs_labels.append(counts)
    np.savez('./data/images.npz', images=unique_imgs, labels=imgs_labels)
    # imgs_labels = np.argmax(imgs_labels, axis=1)
    image_color = []
    image_label = []
    for i in range(len(unique_imgs_nohash)):
        tmp_color = imgs_nohash[i, :, :, :]
        tmp_img = cv2.cvtColor(tmp_color, cv2.COLOR_RGB2GRAY)
        tmp_hash = phash(tmp_img)
        tmp_hash.dtype = np.uint64
        tmp_index = np.where(unique_imgs == tmp_hash)
        # fn = f'captcha_imgs/{imgs_labels[tmp_index][0]}.{i}.jpg'
        # cv2.imwrite(fn, tmp_color)
        image_color.append(tmp_color)
        image_label.append(imgs_labels[tmp_index[0][0]])
    print(np.array(image_color).shape)
    print(np.array(image_label).shape)
    np.savez('./data/my_captcha.npz', images=np.array(image_color), labels=np.array(image_label))


if __name__ == '__main__':
    learn()
