import streamlit as st
import random

threshold = 4

question_pool = {
    'EI': [
        ("Apakah Kamu merasa berenergi setelah bersosialisasi dengan banyak orang?", "Ya, sangat berenergi", "Tidak, merasa lelah"),
        ("Apakah Kamu lebih suka berbicara di grup besar atau percakapan satu lawan satu?", "Grup besar", "Satu lawan satu"),
        ("Apakah Kamu biasanya memulai percakapan dengan orang asing?", "Ya", "Tidak"),
        ("Apakah Kamu lebih suka berada di tempat ramai daripada menyendiri?", "Ya", "Tidak"),
        ("Apakah Kamu menikmati menjadi pusat perhatian?", "Ya", "Tidak"),
        ("Apakah Kamu cenderung bertindak terlebih dahulu lalu berpikir, atau berpikir dulu lalu bertindak?", "Bertindak dahulu", "Berpikir dahulu"),
        ("Ketika sendirian dalam waktu lama, apakah Kamu merasa kesepian?", "Ya", "Tidak"),
        ("Apakah Kamu lebih sering berbicara atau mendengarkan dalam percakapan?", "Berbicara", "Mendengarkan"),
        ("Apakah Kamu lebih suka aktivitas kelompok daripada aktivitas individu?", "Kelompok", "Individu"),
    ],
    'SN': [
        ("Apakah Kamu fokus pada detail atau gambaran besar?", "Detail", "Gambaran besar"),
        ("Apakah Kamu lebih suka informasi konkret atau ide abstrak?", "Konkret", "Abstrak"),
        ("Apakah Kamu cenderung memperhatikan fakta atau kemungkinan?", "Fakta", "Kemungkinan"),
        ("Apakah Kamu lebih suka instruksi langkah demi langkah atau eksplorasi bebas?", "Langkah demi langkah", "Eksplorasi bebas"),
        ("Apakah Kamu lebih tertarik pada apa yang nyata atau apa yang mungkin?", "Yang nyata", "Yang mungkin"),
        ("Apakah Kamu menikmati rutinitas atau variasi?", "Rutinitas", "Variasi"),
        ("Apakah Kamu memercayai hal yang bisa dibuktikan atau ide yang belum terbukti?", "Yang bisa dibuktikan", "Ide yang belum terbukti"),
        ("Apakah Kamu biasanya mendeskripsikan sesuatu secara literal atau menggunakan perbandingan/metafora?", "Literal", "Metafora"),
        ("Apakah Kamu lebih suka fakta atau teori?", "Fakta", "Teori"),
    ],
    'TF': [
        ("Dalam membuat keputusan, apakah Kamu lebih mengKamulkan logika atau perasaan?", "Logika", "Perasaan"),
        ("Apakah Kamu lebih menghargai keadilan atau empati?", "Keadilan", "Empati"),
        ("Apakah Kamu merasa nyaman memberi kritik langsung?", "Ya", "Tidak"),
        ("Apakah Kamu lebih sering menyelesaikan konflik dengan debat atau dengan kompromi?", "Debat", "Kompromi"),
        ("Apakah Kamu merasa keputusan harus adil atau mempertimbangkan perasaan semua orang?", "Adil", "Pertimbangkan perasaan"),
        ("Apakah Kamu lebih sering berpikir objektif atau subjektif?", "Objektif", "Subjektif"),
        ("Apakah Kamu menilai diri Kamu lebih rasional atau penuh empati?", "Rasional", "Penuh empati"),
        ("Apakah Kamu cenderung fokus pada hasil atau dampak emosional?", "Hasil", "Dampak emosional"),
        ("Apakah Kamu merasa nyaman membuat keputusan sulit tanpa terpengaruh emosi?", "Ya", "Tidak"),
    ],
    'JP': [
        ("Apakah Kamu lebih suka memiliki rencana yang jelas atau fleksibilitas?", "Rencana yang jelas", "Fleksibilitas"),
        ("Apakah Kamu menyelesaikan tugas jauh sebelum tenggat atau mendekati akhir?", "Sebelum tenggat", "Mendekati akhir"),
        ("Apakah Kamu merasa terganggu saat rencana berubah tiba-tiba?", "Ya", "Tidak"),
        ("Apakah Kamu lebih produktif dengan jadwal atau spontanitas?", "Jadwal", "Spontanitas"),
        ("Apakah Kamu suka menyelesaikan tugas sebelum bersantai atau sebaliknya?", "Tugas dulu", "Santai dulu"),
        ("Apakah Kamu suka membuat to-do list atau mengikuti alur?", "To-do list", "Mengikuti alur"),
        ("Apakah Kamu merasa nyaman dengan struktur atau fleksibilitas waktu?", "Struktur", "Fleksibilitas"),
        ("Apakah Kamu merasa stres jika sesuatu tidak selesai tepat waktu?", "Ya", "Tidak"),
        ("Apakah Kamu suka menyusun rencana atau spontan menghadapi hari?", "Rencana", "Spontan"),
    ]
}

