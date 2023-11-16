from PIL import Image
from bitstring import BitArray

LSB_PAYLOAD_LENGTH_BITS = 32

def extract_data_from_image(image_path):
    extracted_bits = ""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            pixel_index = 0
            data_size = None
            while True:
                x = pixel_index % width
                y = pixel_index // width
                if y >= height:
                    break
                pixel = img.getpixel((x, y))
                for color in pixel[:3]:  # Look at R, G, B channels
                    extracted_bits += str(color & 1)  # Extract the LSB
                    if data_size is None and len(extracted_bits) == LSB_PAYLOAD_LENGTH_BITS:
                        data_size = int(extracted_bits, 2) * 8  # Convert to number of bits
                    if data_size is not None and len(extracted_bits) == LSB_PAYLOAD_LENGTH_BITS + data_size:
                        break
                if data_size is not None and len(extracted_bits) == LSB_PAYLOAD_LENGTH_BITS + data_size:
                    break
                pixel_index += 1
    except IOError:
        print(f"Could not open {image_path}. Check that the file exists and is a valid image file.")
        return None

    if data_size is None or len(extracted_bits) < LSB_PAYLOAD_LENGTH_BITS + data_size:
        print("Failed to extract the correct amount of data.")
        return None

    # Extract the payload size and payload data
    payload_bits = extracted_bits[LSB_PAYLOAD_LENGTH_BITS:LSB_PAYLOAD_LENGTH_BITS + data_size]
    
    # Convert bits to bytes
    try:
        payload_bytes = BitArray(bin=payload_bits).bytes
    except BitArray.Error as e:
        print(f"Error converting payload to bytes: {e}")
        return None

    return payload_bytes

# Example usage
output_image_path = '/home/deathoftitan/Documents/Cours EPITA/Python/OBFUSCATION/image-Code.png'
extracted_data = extract_data_from_image(output_image_path)
if extracted_data:
    print("Extracted data:", extracted_data)
else:
    print("No data extracted.")
