import streamlit as st
import random

# Data pertanyaan MBTI
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

def get_mbti_type(final_scores):
    mbti = ""
    mbti += 'E' if final_scores['E'] > final_scores['I'] else 'I'
    mbti += 'S' if final_scores['S'] > final_scores['N'] else 'N'
    mbti += 'T' if final_scores['T'] > final_scores['F'] else 'F'
    mbti += 'J' if final_scores['J'] > final_scores['P'] else 'P'
    return mbti

# Inisialisasi session_state
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in ['E','I','S','N','T','F','J','P']}

if "questions" not in st.session_state:
    st.session_state.questions = []
    for dichotomy, questions in question_pool.items():
        q_copy = questions.copy()
        random.shuffle(q_copy)  # Acak pertanyaan
        for q in q_copy:
            st.session_state.questions.append((dichotomy, q))

if "current" not in st.session_state:
    st.session_state.current = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("Tes MBTI Interaktif")

if not st.session_state.finished:
    dichotomy, (question, opt1, opt2) = st.session_state.questions[st.session_state.current]
    pilihan = st.radio(f"**{question}**", (opt1, opt2))

    if st.button("Lanjut"):
        if pilihan == opt1:
            st.session_state.scores[dichotomy[0]] += 1
        else:
            st.session_state.scores[dichotomy[1]] += 1

        st.session_state.current += 1

        if st.session_state.current >= len(st.session_state.questions):
            st.session_state.finished = True
else:
    st.success("Tes selesai!")
    mbti_result = get_mbti_type(st.session_state.scores)
    st.markdown(f"### Tipe MBTI Anda adalah: **{mbti_result}**")

    # Format skor agar tidak tampil sebagai dict
    formatted_scores = ""
    pairs = [('E', 'I'), ('S', 'N'), ('T', 'F'), ('J', 'P')]
    for a, b in pairs:
        formatted_scores += f"{a}: {st.session_state.scores[a]}, {b}: {st.session_state.scores[b]}\n"

    st.text("Skor akhir:\n" + formatted_scores)

    # Input nomor WhatsApp
    phone = st.text_input("Masukkan nomor WhatsApp Anda (format 628xxxxxxxxxx):")
    if phone:
        message = f"Halo! Ini hasil tes MBTI Anda: {mbti_result}\nSkor:\n{formatted_scores}"
        encoded_message = message.replace(' ', '%20').replace('\n', '%0A')
        wa_url = f"https://wa.me/{phone}?text={encoded_message}"
        st.markdown(f"[Klik di sini untuk kirim hasil ke WhatsApp Anda]({wa_url})", unsafe_allow_html=True)

    if st.button("Ulangi Tes"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