def get_mbti_type(final_scores):
    mbti = ""
    mbti += 'E' if final_scores['E'] > final_scores['I'] else 'I'
    mbti += 'S' if final_scores['S'] > final_scores['N'] else 'N'
    mbti += 'T' if final_scores['T'] > final_scores['F'] else 'F'
    mbti += 'J' if final_scores['J'] > final_scores['P'] else 'P'
    return mbti

def check_threshold(scores):
    completed = []
    for a, b in [('E', 'I'), ('S', 'N'), ('T', 'F'), ('J', 'P')]:
        if abs(scores[a] - scores[b]) >= threshold:
            completed.append((a if scores[a] > scores[b] else b))
    return len(completed) == 4  # All 4 dimensions decided

# Inisialisasi session_state
if "name" not in st.session_state:
    st.session_state.name = ""

if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in ['E','I','S','N','T','F','J','P']}

if "questions" not in st.session_state:
    st.session_state.questions = []
    for dichotomy, questions in question_pool.items():
        q_copy = questions.copy()
        random.shuffle(q_copy)
        for q in q_copy:
            st.session_state.questions.append((dichotomy, q))
    random.shuffle(st.session_state.questions)

if "current" not in st.session_state:
    st.session_state.current = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("Tes Kepribadian")

# Jika nama belum diisi, tampilkan input nama dulu
if not st.session_state.name:
    name_input = st.text_input("Masukkan nama Kamu untuk memulai tes:")
    if st.button("Mulai Tes") and name_input.strip() != "":
        st.session_state.name = name_input.strip()
        st.rerun()
else:
    if not st.session_state.finished:
        if st.session_state.current >= len(st.session_state.questions) or check_threshold(st.session_state.scores):
            st.session_state.finished = True
            st.rerun()  # rerun untuk pindah ke hasil
        else:
            dichotomy, (question, opt1, opt2) = st.session_state.questions[st.session_state.current]
            st.markdown(f"**{question}**")

            col1, col2 = st.columns(2)
            if col1.button(opt1):
                st.session_state.scores[dichotomy[0]] += 1
                st.session_state.current += 1
                st.rerun()
            if col2.button(opt2):
                st.session_state.scores[dichotomy[1]] += 1
                st.session_state.current += 1
                st.rerun()
    else:
        st.success(f"Tes selesai, {st.session_state.name}!")
        mbti_result = get_mbti_type(st.session_state.scores)
        st.markdown(f"### Tipe Kepribadianmu adalah **{mbti_result}**")

        formatted_scores = ""
        pairs = [('E', 'I'), ('S', 'N'), ('T', 'F'), ('J', 'P')]
        for a, b in pairs:
            formatted_scores += f"{a}: {st.session_state.scores[a]}, {b}: {st.session_state.scores[b]}\n"

        st.text("Skor akhir:\n" + formatted_scores)

        phone = st.text_input("Masukkan nomor WhatsApp Kamu (format 628xxxxxxxxxx):")
        if phone:
            message = f"Halo {st.session_state.name}! Ini hasil Tes Kepribadianmu : {mbti_result}\nSkor:\n{formatted_scores}"
            encoded_message = message.replace(' ', '%20').replace('\n', '%0A')
            wa_url = f"https://wa.me/{phone}?text={encoded_message}"
            st.markdown(f"[Klik di sini untuk kirim hasil ke WhatsApp Kamu]({wa_url})", unsafe_allow_html=True)

        if st.button("Ulangi Tes"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
