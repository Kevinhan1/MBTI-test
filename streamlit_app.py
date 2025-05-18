import streamlit as st
import random

# Pertanyaan MBTI
question_pool = {
    'EI': [
        ("Apakah Anda merasa berenergi setelah bersosialisasi dengan banyak orang?", "Ya, sangat berenergi", "Tidak, merasa lelah"),
        ("Apakah Anda lebih suka berbicara di grup besar atau percakapan satu lawan satu?", "Grup besar", "Satu lawan satu"),
        ("Apakah Anda biasanya memulai percakapan dengan orang asing?", "Ya", "Tidak"),
        ("Apakah Anda lebih suka berada di tempat ramai daripada menyendiri?", "Ya", "Tidak"),
        ("Apakah Anda menikmati menjadi pusat perhatian?", "Ya", "Tidak"),
        ("Apakah Anda cenderung bertindak terlebih dahulu lalu berpikir, atau berpikir dulu lalu bertindak?", "Bertindak dahulu", "Berpikir dahulu"),
        ("Ketika sendirian dalam waktu lama, apakah Anda merasa kesepian?", "Ya", "Tidak"),
        ("Apakah Anda lebih sering berbicara atau mendengarkan dalam percakapan?", "Berbicara", "Mendengarkan"),
        ("Apakah Anda lebih suka aktivitas kelompok daripada aktivitas individu?", "Kelompok", "Individu"),
    ],
    'SN': [
        ("Apakah Anda fokus pada detail atau gambaran besar?", "Detail", "Gambaran besar"),
        ("Apakah Anda lebih suka informasi konkret atau ide abstrak?", "Konkret", "Abstrak"),
        ("Apakah Anda cenderung memperhatikan fakta atau kemungkinan?", "Fakta", "Kemungkinan"),
        ("Apakah Anda lebih suka instruksi langkah demi langkah atau eksplorasi bebas?", "Langkah demi langkah", "Eksplorasi bebas"),
        ("Apakah Anda lebih tertarik pada apa yang nyata atau apa yang mungkin?", "Yang nyata", "Yang mungkin"),
        ("Apakah Anda menikmati rutinitas atau variasi?", "Rutinitas", "Variasi"),
        ("Apakah Anda memercayai hal yang bisa dibuktikan atau ide yang belum terbukti?", "Yang bisa dibuktikan", "Ide yang belum terbukti"),
        ("Apakah Anda biasanya mendeskripsikan sesuatu secara literal atau menggunakan perbandingan/metafora?", "Literal", "Metafora"),
        ("Apakah Anda lebih suka fakta atau teori?", "Fakta", "Teori"),
    ],
    'TF': [
        ("Dalam membuat keputusan, apakah Anda lebih mengandalkan logika atau perasaan?", "Logika", "Perasaan"),
        ("Apakah Anda lebih menghargai keadilan atau empati?", "Keadilan", "Empati"),
        ("Apakah Anda merasa nyaman memberi kritik langsung?", "Ya", "Tidak"),
        ("Apakah Anda lebih sering menyelesaikan konflik dengan debat atau dengan kompromi?", "Debat", "Kompromi"),
        ("Apakah Anda merasa keputusan harus adil atau mempertimbangkan perasaan semua orang?", "Adil", "Pertimbangkan perasaan"),
        ("Apakah Anda lebih sering berpikir objektif atau subjektif?", "Objektif", "Subjektif"),
        ("Apakah Anda menilai diri Anda lebih rasional atau penuh empati?", "Rasional", "Penuh empati"),
        ("Apakah Anda cenderung fokus pada hasil atau dampak emosional?", "Hasil", "Dampak emosional"),
        ("Apakah Anda merasa nyaman membuat keputusan sulit tanpa terpengaruh emosi?", "Ya", "Tidak"),
    ],
    'JP': [
        ("Apakah Anda lebih suka memiliki rencana yang jelas atau fleksibilitas?", "Rencana yang jelas", "Fleksibilitas"),
        ("Apakah Anda menyelesaikan tugas jauh sebelum tenggat atau mendekati akhir?", "Sebelum tenggat", "Mendekati akhir"),
        ("Apakah Anda merasa terganggu saat rencana berubah tiba-tiba?", "Ya", "Tidak"),
        ("Apakah Anda lebih produktif dengan jadwal atau spontanitas?", "Jadwal", "Spontanitas"),
        ("Apakah Anda suka menyelesaikan tugas sebelum bersantai atau sebaliknya?", "Tugas dulu", "Santai dulu"),
        ("Apakah Anda suka membuat to-do list atau mengikuti alur?", "To-do list", "Mengikuti alur"),
        ("Apakah Anda merasa nyaman dengan struktur atau fleksibilitas waktu?", "Struktur", "Fleksibilitas"),
        ("Apakah Anda merasa stres jika sesuatu tidak selesai tepat waktu?", "Ya", "Tidak"),
        ("Apakah Anda suka menyusun rencana atau spontan menghadapi hari?", "Rencana", "Spontan"),
    ]
}

