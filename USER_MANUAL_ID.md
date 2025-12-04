# 📖 Panduan Pengguna Macca
## AI English Speaking Coach untuk Pelajar Indonesia

---

## 📑 Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Memulai Aplikasi](#memulai-aplikasi)
3. [Halaman Welcome](#halaman-welcome)
4. [Dashboard](#dashboard)
5. [Live Conversation](#live-conversation)
6. [Guided Lessons](#guided-lessons)
7. [Pronunciation Coach](#pronunciation-coach)
8. [Profile & Settings](#profile--settings)
9. [Tips Penggunaan](#tips-penggunaan)

---

## 🎯 Pengenalan

**Macca** adalah aplikasi AI coach untuk melatih kemampuan berbicara bahasa Inggris, khusus dirancang untuk pelajar Indonesia. Aplikasi ini fokus pada:

- ✅ **Latihan berbicara** dengan feedback real-time
- ✅ **Koreksi grammar** dan saran vocabulary
- ✅ **Analisis pronunciation** untuk suara-suara yang sulit
- ✅ **Penjelasan bilingual** (Indonesia & Inggris)
- ✅ **Pembelajaran terstruktur** dengan guided lessons

---

## 🚀 Memulai Aplikasi

### Langkah 1: Jalankan Backend
```bash
cd backend
./start.sh
```
Backend akan berjalan di: `http://localhost:8000`

### Langkah 2: Jalankan Frontend
```bash
cd frontend
npm start
```
Frontend akan berjalan di: `http://localhost:3000`

### Langkah 3: Buka Browser
Buka browser dan akses: `http://localhost:3000`

---

## 🏠 Halaman Welcome

![Welcome Page]

### Apa yang ada di halaman ini?

**Elemen Utama:**
1. **Logo Macca** - Nama aplikasi dengan gradient cyan-blue
2. **Tagline** - "AI English Speaking Coach" dan "Untuk pelajar Indonesia"
3. **Tombol "Get Started"** - Tombol besar untuk memulai
4. **4 Fitur Utama:**
   - 💬 **Live Conversation** - Latihan percakapan bebas
   - 📚 **Guided Lessons** - Pembelajaran terstruktur
   - 🎤 **Pronunciation Coach** - Latihan pelafalan
   - 🎯 **Personalized Goals** - Tujuan pembelajaran personal

### Apa yang harus diklik?

**Klik tombol "Get Started" atau "Start Learning Now"** untuk masuk ke Dashboard.

---

## 📊 Dashboard

![Dashboard]

### Apa yang ada di halaman ini?

**1. Header Sambutan**
- Menampilkan nama Anda: "Welcome back, [Nama]! 👋"
- Instruksi: "Choose a learning mode to continue improving your English"

**2. Kartu Statistik (3 kartu horizontal):**
- **Current Level** - Level bahasa Inggris Anda (A1-C2)
- **Learning Goal** - Tujuan belajar (Job interview, Business meetings, dll)
- **Explanation Language** - Bahasa penjelasan (Bahasa Indonesia/English)

**3. Mode Pembelajaran (3 kartu besar):**

#### a. Live Conversation 💬
- **Deskripsi:** Practice free-form conversations with instant feedback
- **Tombol:** "Start"

#### b. Guided Lessons 📚
- **Deskripsi:** Structured lessons for specific scenarios and goals
- **Tombol:** "Start"

#### c. Pronunciation Coach 🎤
- **Deskripsi:** Master difficult English sounds with targeted practice
- **Tombol:** "Start"

### Apa yang harus diklik?

**Pilih salah satu mode pembelajaran:**
- Klik **kartu** atau **tombol "Start"** pada mode yang ingin Anda gunakan
- Untuk pemula, disarankan mulai dari **Live Conversation**

**Navigasi:**
- **Sidebar kiri** - Klik menu untuk pindah halaman:
  - 🏠 Dashboard
  - 💬 Live Conversation
  - 📚 Guided Lessons
  - 🎤 Pronunciation Coach
  - 👤 Profile

---

## 💬 Live Conversation

![Live Conversation]

### Apa yang ada di halaman ini?

**1. Header**
- Judul: "Live Conversation"
- Deskripsi: "Practice natural conversations with real-time feedback"

**2. Learner Context Bar (Info Anda)**
- Menampilkan Level, Goal, dan Explanation Language Anda

**3. Area Chat**
- **Pesan dari Macca** (kiri, warna cyan):
  - Sapaan awal dari AI coach
  - Respons dan feedback dari Macca
- **Pesan Anda** (kanan, warna slate):
  - Pesan yang Anda kirim (text atau audio)

**4. Input Area (bagian bawah)**
- **Text Input** - Kolom untuk mengetik pesan
- **Tombol Microphone (🎤)** - Tombol biru untuk merekam suara
- **Tombol "Send"** - Tombol untuk mengirim pesan text

### Cara Menggunakan:

#### Opsi 1: Mengetik Pesan
1. **Ketik** pesan Anda di kolom input
2. **Klik tombol "Send"** atau tekan Enter
3. **Tunggu** respons dari Macca (akan muncul "Macca is thinking...")
4. **Lihat feedback** yang muncul di bawah respons Macca

#### Opsi 2: Merekam Suara (REKOMENDASI)
1. **Klik tombol Microphone (🎤)** - tombol akan berubah merah dan berkedip
2. **Bicara** dalam bahasa Inggris (browser akan minta izin akses microphone)
3. **Klik lagi** tombol microphone untuk berhenti merekam
4. Audio akan **otomatis dikirim** ke Macca
5. **Tunggu** respons dan feedback

### Feedback yang Anda Terima:

Setelah setiap percakapan, Macca akan memberikan:

**📝 Grammar Corrections**
- Kesalahan grammar yang Anda buat
- Penjelasan mengapa salah
- Contoh kalimat yang benar

**💡 Vocabulary Suggestions**
- Kata-kata alternatif yang lebih baik
- Sinonim dan penggunaan yang tepat
- Contoh dalam kalimat

**🗣️ Pronunciation Tips**
- Suara-suara yang perlu diperbaiki
- Tips cara melafalkan dengan benar
- Penjelasan dalam bahasa Indonesia/Inggris

### Tips:
- ✅ Gunakan **microphone** untuk latihan speaking yang lebih efektif
- ✅ Jangan takut salah - Macca akan memberikan feedback konstruktif
- ✅ Coba berbicara dengan **natural** seperti percakapan sehari-hari

---

## 📚 Guided Lessons

![Guided Lessons]

### Apa yang ada di halaman ini?

**1. Header**
- Judul: "Guided Lesson"
- Deskripsi: "Follow structured steps to master specific scenarios"

**2. Learner Context Bar**
- Info level dan goal Anda

**3. Lesson Info Card (Kartu dengan gradient cyan-blue)**
- **Judul Lesson** - Contoh: "Job Interview Practice"
- **Subtitle** - Deskripsi singkat lesson
- **Progress Bar** - Menunjukkan kemajuan Anda
- **Step Indicator** - "Step 1 of 5" (contoh)
- **Daftar Steps:**
  - ✓ Step yang sudah selesai (hijau)
  - → Step yang sedang aktif (cyan, bold)
  - ○ Step yang belum dimulai (abu-abu)

**4. Area Conversation**
- Chat dengan Macca untuk menyelesaikan setiap step
- Input area (sama seperti Live Conversation)

### Cara Menggunakan:

1. **Baca instruksi** di Lesson Info Card
2. **Lihat step yang aktif** (ditandai dengan warna cyan)
3. **Ikuti instruksi** dari Macca di chat
4. **Jawab pertanyaan** atau **lakukan task** yang diminta
5. **Terima feedback** setelah setiap respons
6. **Lanjut ke step berikutnya** setelah step selesai (otomatis)

### Struktur Lesson (Contoh: Job Interview):

**Step 1: Warm-up**
- Perkenalan diri
- Ceritakan latar belakang Anda

**Step 2: Experience Discussion**
- Diskusi pengalaman kerja
- Jelaskan skill dan achievement

**Step 3: Behavioral Questions**
- Jawab pertanyaan situasional
- Contoh: "Tell me about a challenge you faced"

**Step 4: Technical Questions**
- Pertanyaan spesifik sesuai bidang
- Jelaskan expertise Anda

**Step 5: Closing**
- Pertanyaan untuk interviewer
- Closing statement yang kuat

### Tips:
- ✅ **Selesaikan semua steps** untuk hasil maksimal
- ✅ **Gunakan microphone** untuk latihan speaking
- ✅ **Perhatikan feedback** di setiap step
- ✅ Progress Anda akan **tersimpan otomatis**

---

## 🎤 Pronunciation Coach

![Pronunciation Coach]

### Apa yang ada di halaman ini?

**Layout 2 Kolom:**

#### Kolom Kiri: Practice Sounds (Daftar Suara)

Menampilkan 5 suara yang sulit untuk orang Indonesia:

1. **TH (voiceless) - /θ/**
   - Badge: "hard" (merah)
   - Contoh: think, thank, three, mouth

2. **TH (voiced) - /ð/**
   - Badge: "hard" (merah)
   - Contoh: this, that, the, mother

3. **R sound - /r/**
   - Badge: "medium" (kuning)
   - Contoh: red, road, berry, correct

4. **V sound - /v/**
   - Badge: "medium" (kuning)
   - Contoh: very, voice, live, have

5. **Short A - /æ/**
   - Badge: "easy" (hijau)
   - Contoh: cat, bat, map, glad

#### Kolom Kanan: Practice Area

**Sebelum memilih suara:**
- Tampilan kosong dengan icon microphone
- Text: "Select a sound from the left to start practicing"

**Setelah memilih suara:**

1. **Practice Card**
   - Judul: "Practice: /θ/ - TH (voiceless)" (contoh)
   - **Example words** (4 kata dalam grid 2x2):
     - Setiap kata ada tombol speaker (🔊) untuk dengar pronunciation
   
2. **Your Turn Section**
   - Input text: "Type a word to practice..."
   - Tombol Microphone besar (🎤)
   - Status: "Recording..." atau "Analyzing..."

3. **Pronunciation Feedback Card** (muncul setelah recording)
   - **Word** - Kata yang Anda ucapkan
   - **Target Sound** - Suara yang dipraktikkan
   - **Status Badge:**
     - 🟢 "excellent" (hijau)
     - 🔵 "good" (biru)
     - 🟡 "needs work" (kuning)
   - **Score Bar** - Progress bar dengan persentase (0-100%)
   - **Tip** - 💡 Tips dalam bahasa Indonesia/Inggris

### Cara Menggunakan:

#### Langkah 1: Pilih Suara
1. **Klik salah satu kartu** di kolom kiri
2. Kartu akan **highlight dengan warna cyan**
3. Kolom kanan akan menampilkan practice area

#### Langkah 2: Dengarkan Contoh
1. **Klik tombol speaker (🔊)** di setiap example word
2. **Dengarkan** pronunciation yang benar
3. **Ulangi** beberapa kali untuk familiar

#### Langkah 3: Praktik
1. **Ketik kata** yang ingin dipraktikkan (atau biarkan kosong untuk kata pertama)
2. **Klik tombol Microphone (🎤)**
3. **Ucapkan kata** dengan jelas
4. **Klik lagi** untuk stop recording
5. **Tunggu** analisis (2-3 detik)

#### Langkah 4: Lihat Feedback
1. **Perhatikan score** Anda (0-100%)
2. **Baca status:**
   - Excellent (80-100%) - Sangat bagus! ✅
   - Good (60-79%) - Bagus, perlu sedikit perbaikan
   - Needs work (<60%) - Perlu latihan lebih banyak
3. **Baca tips** untuk perbaikan
4. **Praktik lagi** sampai score meningkat

### Tips Pronunciation:

**Untuk TH (/θ/ dan /ð/):**
- Letakkan **ujung lidah** di antara gigi atas dan bawah
- Tiup udara keluar (voiceless) atau bergetar (voiced)
- Jangan ganti dengan "T" atau "D"

**Untuk R (/r/):**
- **Jangan** sentuh langit-langit mulut dengan lidah
- Bibir sedikit **maju** dan **bulat**
- Suara keluar dari tenggorokan

**Untuk V (/v/):**
- **Gigi atas** menyentuh **bibir bawah**
- Bergetar saat udara keluar
- Jangan ganti dengan "F" atau "W"

**Untuk Short A (/æ/):**
- Buka mulut **lebih lebar** dari "e"
- Suara di antara "a" dan "e"
- Contoh: "cat" bukan "ket" atau "cat"

### Rekomendasi Latihan:
1. ✅ Mulai dari **easy** (Short A)
2. ✅ Lanjut ke **medium** (R dan V)
3. ✅ Terakhir **hard** (TH sounds)
4. ✅ Praktik **10-15 menit** setiap hari
5. ✅ Fokus pada **1-2 suara** per sesi

---

## 👤 Profile & Settings

![Profile Page]

### Apa yang ada di halaman ini?

**Layout Grid 2x2 (4 kartu):**

#### 1. Personal Information (Kiri Atas)
- **Icon:** 👤 User
- **Fields:**
  - **Name** - Nama Anda
  - **Current Level** - Dropdown: A1, A2, B1, B2, C1, C2
  - **Learning Goal** - Dropdown:
    - Job interview
    - Business meetings
    - Travel
    - Daily conversation
    - Academic study
    - IELTS/TOEFL prep
- **Tombol:**
  - "Edit Profile" - Untuk mengubah data
  - "Save Changes" - Simpan perubahan
  - "Cancel" - Batalkan perubahan

#### 2. Language Settings (Kanan Atas)
- **Icon:** 🌐 Languages
- **Deskripsi:** "Choose your preferred language for explanations and feedback"
- **2 Tombol Besar:**
  - 🇮🇩 **Bahasa Indonesia** - Penjelasan dalam bahasa Indonesia
  - 🇬🇧 **English** - Penjelasan dalam bahasa Inggris
- Tombol yang aktif akan **highlight cyan**

#### 3. Your Progress (Kiri Bawah)
- **Icon:** 🏆 Award
- **Statistik:**
  - **Sessions completed** - Jumlah sesi yang selesai (contoh: 12)
  - **Words practiced** - Jumlah kata yang dipraktikkan (contoh: 48)
  - **Lessons completed** - Jumlah lesson yang selesai (contoh: 3)

#### 4. Current Focus (Kanan Bawah)
- **Icon:** 🎯 Target
- **Info:**
  - **Active Goal** - Tujuan belajar aktif (dengan gradient cyan-blue)
  - **Current Level** - Level saat ini (dengan warna cyan)

### Cara Menggunakan:

#### Mengubah Profile:
1. **Klik "Edit Profile"** di kartu Personal Information
2. **Ubah** Name, Level, atau Goal sesuai kebutuhan
3. **Klik "Save Changes"** untuk menyimpan
4. **Klik "Cancel"** jika ingin membatalkan

#### Mengubah Bahasa Penjelasan:
1. **Klik tombol 🇮🇩 Bahasa Indonesia** - Semua feedback akan dalam bahasa Indonesia
2. **Klik tombol 🇬🇧 English** - Semua feedback akan dalam bahasa Inggris
3. Perubahan **langsung tersimpan** (tidak perlu klik save)

#### Melihat Progress:
- **Lihat statistik** di kartu Your Progress
- **Track kemajuan** Anda dari waktu ke waktu
- **Motivasi** untuk terus belajar!

### Tips:
- ✅ **Update level** Anda setelah merasa ada peningkatan
- ✅ **Ganti goal** sesuai kebutuhan saat ini
- ✅ Gunakan **Bahasa Indonesia** jika masih pemula
- ✅ Ganti ke **English** untuk challenge lebih

---

## 💡 Tips Penggunaan

### Untuk Pemula (A1-A2):

1. **Mulai dari Live Conversation**
   - Latihan percakapan sederhana
   - Jangan takut salah
   - Fokus pada grammar dasar

2. **Gunakan Bahasa Indonesia untuk penjelasan**
   - Lebih mudah memahami feedback
   - Ganti ke English setelah lebih percaya diri

3. **Praktik Pronunciation Coach**
   - Mulai dari suara "easy"
   - 10 menit setiap hari
   - Fokus pada 1 suara per minggu

### Untuk Intermediate (B1-B2):

1. **Kombinasi Live Conversation dan Guided Lessons**
   - Live untuk spontanitas
   - Guided untuk struktur

2. **Challenge diri dengan English explanations**
   - Meningkatkan vocabulary
   - Terbiasa dengan istilah grammar dalam English

3. **Fokus pada Pronunciation yang sulit**
   - TH sounds
   - R vs L
   - V vs W

### Untuk Advanced (C1-C2):

1. **Fokus pada Guided Lessons**
   - Scenario spesifik (job interview, presentation)
   - Vocabulary advanced
   - Idioms dan expressions

2. **Gunakan Live Conversation untuk fluency**
   - Berbicara lebih natural
   - Ekspresikan ide kompleks
   - Debat dan diskusi

3. **Polish pronunciation**
   - Intonation dan stress
   - Connected speech
   - Accent reduction

### Tips Umum:

✅ **Konsisten** - Latihan 15-30 menit setiap hari lebih baik dari 2 jam seminggu sekali

✅ **Gunakan Microphone** - Speaking practice lebih efektif dengan audio

✅ **Baca Feedback** - Jangan skip feedback, itu kunci improvement

✅ **Ulangi** - Praktik kata/kalimat yang salah sampai benar

✅ **Variasi** - Gunakan semua 3 mode pembelajaran

✅ **Track Progress** - Lihat statistik di Profile untuk motivasi

✅ **Jangan Malu** - AI tidak akan menghakimi, ini tempat aman untuk belajar

---

## 🆘 Troubleshooting

### Microphone tidak bekerja:
1. **Izinkan akses microphone** di browser
2. **Cek settings browser** - pastikan microphone tidak diblokir
3. **Test microphone** di aplikasi lain
4. **Restart browser** jika masih tidak bekerja

### Feedback tidak muncul:
1. **Tunggu beberapa detik** - AI membutuhkan waktu untuk proses
2. **Cek koneksi internet** - pastikan stabil
3. **Refresh halaman** jika stuck
4. **Cek backend** - pastikan backend running di `http://localhost:8000`

### Audio tidak terdengar:
1. **Cek volume** device Anda
2. **Cek speaker/headphone** sudah terpasang
3. **Klik tombol speaker (🔊)** untuk play audio

### Aplikasi tidak bisa dibuka:
1. **Pastikan backend running:**
   ```bash
   cd backend
   ./start.sh
   ```
2. **Pastikan frontend running:**
   ```bash
   cd frontend
   npm start
   ```
3. **Cek port** - pastikan port 8000 dan 3000 tidak digunakan aplikasi lain

---

## 📞 Bantuan Lebih Lanjut

Jika mengalami masalah atau punya pertanyaan:

1. **Cek dokumentasi** di `README.md`
2. **Lihat logs** di folder `logs/`
3. **Restart aplikasi** (backend dan frontend)
4. **Hubungi developer** untuk support

---

## 🎉 Selamat Belajar!

Ingat: **Practice makes perfect!** 

Gunakan Macca setiap hari untuk hasil maksimal. Good luck! 🚀

---

**Versi:** 1.0  
**Terakhir diupdate:** 2024  
**Bahasa:** Bahasa Indonesia
