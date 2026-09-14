'''
NAMA            : Muhammad Razky Nur
NPM             : 140810240035
Nama Program    : Encrypt, Decrypt, Find key algoritma Hill Cipher
'''
from math import gcd
import itertools

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def prepare_text(text, block_size):
    clean_text = ''.join(filter(str.isalpha, text.upper()))
    remainder = len(clean_text) % block_size
    if remainder != 0:
        clean_text += 'X' * (block_size - remainder)
    return clean_text

def matrix_det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * matrix_det(minor)
    return det

def matrix_adjugate(matrix):
    n = len(matrix)
    if n == 2:
        return [
            [matrix[1][1], -matrix[0][1]],
            [-matrix[1][0], matrix[0][0]]
        ]
    
    adj = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            minor = [row[:c] + row[c+1:] for row in (matrix[:r] + matrix[r+1:])]
            cofactor = ((-1) ** (r + c)) * matrix_det(minor)
            adj[c][r] = cofactor
    return adj

def matrix_inverse_mod26(matrix):
    det = matrix_det(matrix) % 26
    if gcd(det, 26) != 1:
        raise ValueError(f"Determinan ({det}) tidak koprima dengan 26! Matriks tidak memiliki invers.")
    
    det_inv = pow(det, -1, 26)
    adj = matrix_adjugate(matrix)
    n = len(matrix)
    
    return [[(det_inv * adj[r][c]) % 26 for c in range(n)] for r in range(n)]

def matrix_mult_mod26(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            total = sum(A[i][k] * B[k][j] for k in range(cols_A))
            result[i][j] = total % 26
    return result

def encrypt_hill(plaintext, key_matrix):
    n = len(key_matrix)
    det = matrix_det(key_matrix) % 26
    if gcd(det, 26) != 1:
        raise ValueError(f"Kunci tidak valid! Determinan mod 26 adalah {det} (harus ganjil dan selain 13).")
        
    prepared_pt = prepare_text(plaintext, n)
    ciphertext = ""
    
    for i in range(0, len(prepared_pt), n):
        mp = [[char_to_num(char)] for char in prepared_pt[i:i+n]]
        mc = matrix_mult_mod26(key_matrix, mp)
        ciphertext += ''.join(num_to_char(mc[r][0]) for r in range(n))
        
    return ciphertext

def decrypt_hill(ciphertext, key_matrix):
    n = len(key_matrix)
    inv_key = matrix_inverse_mod26(key_matrix)
    prepared_ct = prepare_text(ciphertext, n)
    plaintext = ""
    
    for i in range(0, len(prepared_ct), n):
        mc = [[char_to_num(char)] for char in prepared_ct[i:i+n]]
        mp = matrix_mult_mod26(inv_key, mc)
        plaintext += ''.join(num_to_char(mp[r][0]) for r in range(n))
        
    return plaintext

def find_key_hill(plaintext, ciphertext, key_size):
    pt_nums = [char_to_num(c) for c in prepare_text(plaintext, key_size)]
    ct_nums = [char_to_num(c) for c in prepare_text(ciphertext, key_size)]
    
    num_blocks = len(pt_nums) // key_size
    if num_blocks < key_size:
        raise ValueError(f"Dibutuhkan minimal {key_size * key_size} karakter untuk mencari kunci {key_size}x{key_size}.")
    
    p_blocks = [[pt_nums[i * key_size + row] for row in range(key_size)] for i in range(num_blocks)]
    c_blocks = [[ct_nums[i * key_size + row] for row in range(key_size)] for i in range(num_blocks)]
    
    for indices in itertools.combinations(range(num_blocks), key_size):
        P_mat = [[p_blocks[idx][row] for idx in indices] for row in range(key_size)]
        C_mat = [[c_blocks[idx][row] for idx in indices] for row in range(key_size)]
        
        det_P = matrix_det(P_mat) % 26
        if gcd(det_P, 26) == 1:
            P_inv = matrix_inverse_mod26(P_mat)
            return matrix_mult_mod26(C_mat, P_inv)
            
    raise ValueError("Gagal! Tidak ada kombinasi blok plaintext yang matriksnya memiliki invers mod 26.")

# INPUT USER
def input_matrix(n):
    print(f"Masukkan elemen matriks kunci ({n}x{n}) per baris (pisahkan dengan spasi):")
    matrix = []
    for i in range(n):
        while True:
            try:
                row = list(map(int, input(f"Baris {i+1}: ").strip().split()))
                if len(row) != n:
                    print(f"Error: Harus memasukkan tepat {n} angka!")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Error: Harap masukkan angka yang valid!")
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print("  [ " + " ".join(f"{val:2d}" for val in row) + " ]")

def main():
    while True:
        print("\n" + "="*35)
        print("    PROGRAM HILL CIPHER")
        print("="*35)
        print("1. Enkripsi Teks")
        print("2. Dekripsi Teks")
        print("3. Cari Matriks Kunci")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ").strip()
        
        if pilihan == '1':
            print("\n--- ENKRIPSI ---")
            n = int(input("Masukkan ordo matriks kunci (2 untuk 2x2, 3 untuk 3x3): "))
            key_matrix = input_matrix(n)
            pt = input("Masukkan Plaintext: ")
            
            try:
                cipher = encrypt_hill(pt, key_matrix)
                print(f"\nHasil Enkripsi (Ciphertext): {cipher}")
            except Exception as e:
                print(f"\n[Gagal Enkripsi] {e}")

        elif pilihan == '2':
            print("\n--- DEKRIPSI ---")
            n = int(input("Masukkan ordo matriks kunci (2 untuk 2x2, 3 untuk 3x3): "))
            key_matrix = input_matrix(n)
            ct = input("Masukkan Ciphertext: ")
            
            try:
                plain = decrypt_hill(ct, key_matrix)
                print(f"\nHasil Dekripsi (Plaintext): {plain}")
            except Exception as e:
                print(f"\n[Gagal Dekripsi] {e}")

        elif pilihan == '3':
            print("\n--- CARI MATRIKS KUNCI ---")
            n = int(input("Masukkan ordo perkiraan kunci (2 untuk 2x2, 3 untuk 3x3): "))
            pt = input("Masukkan Plaintext sampel: ")
            ct = input("Masukkan Ciphertext sampel: ")
            
            try:
                key = find_key_hill(pt, ct, n)
                print(f"\nMatriks Kunci K ({n}x{n}) yang ditemukan:")
                print_matrix(key)
            except Exception as e:
                print(f"\n[Gagal Mencari Kunci] {e}")

        elif pilihan == '4':
            print("\nTerima kasih, program selesai!")
            break
        else:
            print("\nPilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()