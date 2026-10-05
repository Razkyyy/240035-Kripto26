'''
Nama         : Muhammad Razky Nur
NPM          : 140810240035
Nama Program : Steganography - LSB
'''
from PIL import Image

def text_to_binary(text):
    binary = ""

    for char in text:
        binary += format(ord(char), "08b")

    return binary


def binary_to_text(binary):
    text = ""

    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]

        if len(byte) == 8:
            text += chr(int(byte, 2))

    return text


def encode():
    print("\n=== ENCODE ===")

    input_image = input("Masukkan nama/path gambar: ")
    message = input("Masukkan pesan rahasia: ")
    output_image = input("Masukkan nama gambar hasil (contoh: hasil.png): ")

    try:
        image = Image.open(input_image).convert("RGB")
    except Exception:
        print("Gambar tidak dapat dibuka.")
        return

    binary_message = text_to_binary(message)

    end_marker = "1111111111111110"

    binary_message += end_marker

    width, height = image.size
    capacity = width * height * 3

    print("Jumlah bit pesan :", len(binary_message))
    print("Kapasitas gambar  :", capacity)

    if len(binary_message) > capacity:
        print("Pesan terlalu panjang untuk gambar tersebut.")
        return

    pixels = list(image.getdata())

    binary_index = 0
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel

        warna = [r, g, b]

        for i in range(3):
            if binary_index < len(binary_message):
                warna[i] = (warna[i] & ~1) | int(binary_message[binary_index])
                binary_index += 1

        new_pixels.append(tuple(warna))

    stego_image = Image.new("RGB", image.size)
    stego_image.putdata(new_pixels)

    try:
        stego_image.save(output_image, format="PNG")
        print("Encode berhasil!")
        print("Stego image disimpan sebagai:", output_image)
    except Exception:
        print("Gagal menyimpan gambar.")


def decode():
    print("\n=== DECODE ===")

    input_image = input("Masukkan nama/path stego image: ")

    try:
        image = Image.open(input_image).convert("RGB")
    except Exception:
        print("Gambar tidak dapat dibuka.")
        return

    pixels = list(image.getdata())

    binary_message = ""

    for pixel in pixels:
        r, g, b = pixel

        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    end_marker = "1111111111111110"

    end_position = binary_message.find(end_marker)

    if end_position == -1:
        print("Pesan tersembunyi tidak ditemukan.")
        return

    binary_message = binary_message[:end_position]

    if len(binary_message) % 8 != 0:
        print("Data pesan tidak valid.")
        return

    message = binary_to_text(binary_message)

    print("\nPesan tersembunyi:")
    print(message)


def main():
    while True:
        print("\n================================")
        print("     STEGANOGRAPHY - LSB")
        print("================================")
        print("1. Encode")
        print("2. Decode")
        print("3. Keluar")
        print("================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            encode()

        elif pilihan == "2":
            decode()

        elif pilihan == "3":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()