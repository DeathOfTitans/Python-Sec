from bitstring import BitArray
from PIL import Image
import zlib

LSB_PAYLOAD_LENGTH_BITS = 32

input_image_path = '/home/deathoftitan/Documents/Cours EPITA/Python/OBFUSCATION/image_aléatoire.png'
code_file_path = '/home/deathoftitan/Documents/Cours EPITA/Python/OBFUSCATION/code-file.txt'
output_image_path = '/home/deathoftitan/Documents/Cours EPITA/Python/OBFUSCATION/image-Code.png'

def calculate_max_data_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width * height * 3 // 8
    
def compress_data(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        return zlib.compress(data)
    
def validate_data_size(data, max_size):
    return len(data) <= max_size

max_data_size = calculate_max_data_size(input_image_path)
compressed_data = compress_data(code_file_path)

def obfuscate_via_lsb(data, input_file, output_file):
    data = BitArray(uint=len(data) * 8, length=LSB_PAYLOAD_LENGTH_BITS).bin + BitArray(bytes=data).bin

    i = 0
    try:
        with Image.open(input_file) as img:
            width, height = img.size
            if len(data) > width * height * 3:
                print("Data is too large to be embedded in the image. Data contains {} bytes, maximum is {}".format(
                    int(len(data) / 8), int(width * height * 3 / 8)))
                exit(1)
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        if i < len(data):
                            pixel[n] = pixel[n] & ~1 | int(data[i])
                            i += 1
                    img.putpixel((x, y), tuple(pixel))
                    if i >= len(data):
                        break
                if i >= len(data):
                    break
            img.save(output_file, "png")
    except IOError:
        print("Could not open {}. Check that the file exists and it is a valid image file.".format(input_file))
        exit(1)
    print("Data written to {}".format(output_file))


if validate_data_size(compressed_data, max_data_size):
    obfuscate_via_lsb(compressed_data, input_image_path, output_image_path)
else:
    print("Compressed data is too large for the image.")

