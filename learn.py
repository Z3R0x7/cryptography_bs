from PIL import Image


def encrypt_message(message, image_path):
    with Image.open(image_path) as image:
        # Convert the image to RGB format
        image = image.convert("RGB")

        # Initialize a variable to keep track of the current pixel
        current_pixel = 0

        # Iterate over the characters of the message
        for char in message:
            # Convert the character to its binary representation
            binary_char = format(ord(char), '08b')

            # Iterate over the bits of the binary character
            for bit in binary_char:
                # Get the current pixel's color channels
                r, g, b = image.getpixel((current_pixel, 0))

                # Change the least significant bit of the current color channel to the current bit of the message
                if bit == '0':
                    r = r & ~1
                    g = g & ~1
                    b = b & ~1
                else:
                    r = r | 1
                    g = g | 1
                    b = b | 1

                # Set the current pixel's color channels
                image.putpixel((current_pixel, 0), (r, g, b))

                # Go to the next pixel
                current_pixel += 1

        # Save the image with the hidden message
        image.save("encrypted_image.png")
        return "Encryption done successfully"


def decrypt_message(image_path):
    with Image.open(image_path) as image:
        # Convert the image to RGB format
        image = image.convert("RGB")

        # Initialize a variable to store the decoded message
        message = ""

        # Iterate over the pixels of the image
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))

                # Append the least significant bit of each color channel to the message
                message += str(r & 1)
                message += str(g & 1)
                message += str(b & 1)
                if len(message) % 8 == 0:
                    message += " "

        # Convert the binary message to a string
        decoded_message = ''.join(
            chr(int(message[i:i+8], 2)) for i in range(0, len(message), 8))
        return decoded_message


'''
message = input("Enter the message to be encrypted:")
image_path = input("Enter the path of the image:")
encryption_status = encrypt_message(message, image_path)
print(encryption_status)
'''
image_path = input("Enter the path of the image to decrypt the message:")
decoded_message = decrypt_message(image_path)
print("Decrypted message: " + decoded_message)
