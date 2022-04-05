import tensorflow as tf
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import os


def is_image(fn):
    data = open(fn, 'rb').read(10)
    # check if file is JPG or JPEG
    if data[:3] == b'\xff\xd8\xff':
        print(fn + " is: JPG/JPEG.")
        return True
    return False


# go through all files in desired folder ###############################################################################
folders = ['./animals/lion mammal/', './animals/leopard mammal/', './animals/puma mammal/']
for fd in folders:
    for filename in os.listdir(fd):
        if not is_image(fd + filename):  # check if file is actually an image file
            os.remove(os.path.join(fd, filename))  # if the file is not valid, remove it

img_height, img_width = [256, 256]
batch_size = 72
# POSSIBILY LARGER BATCH ###############################################################################################

# CHANGE ###############################################################################################################
data_dir = './Traffic Signs/'
data_dir = pathlib.Path(data_dir)

train_ds = tf.keras.utils.image_dataset_from_directory(data_dir, validation_split=0.2, subset="training", seed=123,
                                                       image_size=(img_height, img_width), batch_size=batch_size)
val_ds = tf.keras.utils.image_dataset_from_directory(data_dir, validation_split=0.2, subset="validation", seed=123,
                                                     image_size=(img_height, img_width), batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

normalization_layer = tf.keras.layers.Rescaling(1. / 255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# CHANGE ###############################################################################################################
num_classes = 4

model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1. / 255),
    tf.keras.layers.Conv2D(72, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(56, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(40, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(24, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(10, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(3, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes)
])

model.compile(optimizer='adam', loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = model.fit(train_ds, validation_data=val_ds,
                    epochs=300)  # EPOCHS #############################################

y_vloss = history.history['val_loss']
y_loss = history.history['loss']
y_acc = history.history['accuracy']
y_vacc = history.history['val_accuracy']

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(np.arange(len(y_vloss)), y_vloss, marker='.', c='red')
ax1.plot(np.arange(len(y_loss)), y_loss, marker='.', c='blue')
ax1.grid()
plt.setp(ax1, xlabel='epoch', ylabel='loss')

ax2.plot(np.arange(len(y_vacc)), y_vacc, marker='.', c='red')
ax2.plot(np.arange(len(y_acc)), y_acc, marker='.', c='blue')
ax2.grid()
plt.setp(ax2, xlabel='epoch', ylabel='accuracy')

plt.show()
