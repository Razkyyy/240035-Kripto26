'''
Nama        : Muhammad Razky Nur
NPM         : 140810240035
Program     : Vigenere Cipher (Encrypt & Decrypt)
'''
def extend_key(text, key):
    key = list(key.upper())
    text = text.upper()
    if len(text) == len(key):
        return "".join(key)
    else:
        extended_key = []
        for i in range(len(text)):
            extended_key.append(key[i % len(key)])
        return "".join(extended_key)


def enkripsi_vigenere(plaintext, key):
    plaintext = plaintext.upper()
    key_extended = extend_key(plaintext, key)
    ciphertext = []

    for i in range(len(plaintext)):
        x = ord(plaintext[i]) - ord("A")
        k = ord(key_extended[i]) - ord("A")

        e_x = (x + k) % 26

        char_e = chr(e_x + ord("A"))
        ciphertext.append(char_e)

    return "".join(ciphertext)


def dekripsi_vigenere(ciphertext, key):
    ciphertext = ciphertext.upper()
    key_extended = extend_key(ciphertext, key)
    plaintext = []

    for i in range(len(ciphertext)):
        x = ord(ciphertext[i]) - ord("A")
        k = ord(key_extended[i]) - ord("A")

        d_x = (x - k) % 26

        char_d = chr(d_x + ord("A"))
        plaintext.append(char_d)

    return "".join(plaintext)


if __name__ == "__main__":
    while True:
        print("\n=== PROGRAM VIGENERE CIPHER ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")
        
        pilihan = input("Pilih operasi (1/2/3): ")

        if pilihan == "1":
            print("\n--- ENKRIPSI ---")
            pt = input("Masukkan Plaintext : ").replace(" ", "")
            k = input("Masukkan Key       : ").replace(" ", "")
            
            if not pt or not k:
                print("Teks dan Kunci tidak boleh kosong!")
                continue

            ct = enkripsi_vigenere(pt, k)
            
            print("\n[HASIL]")
            print(f"Plaintext (Pt)  : {pt.upper()}")
            print(f"Key (K)         : {k.upper()}")
            print(f"Ciphertext (Ct) : {ct}")

        elif pilihan == "2":
            print("\n--- DEKRIPSI ---")
            ct = input("Masukkan Ciphertext : ").replace(" ", "")
            k = input("Masukkan Key        : ").replace(" ", "")
            
            if not ct or not k:
                print("Teks dan Kunci tidak boleh kosong!")
                continue

            pt = dekripsi_vigenere(ct, k)
            
            print("\n[HASIL]")
            print(f"Ciphertext (Ct) : {ct.upper()}")
            print(f"Key (K)         : {k.upper()}")
            print(f"Hasil Dekripsi  : {pt}")

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan program Vigenere Cipher. Sampai jumpa!")
            break

        else:
            print("\nPilihan tidak valid. Silakan ketik 1, 2, atau 3.")