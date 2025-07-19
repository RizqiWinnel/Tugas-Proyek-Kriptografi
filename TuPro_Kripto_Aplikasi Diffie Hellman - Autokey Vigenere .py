#PROGRAM APLIKASI KRIPTOGRAFI DIFFIE HELLMAN - AUTOKEY VIGENERE CIPHER

from customtkinter import *
import math

#--- Form ---
root = CTk()
root.title('Diffie Hellman - Autokey Vigenere Cipher')
root.geometry('1000x500')
set_appearance_mode("dark")
set_default_color_theme("blue")

# --- Fungsi Cek Prima ---
def cek_prima(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True

# --- Fungsi Generator Bilangan Prima ---
def generate_prima(awal, jumlah):
    prima = []
    n = awal
    while len(prima) < jumlah:
        if cek_prima(n):
            prima.append(n)
        n += 1
    return prima

# --- Fungsi Proses Generator Bilangan Prima ---
def proses_generator_prima(entry_inputawal, entry_jumlah, textbox_hasil):
    awal = int(entry_inputawal.get())
    jumlah = int(entry_jumlah.get())
    if jumlah < 1:
        textbox_hasil.delete("0.0", END)
        textbox_hasil.insert(END, 'Jumlah harus lebih dari 0.')
    else:
        prima = generate_prima(awal, jumlah)
        hasil = f"Diperoleh {len(prima)} bilangan prima mulai dari {awal}:\n\n"
        for i in range(len(prima)):
            hasil += f"{prima[i]}\n"
        textbox_hasil.delete("0.0", END)
        textbox_hasil.insert("0.0", hasil)

# --- Fungsi Totient ---
def totient(n):
    hasil = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            hasil -= hasil // i
        i += 1
    if n > 1:
        hasil -= hasil // n
    return hasil

# --- Fungsi Faktor Prima ---
def faktor_prima(n):
    faktorprima = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            count = 0
            while n % i == 0:
                n //= i
                count += 1
            faktorprima.append((i, count))
        i += 1
    if n > 1:
        faktorprima.append((n, 1))
    return faktorprima

# --- Fungsi Order ---
def order(a, n):
    if math.gcd(a, n) != 1:
        return 0
    hasil = totient(n)
    faktorprima = faktor_prima(hasil)
    for p, e in faktorprima:
        while hasil % p == 0 and pow(a, hasil // p, n) == 1:
            hasil //= p
    return hasil

# --- Fungsi Akar Primitif ---
def punya_akar_primitif(n):
    if n <= 0:
        return False
    if n == 1 or n == 2 or n == 4:
        return True
    if n % 4 == 0:
        return False
    faktor = faktor_prima(n)
    if len(faktor) == 1 and faktor[0][0] > 2:
        return True
    if len(faktor) == 2 and faktor[0] == (2, 1):
        return True
    return False

# --- Fungsi Hitung Semua Akar Primitif ---
def hitung_akar_primitif(n: int) -> list:
    if not punya_akar_primitif(n):
        return []
    phi = totient(n)
    akarprimitif = []
    for a in range(1, n):
        if math.gcd(a, n) == 1 and order(a, n) == phi:
            akarprimitif.append(a)
    return akarprimitif

# --- Fungsi Proses hitung Akar Primitif ---
def proses_hitung_akar_primitif(entry_inputbilangan, textbox_hasil):
    p = int(entry_inputbilangan.get())
    if p < 2:
        textbox_hasil.delete("0.0", END)
        textbox_hasil.insert(END, 'Bilangan harus lebih dari 1.')
    else:
        akarprimitif = hitung_akar_primitif(p)
        hasil = f"Diperoleh {len(akarprimitif)} akar primitif untuk p = {p}:\n\n"
        for i in range(len(akarprimitif)):
            hasil += f"{akarprimitif[i]}\n"
        textbox_hasil.delete("0.0", END)
        textbox_hasil.insert("0.0", hasil)

# --- Fungsi Hitung Kunci Publik ---
def hitung_kunci_publik(KunciPrivat, g, n):
    KunciPublik = pow(g, KunciPrivat, n)
    return KunciPublik

# --- Fungsi Hitung Kunci Simetri ---
def hitung_kunci_simetri(KunciPublik, KunciPrivat, n):
    K = pow(KunciPublik, KunciPrivat, n)
    KunciRahasia = K
    return KunciRahasia

# --- Fungsi Proses Hitung Kunci Publik ---
def proses_hitung_kunci_publik(entry_inputkunciprivat, entry_inputg, entry_inputn, entry_outputkuncipublik):
    kunciprivat = int(entry_inputkunciprivat.get())
    g = int(entry_inputg.get())
    n = int(entry_inputn.get())
    if kunciprivat < 1 or g < 1 or n < 1:
        entry_outputkuncipublik.delete(0, END)
        entry_outputkuncipublik.insert(END, 'Kunci privat, g, dan n harus lebih dari 0.')
    else:
        kuncipublik = hitung_kunci_publik(kunciprivat, g, n)
        entry_outputkuncipublik.delete(0, END)
        entry_outputkuncipublik.insert(END, kuncipublik)

# --- Fungsi Proses Hitung Kunci Simetri ---
def proses_hitung_kunci_simetri(entry_inputkuncipublik, entry_inputkunciprivat, entry_inputn, entry_outputkuncisimetri):
    kuncipublik = int(entry_inputkuncipublik.get())
    kunciprivat = int(entry_inputkunciprivat.get())
    n = int(entry_inputn.get())
    if kuncipublik < 1 or kunciprivat < 1 or n < 1:
        entry_outputkuncisimetri.delete(0, END)
        entry_outputkuncisimetri.insert(END, 'Kunci publik, kunci privat, dan n harus lebih dari 0.')
    else:
        kuncisimetri = hitung_kunci_simetri(kuncipublik, kunciprivat, n)
        entry_outputkuncisimetri.delete(0, END)
        entry_outputkuncisimetri.insert(END, kuncisimetri)

# --- Fungsi Konversi Kunci Simetri ---
def konversi_kunci_simetri(kuncisimetri):
    kunci_str = str(kuncisimetri)
    blok = []
    for i in range(len(kunci_str)):
        if i == len(kunci_str) - 1:
            blok.append(int(kunci_str[i]))
        else:
            blok.append(int(kunci_str[i:i+2]))
    hasil = ''
    for n in blok:
        hasil = hasil + chr(n % 26 + 97)
    return hasil

# --- Fungsi Proses Konversi Kunci Simetri ---
def proses_konversi_kunci_simetri(entry_inputkuncisimetri, entry_outputkuncikonversi):
    kuncisimetri = int(entry_inputkuncisimetri.get())
    kunciAutokeyVigenere = konversi_kunci_simetri(kuncisimetri)
    entry_outputkuncikonversi.delete(0, END)
    entry_outputkuncikonversi.insert(END, kunciAutokeyVigenere)

# --- Fungsi Pembangkit Kunci Enkripsi ---
def pembangkit_kunci_enkripsi(plainteks, kunciAutokeyVigenere):
    kunci = kunciAutokeyVigenere
    for i in range(len(plainteks) - len(kunciAutokeyVigenere)):
        kunci = kunci + plainteks[i]
    return kunci

# --- Fungsi Pembangkit Kunci Dekripsi ---
def pembangkit_kunci_dekripsi(cipherteks, kunciAutokeyVigenere):
    kunci = kunciAutokeyVigenere
    for i in range(len(cipherteks) - len(kunciAutokeyVigenere)):
        kunci = kunci + chr(((ord(cipherteks[i]) - 97) - (ord(kunci[i]) - 97)) % 26 + 97)
    return kunci

# --- Fungsi Enkripsi Autokey Vigenere ---
def enkripsi_AutokeyVigenere(entry_plainteks, entry_kunciAutokeyVigenere, entry_cipherteks):
    plainteks = entry_plainteks.get()
    kunciAutokeyVigenere = entry_kunciAutokeyVigenere.get()
    kunci = pembangkit_kunci_enkripsi(plainteks, kunciAutokeyVigenere)
    cipherteks = ''
    for i in range(len(plainteks)):
        cipherteks = cipherteks + chr(((ord(plainteks[i]) - 97) + (ord(kunci[i]) - 97)) % 26 + 97)
    entry_cipherteks.delete(0, END)
    entry_cipherteks.insert(END, cipherteks)
    return cipherteks

def dekripsi_AutokeyVigenere(entry_cipherteks, entry_kunciAutokeyVigenere, entry_plainteks):
    cipherteks = entry_cipherteks.get()
    kunciAutokeyVigenere = entry_kunciAutokeyVigenere.get()
    kunci = pembangkit_kunci_dekripsi(cipherteks, kunciAutokeyVigenere)
    plainteks = ''
    for i in range(len(cipherteks)):
        plainteks = plainteks + chr(((ord(cipherteks[i]) - 97) - (ord(kunci[i]) - 97)) % 26 + 97)
    entry_plainteks.delete(0, END)
    entry_plainteks.insert(END, plainteks)
    return plainteks

# --- Frame Utama ---
frame_utama = CTkFrame(master = root, width = 800, height = 500)
frame_utama.propagate(False)

# --- Laman Home ---
def laman_home():
    frame_home = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_home.propagate(False)
    
    # --- Widget Home ---
    label_judul = CTkLabel(master = frame_home, text = 'Kriptografi Diffie Hellman - Autokey Vigenere Cipher', font = ('Montserrat', 18, 'bold'))
    label_judul.place(x=180, y=50)
    label_keterangan = CTkLabel(master = frame_home, text = 'Terdapat 4 jenis program:', font = ('Montserrat', 14, 'bold'))
    label_keterangan.place(x=140, y=100)
    label_bilanganprima = CTkLabel(master = frame_home, text = '1. Generator Bilangan Prima', font = ('Montserrat', 12))
    label_bilanganprima.place(x=140, y=130)
    label_akarprimitif = CTkLabel(master = frame_home, text = '2. Generator Akar Primitif', font = ('Montserrat', 12))
    label_akarprimitif.place(x=140, y=160)
    label_pertukarankunci = CTkLabel(master = frame_home, text = '3. Pertukaran Kunci Diffie Hellman', font = ('Montserrat', 12))
    label_pertukarankunci.place(x=140, y=190)
    label_AutokeyVigenere = CTkLabel(master = frame_home, text = '4. Enkripsi dan Dekripsi menggunakan Autokey Vigenere Cipher', font = ('Montserrat', 12))
    label_AutokeyVigenere.place(x=140, y=220)
    label_penutup = CTkLabel(master = frame_home, text = 'Silakan pilih salah satu program pada tombol di samping.', font = ('Montserrat', 12))
    label_penutup.place(x=140, y=260)

    frame_home.pack(side = 'left')

# --- Laman Bilangan Prima ---
def laman_bilanganprima():
    frame_bilanganprima = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_bilanganprima.propagate(False)
    
    # --- Widget Bilangan Prima ---
    label_judulbilanganprima = CTkLabel(master = frame_bilanganprima, text = 'Generator Bilangan Prima', font = ('Montserrat', 18, 'bold'))
    label_judulbilanganprima.place(x=270, y=30)
    label_inputawal = CTkLabel(master = frame_bilanganprima, text = 'Masukkan nilai awal:', font = ('Montserrat', 12))
    label_inputawal.place(x=60, y=100)
    entry_inputawal = CTkEntry(master = frame_bilanganprima, width = 200)
    entry_inputawal.place(x=60, y=130)
    label_inputbanyak = CTkLabel(master = frame_bilanganprima, text = 'Masukkan banyak bilangan:', font = ('Montserrat', 12))
    label_inputbanyak.place(x=60, y=160)
    entry_inputbanyak = CTkEntry(master = frame_bilanganprima, width = 200)
    entry_inputbanyak.place(x=60, y=190)
    label_hasil = CTkLabel(master = frame_bilanganprima, text = 'Hasil:', font = ('Montserrat', 12))
    label_hasil.place(x=300, y=100)
    textbox_hasil = CTkTextbox(master = frame_bilanganprima, width=470, height=350, scrollbar_button_color='#333333')
    textbox_hasil.place(x=300, y=130)

    # --- Button Proses ---
    button_proses = CTkButton(master = frame_bilanganprima, text = 'Proses', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command=lambda: proses_generator_prima(entry_inputawal, entry_inputbanyak, textbox_hasil))
    button_proses.place(x = 60, y = 230)

    frame_bilanganprima.pack(side = 'left')

# --- Laman Akar Primitif ---
def laman_akarprimitif():
    frame_akarprimitif = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_akarprimitif.propagate(False)
    
    # --- Widget Akar Primitif ---
    label_judulakarprimitif = CTkLabel(master = frame_akarprimitif, text = 'Generator Akar Primitif', font = ('Montserrat', 18, 'bold'))
    label_judulakarprimitif.place(x=270, y=30)
    label_bilangan = CTkLabel(master = frame_akarprimitif, text = 'Masukkan bilangan:', font = ('Montserrat', 12))
    label_bilangan.place(x=60, y=100)
    entry_inputbilangan = CTkEntry(master = frame_akarprimitif, width = 200)
    entry_inputbilangan.place(x=60, y=130)
    label_hasil = CTkLabel(master = frame_akarprimitif, text = 'Akar Primitif:', font = ('Montserrat', 12))
    label_hasil.place(x=300, y=100)
    textbox_hasil = CTkTextbox(master = frame_akarprimitif, width=470, height=350, scrollbar_button_color='#333333')
    textbox_hasil.place(x=300, y=130)

    # --- Button Proses ---
    button_proses = CTkButton(master = frame_akarprimitif, text = 'Proses', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command=lambda: proses_hitung_akar_primitif(entry_inputbilangan, textbox_hasil))
    button_proses.place(x = 60, y = 170)

    frame_akarprimitif.pack(side = 'left')

# --- Laman Pertukaran Kunci ---
def laman_pertukarankunci():
    frame_pertukarankunci = CTkFrame(master = frame_utama, width = 800, height = 500)
    frame_pertukarankunci.propagate(False)
    
    label_judulpertukarankunci = CTkLabel(master = frame_pertukarankunci, text = 'Pertukaran Kunci Diffie Hellman', font = ('Montserrat', 18, 'bold'))
    label_judulpertukarankunci.place(x=250, y=30)
    tabview = CTkTabview(master = frame_pertukarankunci, width = 750, height = 400)
    tabview.place(x = 20, y = 70)
    tabview.add('Peran Alice')
    tabview.add('Peran Bob')
   
    # --- Widget Tab Peran Alice ---
    label_peranAlice = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Peran Alice', font = ('Montserrat', 14, 'bold'))
    label_peranAlice.place(x=20, y = 20)
    label_inputg_alice = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Input g yang telah disepakati bersama Bob:', font = ('Montserrat', 12))
    label_inputg_alice.place(x=20, y=50)
    label_inputn_alice = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Input n yang telah disepakati bersama Bob:', font = ('Montserrat', 12))
    label_inputn_alice.place(x = 400, y = 50)
    entry_g_alice = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_g_alice.place(x = 20, y = 80)
    entry_n_alice = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_n_alice.place(x = 400, y = 80)
    label_inputx = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Input nilai x, rahasiakan nilai x:', font = ('Montserrat', 12))
    label_inputx.place(x = 20, y = 110)
    entry_inputx = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_inputx.place(x = 20, y = 140)
    label_inputY = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Input nilai Y dari Bob:', font = ('Montserrat', 12))
    label_inputY.place(x = 400, y = 110)
    entry_inputY = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_inputY.place(x = 400, y = 140)
    label_kuncisimetri_alice = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Kunci yang dibentuk:', font = ('Montserrat', 12))
    label_kuncisimetri_alice.place(x=400, y=220)
    entry_kuncisimetri_alice = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_kuncisimetri_alice.place(x = 400, y = 250)
    label_outputX = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Output nilai X untuk Bob:', font = ('Montserrat', 12))
    label_outputX.place(x = 20, y = 220)
    entry_outputX = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_outputX.place(x = 20, y = 250)
    label_kunciautokeyvigenere_alice = CTkLabel(master = tabview.tab('Peran Alice'), text = 'Kunci Autokey Vigenere:', font = ('Montserrat', 12))
    label_kunciautokeyvigenere_alice.place(x = 400, y = 280)
    entry_kunciautokeyvigenere_alice = CTkEntry(master = tabview.tab('Peran Alice'), width = 325)
    entry_kunciautokeyvigenere_alice.place(x = 400, y = 310)
    
    # --- Button Alice ---
    button_hitungX = CTkButton(master = tabview.tab('Peran Alice'), text = 'Hitung X', font = ('Montserrat', 12), width = 325, height = 30, corner_radius= 10, command = lambda: proses_hitung_kunci_publik(entry_inputx, entry_g_alice, entry_n_alice, entry_outputX))
    button_hitungX.place(x = 20, y = 180)
    button_hitungkuncisimetri_alice = CTkButton(master = tabview.tab('Peran Alice'), text = 'Hitung Kunci', font = ('Montserrat', 12), width = 325, height = 30, corner_radius= 10, command=lambda: [proses_hitung_kunci_simetri(entry_inputY, entry_inputx, entry_n_alice, entry_kuncisimetri_alice), proses_konversi_kunci_simetri(entry_kuncisimetri_alice, entry_kunciautokeyvigenere_alice)])
    button_hitungkuncisimetri_alice.place(x = 400, y = 180)

    # --- Widget Tab Peran Bob ---
    label_peranBob = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Peran Bob', font = ('Montserrat', 14, 'bold'))
    label_peranBob.place(x=20, y = 20)
    label_inputg_bob = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Input g yang telah disepakati bersama Alice:', font = ('Montserrat', 12))
    label_inputg_bob.place(x=20, y=50)
    label_inputn_bob = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Input n yang telah disepakati bersama Alice:', font = ('Montserrat', 12))
    label_inputn_bob.place(x = 400, y = 50)
    entry_inputg_bob = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_inputg_bob.place(x = 20, y = 80)
    entry_inputn_bob = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_inputn_bob.place(x = 400, y = 80)
    label_inputy = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Input nilai y, rahasiakan nilai y:', font = ('Montserrat', 12))
    label_inputy.place(x = 20, y = 110)
    entry_inputy = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_inputy.place(x = 20, y = 140)
    label_inputX = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Input nilai X dari Alice:', font = ('Montserrat', 12))
    label_inputX.place(x = 400, y = 110)
    entry_inputX = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_inputX.place(x = 400, y = 140)
    label_kuncisimetri_bob = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Kunci yang dibentuk:', font = ('Montserrat', 12))
    label_kuncisimetri_bob.place(x=400, y=220)
    label_outputY = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Output nilai Y untuk Alice:', font = ('Montserrat', 12))
    label_outputY.place(x = 20, y = 220)
    entry_outputY = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_outputY.place(x = 20, y = 250)
    entry_kuncisimetri_bob = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_kuncisimetri_bob.place(x = 400, y = 250)
    label_kunciautokeyvigenere_bob = CTkLabel(master = tabview.tab('Peran Bob'), text = 'Kunci Autokey Vigenere:', font = ('Montserrat', 12))
    label_kunciautokeyvigenere_bob.place(x = 400, y = 280)
    entry_kunciautokeyvigenere_bob = CTkEntry(master = tabview.tab('Peran Bob'), width = 325)
    entry_kunciautokeyvigenere_bob.place(x = 400, y = 310)

    # --- Button Bob ---
    button_hitungY = CTkButton(master = tabview.tab('Peran Bob'), text = 'Hitung Y', font = ('Montserrat', 12), width = 325, height = 30, corner_radius= 10, command=lambda: proses_hitung_kunci_publik(entry_inputy, entry_inputg_bob, entry_inputn_bob, entry_outputY))
    button_hitungY.place(x = 20, y = 180)
    button_hitungkuncisimetri_bob = CTkButton(master = tabview.tab('Peran Bob'), text = 'Hitung Kunci', font = ('Montserrat', 12), width = 325, height = 30, corner_radius= 10, command=lambda: [proses_hitung_kunci_simetri(entry_inputX, entry_inputy, entry_inputn_bob, entry_kuncisimetri_bob), proses_konversi_kunci_simetri(entry_kuncisimetri_bob, entry_kunciautokeyvigenere_bob)])
    button_hitungkuncisimetri_bob.place(x = 400, y = 180)

    frame_pertukarankunci.pack(side = 'left')

# --- Laman Autokey Vigenere ---
def laman_AutokeyVigenere():
    frame_AutokeyVigenere = CTkFrame(master = frame_utama, width = 800, height = 500)
    frame_AutokeyVigenere.propagate(False)
    
    label_JudulAutokeyVigenere = CTkLabel(master = frame_AutokeyVigenere, text = 'Autokey Vigenere Cipher', font = ('Montserrat', 18, 'bold'))
    label_JudulAutokeyVigenere.place(x=280, y=30)
    tabview = CTkTabview(master = frame_AutokeyVigenere, width = 750, height = 400)
    tabview.place(x = 20, y = 70)
    tabview.add('Enkripsi')
    tabview.add('Dekripsi')

    # --- Widget Tab Enkripsi ---
    label_enkripsi = CTkLabel(master = tabview.tab('Enkripsi'), text = 'Enkripsi Autokey Vigenere', font = ('Montserrat', 14, 'bold'))
    label_enkripsi.place(x=20, y=20)
    label_inputplainteks = CTkLabel(master = tabview.tab('Enkripsi'), text = 'Input plainteks yang ingin dienkripsi:', font = ('Montserrat', 12))
    label_inputplainteks.place(x = 20, y = 50)
    entry_inputplainteks = CTkEntry(master = tabview.tab('Enkripsi'), width = 700)
    entry_inputplainteks.place(x = 20, y = 80)
    label_inputkunci_enkripsi = CTkLabel(master = tabview.tab('Enkripsi'), text = 'Input kunci:', font = ('Montserrat', 12))
    label_inputkunci_enkripsi.place(x = 20, y = 110)
    entry_inputkunci_enkripsi = CTkEntry(master = tabview.tab('Enkripsi'), width = 325)
    entry_inputkunci_enkripsi.place(x = 20, y = 140)
    label_outputcipherteks = CTkLabel(master = tabview.tab('Enkripsi'), text = 'Output cipherteks:', font = ('Montserrat', 12))
    label_outputcipherteks.place(x = 20, y = 220)
    entry_outputcipherteks = CTkEntry(master = tabview.tab('Enkripsi'), width = 700)
    entry_outputcipherteks.place(x = 20, y = 250)

    # --- Button Enkripsi ---
    button_enkripsi = CTkButton(master = tabview.tab('Enkripsi'), text = 'Enkripsi', font = ('Montserrat', 12), width = 200, command=lambda: enkripsi_AutokeyVigenere(entry_inputplainteks, entry_inputkunci_enkripsi, entry_outputcipherteks))
    button_enkripsi.place(x = 20, y = 180)

    # --- Widget Tab Dekripsi ---
    label_dekripsi = CTkLabel(master = tabview.tab('Dekripsi'), text = 'Dekripsi Autokey Vigenere', font = ('Montserrat', 14, 'bold'))
    label_dekripsi.place(x=20, y=20)
    label_inputcipherteks = CTkLabel(master = tabview.tab('Dekripsi'), text = 'Input cipherteks yang ingin didekripsi:', font = ('Montserrat', 12))
    label_inputcipherteks.place(x = 20, y = 50)
    entry_inputcipherteks = CTkEntry(master = tabview.tab('Dekripsi'), width = 700)
    entry_inputcipherteks.place(x = 20, y = 80)
    label_inputkunci_dekripsi = CTkLabel(master = tabview.tab('Dekripsi'), text = 'Input kunci:', font = ('Montserrat', 12))
    label_inputkunci_dekripsi.place(x = 20, y = 110)
    entry_inputkunci_dekripsi = CTkEntry(master = tabview.tab('Dekripsi'), width = 325)
    entry_inputkunci_dekripsi.place(x = 20, y = 140)
    label_outputplainteks = CTkLabel(master = tabview.tab('Dekripsi'), text = 'Output plainteks:', font = ('Montserrat', 12))
    label_outputplainteks.place(x = 20, y = 220)
    entry_outputplainteks = CTkEntry(master = tabview.tab('Dekripsi'), width = 700)
    entry_outputplainteks.place(x = 20, y = 250)

    # --- Button Dekripsi ---
    button_dekripsi = CTkButton(master = tabview.tab('Dekripsi'), text = 'Dekripsi', font = ('Montserrat', 12), width = 200, command=lambda: dekripsi_AutokeyVigenere(entry_inputcipherteks, entry_inputkunci_dekripsi, entry_outputplainteks))
    button_dekripsi.place(x = 20, y = 180)

    frame_AutokeyVigenere.pack(side = 'left')

# --- Laman Help ---
def laman_help():
    frame_help = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_help.propagate(False)
    
    # --- Widget Help ---
    label_judulhelp = CTkLabel(master = frame_help, text = 'Panduan Penggunaan Aplikasi', font = ('Montserrat', 18, 'bold'))
    label_judulhelp.place(x=270, y=30)
    tabview = CTkTabview(master = frame_help, width = 750, height = 400)
    tabview.place(x = 20, y = 70)
    tabview.add('Generator Prima')
    tabview.add('Akar Primitif')
    tabview.add('Diffie Hellman')
    tabview.add('Autokey Vigenere')
    
    # --- Panduan Generator Bilangan Prima ---
    panduan_prima = """Program Generator Bilangan Prima membantu untuk menghasilkan bilangan prima.

Cara Penggunaan:
1. Masukkan nilai awal pencarian bilangan prima pada kolom "Masukkan nilai awal"
2. Masukkan jumlah bilangan prima yang ingin dihasilkan pada kolom "Masukkan banyak bilangan"
3. Klik tombol "Proses" untuk menghasilkan bilangan prima
4. Hasil akan ditampilkan di panel sebelah kanan

Catatan:
- Nilai awal harus berupa bilangan positif
- Program akan mencari bilangan prima mulai dari nilai awal yang dimasukkan"""

    textbox_prima = CTkTextbox(master = tabview.tab('Generator Prima'), width=700, height=300)
    textbox_prima.insert("0.0", panduan_prima)
    textbox_prima.configure(state="disabled")
    textbox_prima.place(x=20, y=20)
    
    # --- Panduan Generator Akar Primitif ---
    panduan_akarprimitif = """Program Generator Akar Primitif membantu menemukan semua akar primitif dari suatu bilangan.

Cara Penggunaan:
1. Masukkan bilangan yang ingin dicari akar primitifnya pada kolom "Masukkan bilangan"
2. Klik tombol "Proses" untuk mencari akar primitif
3. Hasil akan ditampilkan di panel sebelah kanan

Catatan:
- Bilangan yang dimasukkan harus positif
- Tidak semua bilangan memiliki akar primitif"""

    textbox_akarprimitif = CTkTextbox(master = tabview.tab('Akar Primitif'), width=700, height=300)
    textbox_akarprimitif.insert("0.0", panduan_akarprimitif)
    textbox_akarprimitif.configure(state="disabled")
    textbox_akarprimitif.place(x=20, y=20)
    
    # --- Panduan Pertukaran Kunci Diffie Hellman ---
    panduan_diffiehellman = """Program Pertukaran Kunci Diffie Hellman memungkinkan dua pihak (Alice dan Bob) untuk membuat kunci rahasia bersama.

Cara Penggunaan:
1. Alice dan Bob harus menyepakati dan menggunakan nilai g dan n yang sama
   - n adalah suatu bilangan prima
   - g adalah akar primitif dari n

2. Pada tab "Peran Alice":
   - Masukkan nilai g dan n yang telah disepakati
   - Pilih nilai x (kunci privat Alice) dan rahasiakan
   - Klik "Hitung X" untuk mendapatkan nilai X (kunci publik Alice)
   - Kirim nilai X ke Bob
   - Masukkan nilai Y yang diterima dari Bob
   - Klik "Hitung Kunci" untuk mendapatkan kunci rahasia

3. Pada tab "Peran Bob":
   - Masukkan nilai g dan n yang telah disepakati
   - Pilih nilai y (kunci privat Bob) dan rahasiakan
   - Klik "Hitung Y" untuk mendapatkan nilai Y (kunci publik Bob)
   - Kirim nilai Y ke Alice
   - Masukkan nilai X yang diterima dari Alice
   - Klik "Hitung Kunci" untuk mendapatkan kunci rahasia

Catatan:
- Kunci privat (x dan y) harus dirahasiakan
- Kunci publik (X dan Y) aman untuk dikirim
- Jika prosesnya benar, Alice dan Bob akan mendapatkan kunci rahasia yang sama"""

    textbox_diffiehellman = CTkTextbox(master = tabview.tab('Diffie Hellman'), width=700, height=300)
    textbox_diffiehellman.insert("0.0", panduan_diffiehellman)
    textbox_diffiehellman.configure(state="disabled")
    textbox_diffiehellman.place(x=20, y=20)
    
    # --- Panduan Autokey Vigenere Cipher ---
    panduan_autokeyvigenere = """Program Autokey Vigenere Cipher digunakan untuk mengenkripsi dan mendekripsi pesan menggunakan kunci dari hasil pertukaran Diffie Hellman.

Cara Penggunaan Enkripsi:
1. Pada tab "Enkripsi":
   - Masukkan plainteks (pesan asli) yang ingin dienkripsi
   - Masukkan kunci (hasil konversi dari pertukaran Diffie Hellman)
   - Klik tombol "Enkripsi"
   - Hasil enkripsi (cipherteks) akan muncul di bagian output

Cara Penggunaan Dekripsi:
1. Pada tab "Dekripsi":
   - Masukkan cipherteks (pesan terenkripsi) yang ingin didekripsi
   - Masukkan kunci yang sama dengan yang digunakan untuk enkripsi
   - Klik tombol "Dekripsi"
   - Hasil dekripsi (plainteks) akan muncul di bagian output

Catatan:
- Plainteks hanya boleh berisi huruf kecil (a-z)
- Spasi dan karakter khusus tidak diperbolehkan
- Kunci harus sama untuk enkripsi dan dekripsi
- Metode Autokey Vigenere menggunakan plainteks sebagai bagian dari kunci"""

    textbox_autokeyvigenere = CTkTextbox(master = tabview.tab('Autokey Vigenere'), width=700, height=300)
    textbox_autokeyvigenere .insert("0.0", panduan_autokeyvigenere)
    textbox_autokeyvigenere .configure(state="disabled")
    textbox_autokeyvigenere .place(x=20, y=20)

    frame_help.pack(side = 'left')

# --- Laman About ---
def laman_about():
    frame_about = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_about.propagate(False)
    
    # --- Widget About ---
    label_judulabout = CTkLabel(master = frame_about, text = 'Tentang Aplikasi', font = ('Montserrat', 18, 'bold'))
    label_judulabout.place(x=330, y=30)
    frame_info = CTkFrame(master = frame_about, width = 700, height = 400)
    frame_info.place(x = 50, y = 70)
    label_nama_aplikasi = CTkLabel(master = frame_info, text = 'Aplikasi Kriptografi\nDiffie Hellman - Autokey Vigenere Cipher', font = ('Montserrat', 16, 'bold'))
    label_nama_aplikasi.place(x=190, y=20)
    label_versi = CTkLabel(master = frame_info, text = 'Versi 1.0.0', font = ('Montserrat', 12))
    label_versi.place(x=315, y=70)
    
    # Deskripsi Aplikasi
    tentang_deskripsi = """Aplikasi ini merupakan implementasi dari algoritma pertukaran kunci Diffie-Hellman 
yang dikombinasikan dengan metode enkripsi Autokey Vigenere Cipher. Aplikasi ini 
bertujuan untuk memfasilitasi proses pertukaran kunci yang aman antara dua pihak 
dan menggunakan kunci tersebut untuk enkripsi pesan menggunakan Autokey Vigenere Cipher.

Fitur Utama:
• Generator Bilangan Prima
• Generator Akar Primitif
• Pertukaran Kunci Diffie-Hellman
• Enkripsi dan Dekripsi menggunakan Autokey Vigenere Cipher"""

    textbox_deskripsi = CTkTextbox(master = frame_info, width=600, height=120)
    textbox_deskripsi.insert("0.0", tentang_deskripsi)
    textbox_deskripsi.configure(state="disabled")
    textbox_deskripsi.place(x=50, y=100)
    
    label_pengembang = CTkLabel(master = frame_info, text = 'Dikembangkan oleh:', font = ('Montserrat', 14, 'bold'))
    label_pengembang.place(x=50, y=240)
    tentang_pengembang = """Fahmi Ismail Ramantoko                 (2205676)
Muhammad Rizqi Winnel Adnin      (2209397)
Muhammad Thoriq Atallah              (2202991)
Shafira Mayora Handriyudha           (2202576)"""

    textbox_pengembang = CTkTextbox(master = frame_info, width=600, height=80)
    textbox_pengembang.insert("0.0", tentang_pengembang)
    textbox_pengembang.configure(state="disabled")
    textbox_pengembang.place(x=50, y=270)
    
    frame_about.pack(side = 'left')

# --- Fungsi sembunyikan frame ---
def sembunyikan_frame():
    for frame in frame_utama.winfo_children():
        frame.destroy()

# --- Fungsi munculkan frame ---
def munculkan(laman):
    sembunyikan_frame()
    laman()

# --- frame pilihan program ---
frame_pilihan = CTkFrame(master = root, width = 200, height = 500, fg_color="#333333")
frame_pilihan.propagate(False)

# --- Pilihan Program ---
labelPilihanProgram = CTkLabel(master = frame_pilihan, text = 'Pilihan Program', font = ('Montserrat', 14, 'bold'))
labelPilihanProgram.place(x = 45, y = 5)
button_home = CTkButton(master = frame_pilihan, text = 'Home', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_home))
button_home.place(x = 20, y = 70)
button_bilanganprima = CTkButton(master = frame_pilihan, text = 'Bilangan Prima', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_bilanganprima))
button_bilanganprima.place(x = 20, y = 120)
button_akarprimitif = CTkButton(master = frame_pilihan, text = 'Akar Primitif', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_akarprimitif))
button_akarprimitif.place(x = 20, y = 170)
button_pembangkitkunci = CTkButton(master = frame_pilihan, text = 'Pertukaran Kunci', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_pertukarankunci))
button_pembangkitkunci.place(x = 20, y = 220)
button_AutokeyVigenere = CTkButton(master = frame_pilihan, text = 'Autokey Vigenere', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_AutokeyVigenere))
button_AutokeyVigenere.place(x = 20, y = 270)
button_help = CTkButton(master = frame_pilihan, text = 'Help', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_help))
button_help.place(x = 20, y = 320)
button_about = CTkButton(master = frame_pilihan, text = 'About', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_about))
button_about.place(x = 20, y = 370)

frame_pilihan.pack(side = 'left')
frame_utama.pack(side = 'left')
laman_home()

root.mainloop()