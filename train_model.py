import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import warnings

warnings.filterwarnings("ignore")

width = 80  # Width of all utils
height = 75  # Height of all utils


# A function for get utils and their labels by given image paths
def get_images_and_labels(images):
    list_imgs = []  # A list for store the utils
    list_labels = []  # A list for store the labels

    for img_path in images:
        filename = os.path.basename(img_path)  # Get filename from img_path
        label = filename.split("_")[0]  # Get label from filename
        grey_image = Image.open(img_path).convert("L")  # Convert RGB image to grey_scale image
        img = np.array(grey_image.resize((width, height)))  # Resize the grey image and convert it to numpy array
        img = img / 255  # Normalize the image array
        list_imgs.append(img)  # Append image array to X
        list_labels.append(label)  # Append label to Y

    arr_imgs = np.array(list_imgs)  # Convert list X to numpy array
    arr_imgs = arr_imgs.reshape(arr_imgs.shape[0], width, height, 1)  # Reshape the X

    return arr_imgs, list_labels


# A function for convert labels to onehot labels for training
def onehot_labels(labels):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(labels)
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_labels = onehot_encoder.fit_transform(integer_encoded)
    return onehot_labels


# A function for create a CNN model and return it
def get_CNN_model():
    model = Sequential()

    model.add(Conv2D(16, kernel_size=(5, 5), activation="relu", input_shape=(width, height, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, kernel_size=(5, 5), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(5, 5), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))  # For regularization
    model.add(Dense(3, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    return model


# Plot number of data categorical
def plot_data():
    # Plot number of the data for each class
    sns.countplot(labels)
    values, counts = np.unique(labels, return_counts=True)
    print(values, counts)
    plt.title('Number of data for each class')
    plt.show()

    # Plot number of the data for train and test set
    train_size = int(len(images) * 0.9)  # %90
    test_size = int(len(images) * 0.1)  # %10
    print('train: ' + str(train_size), ' - test: ' + str(test_size))
    sets = ['Train', 'Test']
    number_of_data = [train_size, test_size]
    plt.bar(sets, number_of_data, color=['orange', "teal"])
    plt.title('Number of data for train and test set')
    plt.ylabel('count')
    plt.show()


# Plot confusion matrix of trained model
def plot_confusion_matrix():
    pred_imgs = model.predict(test_imgs)
    pred_imgs = np.argmax(pred_imgs, axis=1)
    test_labels_new = np.argmax(test_labels, axis=1)

    cm = confusion_matrix(test_labels_new, pred_imgs)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["down", "right", "up"])

    disp = disp.plot(include_values=True, cmap='Blues', ax=None, xticks_rotation='horizontal')
    plt.title('Confusion Matrix')
    plt.show()


# Plot accuracy and loss of the model while training
def plot_accuracy_and_loss():
    plt.plot(history.history['accuracy'], linewidth=2)
    plt.title('Train Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.show()

    plt.plot(history.history['loss'], color='orange', linewidth=2)
    plt.title('Train Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.show()


# MAIN PROGRAM
if __name__ == "__main__":
    images = glob.glob("D:/AI-training/Dino2/*.png")  # Get all image paths with glob

    imgs, labels = get_images_and_labels(images)  # Get utils and their labels

    plot_data()  # Plot number of data categorical

    labels = onehot_labels(labels)  # Convert labels to onehot labels ==> down: 100, right: 010, up: 001

    train_imgs, test_imgs, train_labels, test_labels = train_test_split(imgs, labels, test_size=0.1, random_state=10)  # Split the dataset
    model = get_CNN_model()
    print(model.summary())  # Print model summary

    history = model.fit(train_imgs, train_labels, epochs=10, batch_size=64)

    train_accuracy = model.evaluate(train_imgs, train_labels)
    print("Train accuracy: %", train_accuracy[1] * 100)

    test_accuracy = model.evaluate(test_imgs, test_labels)
    print("Test accuracy: %", test_accuracy[1] * 100)

    plot_accuracy_and_loss()  # Plot accuracy and loss of the model while training
    plot_confusion_matrix()  # Plot confusion matrix of trained model

    open("model.json", "w").write(model.to_json())
    model.save_weights("weights.h5")
