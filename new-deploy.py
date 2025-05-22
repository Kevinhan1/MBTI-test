import streamlit as st
import numpy as np

# Daftar pertanyaan MBTI (40 pertanyaan)
questions = [
    # Extraversion (E) vs Introversion (I) - 10 pertanyaan
    "1. Saya merasa berenergi setelah menghabiskan waktu dengan banyak orang.",
    "2. Saya lebih suka berbicara daripada mendengarkan dalam percakapan.",
    "3. Saya senang menjadi pusat perhatian dalam kelompok.",
    "4. Saya mudah bosan jika sendirian terlalu lama.",
    "5. Saya lebih memilih kerja kelompok daripada bekerja sendiri.",
    "6. Saya sering mengungkapkan pikiran saya secara spontan.",
    "7. Saya memiliki banyak teman dan kenalan.",
    "8. Saya merasa lebih nyaman di acara sosial daripada di rumah sendirian.",
    "9. Saya senang memulai percakapan dengan orang asing.",
    "10. Saya cenderung berpikir keras setelah berbicaran.",
    # Sensing (S) vs Intuition (N) - 10 pertanyaan
    "11. Saya lebih fokus pada fakta daripada teori abstrak.",
    "12. Saya lebih suka petunjuk langkah demi langkah daripada ide besar.",
    "13. Saya percaya pengalaman lebih penting daripada imajinasi.",
    "14. Saya lebih tertarik pada 'apa yang ada' daripada 'apa yang mungkin'.",
    "15. Saya lebih suka hal-hal praktis daripada konsep filosofis.",
    "16. Saya memperhatikan detail kecil dalam lingkungan sekitar.",
    "17. Saya lebih mengandalkan bukti nyata daripada firasat.",
    "18. Saya lebih nyaman dengan rutinitas yang jelas.",
    "19. Saya lebih suka sejarah daripada sains fiksi.",
    "20. Saya lebih memilih solusi yang sudah terbukti daripada ide baru.",
    # Thinking (T) vs Feeling (F) - 10 pertanyaan
    "21. Saya lebih memilih logika daripada perasaan saat mengambil keputusan.",
    "22. Saya lebih peduli kebenaran daripada harmoni dalam diskusi.",
    "23. Kritik objektif lebih penting bagi saya daripada dukungan emosional.",
    "24. Saya cenderung analitis daripada empatik.",
    "25. Saya lebih mudah memisahkan emosi dari fakta.",
    "26. Saya lebih menghargai keadilan daripada belas kasihan.",
    "27. Saya lebih suka debat intelektual daripada percakapan emosional.",
    "28. Saya lebih sering menggunakan 'kepala' daripada 'hati'.",
    "29. Saya lebih fokus pada hasil daripada perasaan orang lain.",
    "30. Saya percaya bahwa kebenaran harus diutamakan meski menyakiti perasaan.",
    # Judging (J) vs Perceiving (P) - 10 pertanyaan
    "31. Saya suka membuat rencana terlebih dahulu sebelum bertindak.",
    "32. Saya lebih nyaman dengan jadwal yang terstruktur.",
    "33. Saya tidak suka menunda-nunda pekerjaan.",
    "34. Saya lebih memilih kepastian daripada fleksibilitas.",
    "35. Saya merasa stres jika tidak memiliki daftar tugas yang jelas.",
    "36. Saya lebih suka menyelesaikan proyek sebelum bersantai.",
    "37. Saya cenderung rapi dan terorganisir.",
    "38. Saya lebih suka keputusan cepat daripada menimbang terlalu lama.",
    "39. Saya merasa tidak nyaman dengan perubahan mendadak.",
    "40. Saya lebih suka aturan yang jelas daripada kebebasan mutlak."
]

