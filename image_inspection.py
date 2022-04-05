import os

def is_image(fn):
    data = open(fn, 'rb').read(10)
    # check if file is JPG or JPEG
    if data[:3] == b'\xff\xd8\xff':
        print(fn+" is: JPG/JPEG.")
        return True
    return False

# go through all files in desired folder
folders = ['./images/pickup/', './images/sedan/']
for fd in folders:
    for filename in os.listdir(fd):
        if not is_image(fd + filename):  # check if file is actually an image file
            os.remove(os. path. join(fd, filename))  # if the file is not valid, remove it


