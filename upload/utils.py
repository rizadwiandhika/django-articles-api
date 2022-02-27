import imghdr

from uuid import uuid4

def is_valid_image(buff, allowedTypes = ['jpg', 'jpeg', 'png']):
    typefile = imghdr.what(buff)
    return typefile is not None and typefile in allowedTypes

def generate_filename(name):
    filename_part = name.split('.')
    name = filename_part[0].replace(' ', '-')
    ext = filename_part[-1]
    sufix = uuid4().hex

    filename = "{}-{}.{}".format(name, sufix, ext)
    return filename