# Data MBTI
mbti_data = {
    "ISTJ": {"deskripsi": "Inspektur...", "pekerjaan": ["Auditor IT", "Analis Data"]},
    "ISFJ": {"deskripsi": "Pemelihara...", "pekerjaan": ["IT Support", "Admin Sistem"]},
    "INFJ": {"deskripsi": "Konselor...", "pekerjaan": ["Konsultan IT", "Analis Bisnis"]},
    "INTJ": {"deskripsi": "Perencana...", "pekerjaan": ["System Analyst", "PM"]},
    "INTP": {"deskripsi": "Pemikir...", "pekerjaan": ["Programmer", "Data Scientist"]},
    "ESTJ": {"deskripsi": "Eksekutor...", "pekerjaan": ["Manager Proyek IT"]},
    "ESFJ": {"deskripsi": "Pemberi...", "pekerjaan": ["Trainer IT", "IT Support"]},
    "ENFJ": {"deskripsi": "Guru...", "pekerjaan": ["PM", "Konsultan IT"]},
    "ENFP": {"deskripsi": "Penginspirasi...", "pekerjaan": ["Product Manager"]},
    "ISTP": {"deskripsi": "Pengrajin...", "pekerjaan": ["Network Engineer"]},
    "ISFP": {"deskripsi": "Seniman...", "pekerjaan": ["UI/UX Designer"]},
    "INFP": {"deskripsi": "Idealis...", "pekerjaan": ["Content Developer"]},
    "ESTP": {"deskripsi": "Pengusaha...", "pekerjaan": ["Cybersecurity"]},
    "ESFP": {"deskripsi": "Penghibur...", "pekerjaan": ["Digital Content Creator"]},
    "ENTJ": {"deskripsi": "Komandan...", "pekerjaan": ["Auditor", "PM"]},
    "ENTP": {"deskripsi": "Pendebat...", "pekerjaan": ["Product Manager", "Konsultan"]}
}

# Index per kategori
categories = {"E/I": (0, 10), "S/N": (10, 20), "T/F": (20, 30), "J/P": (30, 40)}
threshold = 30.5

# Inisialisasi session_state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.category_scores = {k: 0 for k in categories}

# Mendapatkan kategori dari index pertanyaan
def get_category_for_question(idx):
    for cat, (start, end) in categories.items():
        if start <= idx < end:
            return cat
    return None

# Fungsi lompat ke kategori berikutnya
def jump_to_next_category(current_idx):
    keys = list(categories.keys())
    curr_cat = get_category_for_question(current_idx)
    i = keys.index(curr_cat)
    return categories[keys[i + 1]][0] if i + 1 < len(keys) else 40

# Fungsi untuk lanjutkan pertanyaan
def advance_question(skor):
    idx = st.session_state.current_q
    cat = get_category_for_question(idx)
    st.session_state.answers.append(skor)
    st.session_state.category_scores[cat] += skor

    if st.session_state.category_scores[cat] >= threshold:
        st.session_state.current_q = jump_to_next_category(idx)
    else:
        st.session_state.current_q += 1

st.title("Tes Kepribadian MBTI")
st.write("Skala 1-5: 1 = Tidak Setuju, 5 = Sangat Setuju")

if st.session_state.current_q < len(questions):
    idx = st.session_state.current_q
    skor = st.slider(questions[idx], 1, 5, 3, key=f"slider_{idx}")
    if st.button("Pertanyaan Berikutnya"):
        advance_question(skor)
        st.experimental_rerun()
else:
    scores = st.session_state.category_scores
    tipe = ""
    tipe += "E" if scores["E/I"] > threshold else "I"
    tipe += "S" if scores["S/N"] > threshold else "N"
    tipe += "T" if scores["T/F"] > threshold else "F"
    tipe += "J" if scores["J/P"] > threshold else "P"

    st.subheader("Hasil MBTI Anda")
    st.write(f"**Tipe Kepribadian: {tipe}**")
    st.write(f"**Deskripsi:** {mbti_data[tipe]['deskripsi']}")
    st.write("**Pekerjaan yang Cocok:**")
    for i, job in enumerate(mbti_data[tipe]['pekerjaan'], 1):
        st.write(f"{i}. {job}")

    if st.button("Ulangi Tes"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
