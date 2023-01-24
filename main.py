# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
import os
from Crypto.Cipher import AES
from PyPDF4 import PdfFileReader, PdfFileWriter
# Convert encoding data into 8-bit binary
# form using ASCII value of characters


def genData(data):

    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Pixels are modified according to thepython
# 8-bit binary data and finally returned


def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image


def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image


def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

# ceaser chipher


def encrypt(text, s):
    result = ""
   # transverse the plain text
    for i in range(len(text)):
        char = text[i]
      # Encrypt uppercase characters in plain text

        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
      # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


def decrypt(text, s):
    plaintext = ""
    for c in text:
        if c.isalpha():
            shifted_c = chr((ord(c) - ord('A') - s) % 26 + ord('A'))
            plaintext += shifted_c
        else:
            plaintext += c
    return plaintext
######
######


def encrypt_file(file_path, key):
    # Generate a random initialization vector
    iv = os.urandom(16)

    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Read the file to be encrypted
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Pad the plaintext to a multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length

    # Encrypt the plaintext
    ciphertext = cipher.encrypt(plaintext)

    # Write the ciphertext to a new file
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as file:
        file.write(iv + ciphertext)


def decrypt_file(file_path, key):
    # Read the initialization vector and ciphertext from the file
    with open(file_path, 'rb') as file:
        iv = file.read(16)
        ciphertext = file.read()

    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    plaintext = cipher.decrypt(ciphertext)

    # Remove the padding from the plaintext
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]

    # Write the plaintext to a new file
    decrypted_file_path = file_path + '.decrypted'
    with open(decrypted_file_path, 'wb') as file:
        file.write(plaintext)
#####
#####


def pdf_password():
    file_path = input("Enter the file path:")
    password = input("Enter the password you want to set:")
    pdf = PdfFileReader(file_path)
    writer = PdfFileWriter()
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        writer.addPage(page)

    writer.encrypt(password)
    with open('encrypted_'+file_path, 'wb') as output_file:
        writer.write(output_file)
#####
# Main Function


def main():
    print("###: Welcome to Heartbeat :###\n"
          "1. Stegnography\n2. Text chiper\n3. File encrypter\n4. PDF encrypter\n")
    x = int(input("Enter your option: "))

    # STEGNOGRAPHY CODE
    if (x == 1):
        print('::STEGANOGRAPHY::\n'
              "1. Encode\n2. Decode\n")
        a = int(input("Enter you option: "))
        if (a == 1):
            encode()

        elif (a == 2):
            print("Decoded Word : " + decode())
        else:
            raise Exception("Enter correct input")
    if (x == 2):
        print('::Caesar cipher::\n'
              "1. Encode\n2. Decode\n")
        a = int(input("Enter you option: "))
        if (a == 1):
            text = input("enter the text: ")
            s = int(input("enter the shift: "))
            print("the chipher is: ", encrypt(text, s))
        elif(a == 2):
            text = input("enter the encrypted: ")
            s = int(input("enter the shift: "))
            print("the message is: ", decrypt(text, s))
    if (x == 3):
        encrypt_file('file.txt', b'keykeykeykeykeyk')
    if (x == 4):
        pdf_password()

    # TEXT CIPHER (IDIVISUALLY)

    #

    """
    # CODE I DON"T NEED NOW
    
    if (a == 1):
        encode()

    elif (a == 2):
        print("Decoded Word : " + decode())
    else:
        raise Exception("Enter correct input")
    """


# Driver Code
if __name__ == '__main__':

    # Calling main function1
    main()