EVIDENCE_THRESHOLD = 5  # Biar gak kelamaan di Streamlit, contoh threshold kecil

# Inisialisasi session state
if "scores" not in st.session_state:
    st.session_state.scores = {'E':0,'I':0,'S':0,'N':0,'T':0,'F':0,'J':0,'P':0}
if "concluded_dichotomies" not in st.session_state:
    st.session_state.concluded_dichotomies = {'EI': False, 'SN': False, 'TF': False, 'JP': False}
if "question_pool" not in st.session_state:
    # Copy question_pool ke session state, supaya tidak kehabisan asli
    st.session_state.question_pool = {k:list(v) for k,v in question_pool.items()}
if "current_dichotomy" not in st.session_state:
    st.session_state.current_dichotomy = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "finished" not in st.session_state:
    st.session_state.finished = False

def get_mbti_type(final_scores):
    mbti = ""
    mbti += 'E' if final_scores['E'] > final_scores['I'] else 'I'
    mbti += 'S' if final_scores['S'] > final_scores['N'] else 'N'
    mbti += 'T' if final_scores['T'] > final_scores['F'] else 'F'
    mbti += 'J' if final_scores['J'] > final_scores['P'] else 'P'
    return mbti

st.title("🧠 Tes Kepribadian MBTI")

if not st.session_state.finished:

    # Tentukan dikotomi yang belum selesai
    available_dichotomies = [d for d,v in st.session_state.concluded_dichotomies.items() if not v]

    if st.session_state.current_dichotomy is None or st.session_state.current_dichotomy not in available_dichotomies:
        if not available_dichotomies:
            st.session_state.finished = True
        else:
            st.session_state.current_dichotomy = random.choice(available_dichotomies)

    if not st.session_state.finished:
        cd = st.session_state.current_dichotomy

        if st.session_state.current_question is None:
            # Ambil pertanyaan pertama dikotomi terpilih
            if st.session_state.question_pool[cd]:
                st.session_state.current_question = st.session_state.question_pool[cd].pop(0)
            else:
                # Jika habis pertanyaan, tandai selesai
                st.session_state.concluded_dichotomies[cd] = True
                st.session_state.current_question = None
                st.experimental_rerun()

        if st.session_state.current_question:
            question, opt1, opt2 = st.session_state.current_question
            st.write(f"**{question}**")
            pilihan = st.radio("Pilih jawaban Anda:", [opt1, opt2], key="jawaban")

            if st.button("Submit Jawaban"):
                pref1, pref2 = cd[0], cd[1]
                # Hitung skor berdasarkan pilihan
                if pilihan == opt1:
                    st.session_state.scores[pref1] += 1
                else:
                    st.session_state.scores[pref2] += 1

                # Cek apakah skor sudah cukup untuk simpulkan dikotomi
                if abs(st.session_state.scores[pref1] - st.session_state.scores[pref2]) >= EVIDENCE_THRESHOLD:
                    st.session_state.concluded_dichotomies[cd] = True
                    st.success(f"Preferensi {cd} sudah cukup jelas, lanjut ke bagian berikutnya.")

                st.session_state.current_question = None
                st.experimental_rerun()
else:
    st.write("### Terima kasih telah menyelesaikan tes!")
    final_type = get_mbti_type(st.session_state.scores)
    st.write(f"**Tipe MBTI Anda adalah: {final_type}**")

    if st.button("Mulai Ulang Tes"):
        for k in st.session_state.scores:
            st.session_state.scores[k] = 0
        for k in st.session_state.concluded_dichotomies:
            st.session_state.concluded_dichotomies[k] = False
        st.session_state.question_pool = {k:list(v) for k,v in question_pool.items()}
        st.session_state.current_dichotomy = None
        st.session_state.current_question = None
        st.session_state.finished = False
        st.experimental_rerun()
