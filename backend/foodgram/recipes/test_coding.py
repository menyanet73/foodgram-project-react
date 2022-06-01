from PIL import Image
import base64


def coding_to_b64():
    with open('image.jpg', 'rb') as im:
        b64_string = base64.b64encode(im.read())
    print(b64_string)
    text_file = open('salad.txt', 'wb')
    text_file.write(b64_string)
    text_file.close()
    
def decoding_to_image():
    text_file = open('salad.txt', 'rb')
    text = text_file.read()
    string = base64.b64decode(text)
    new_image = open('salad.jpg', 'wb')
    new_image.write(string)
    new_image.close()
    
decoding_to_image()