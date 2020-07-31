import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from datetime import datetime

CATEGORIES = ["front", "turned"]

def prepare(filepath):
    IMG_SIZE = 70
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    # plt.imshow(new_array, cmap='gray')
    # plt.show()
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def test(name):
    print("HERE")
    model = tf.keras.models.load_model(name + ".model")
    count = 0
    times = []
    attentionspan = []
    path = "static/images/students/" + name + "/"
    for img in os.listdir(path):
        fp = os.path.join(path, img)
        prediction = model.predict([prepare(fp)])
        if CATEGORIES[int(prediction[0][0])] == "turned":
            date = img[:11]
            date = date.replace("-", "/")
            name = img[12:-4] + " " + date +","
            if (len(times) > 0):
                # print(count-1)
                # print(times)
                pre = times[count-1]
                # print(pre[6:8])
                # print(name[6:7])
                aspan = abs(int(pre[6:8]) - int(name[6:8]))
                if (aspan > 1):
                    attentionspan.append(aspan)
                # print(aspan)
            # if pre[]
            times.append(name)
            count = count + 1


    average = 0
    print("YELLOW")

    if (len(attentionspan) > 0):
        average = int(sum(attentionspan)/len(attentionspan))

    info = [times, attentionspan, average]
    return info

    # print(times)
    # for x in times:
    #     print(x)
    # average = int(sum(attentionspan)/len(attentionspan))
    # print(average)
