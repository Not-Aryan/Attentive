import numpy as np 
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

# def create_training_data():
#     for category in CATEGORIES:  # do dogs and cats
#         path = os.path.join(DATADIR,category)  # create path to dogs and cats
#         class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat

#         for img in (os.listdir(path)):  # iterate over each image per dogs and cats
#             try:
#                 img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
#                 new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
#                 training_data.append([new_array, class_num])  # add this to our training_data
#             except Exception as e:  # in the interest in keeping the output clean...
#                 pass
#             #except OSError as e:
#             #    print("OSErrroBad img most likely", e, os.path.join(path,img))
#             #except Exception as e:
#             #    print("general exception", e, os.path.join(path,img))

def prep(name):    
    DATADIR = str('static/datasets/'+str(name))

    CATEGORIES = ["front", "turned"]

    for category in CATEGORIES:
        path = os.path.join(DATADIR,category)
        for img in os.listdir(path):
            img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
            break 
        break

    IMG_SIZE = 70

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    plt.imshow(new_array, cmap='gray')
    plt.show()

    training_data = []

    for category in CATEGORIES:  # do dogs and cats
        path = os.path.join(DATADIR,category)  # create path to dogs and cats
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat

        for img in (os.listdir(path)):  # iterate over each image per dogs and cats
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass
            #except OSError as e:
            #    print("OSErrroBad img most likely", e, os.path.join(path,img))
            #except Exception as e:
            #    print("general exception", e, os.path.join(path,img))

    random.shuffle(training_data)
    X = []
    y = []
    for features,label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    stuff = [X, y]

    return stuff

# pickle_out = open("X-real.pickle","wb")
# pickle.dump(X, pickle_out)
# pickle_out.close()

# pickle_out = open("y-real.pickle","wb")
# pickle.dump(y, pickle_out)
# pickle_out.close()


# pickle_in = open("X-real.pickle","rb")
# X = pickle.load(pickle_in)

# pickle_in = open("y-real.pickle","rb")
# y = pickle.load(pickle_in)










