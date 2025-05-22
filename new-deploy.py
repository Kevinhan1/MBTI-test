import streamlit as st

# --- Daftar Pertanyaan ---
questions = [
    # E/I
    "Saya merasa berenergi setelah menghabiskan waktu dengan banyak orang.",
    "Saya lebih suka berbicara daripada mendengarkan.",
    "Saya senang menjadi pusat perhatian.",
    "Saya mudah bosan jika sendirian.",
    "Saya lebih memilih kerja kelompok.",
    "Saya sering mengungkapkan pikiran secara spontan.",
    "Saya punya banyak teman dan kenalan.",
    "Saya nyaman di acara sosial.",
    "Saya senang memulai percakapan.",
    "Saya cenderung berpikir keras setelah berbicara.",
    # S/N
    "Saya fokus pada fakta daripada teori.",
    "Saya suka petunjuk langkah demi langkah.",
    "Saya percaya pengalaman lebih penting dari imajinasi.",
    "Saya tertarik pada kenyataan daripada kemungkinan.",
    "Saya suka hal-hal praktis.",
    "Saya memperhatikan detail kecil.",
    "Saya mengandalkan bukti nyata.",
    "Saya nyaman dengan rutinitas.",
    "Saya lebih suka sejarah daripada fiksi.",
    "Saya pilih solusi terbukti daripada ide baru.",
    # T/F
    "Saya gunakan logika saat mengambil keputusan.",
    "Saya peduli kebenaran daripada harmoni.",
    "Kritik objektif lebih penting daripada dukungan emosional.",
    "Saya analitis daripada empatik.",
    "Saya bisa memisahkan emosi dari fakta.",
    "Saya menghargai keadilan daripada belas kasihan.",
    "Saya suka debat intelektual.",
    "Saya gunakan kepala daripada hati.",
    "Saya fokus pada hasil daripada perasaan.",
    "Kebenaran harus diutamakan meski menyakitkan.",
    # J/P
    "Saya membuat rencana sebelum bertindak.",
    "Saya nyaman dengan jadwal terstruktur.",
    "Saya tidak suka menunda pekerjaan.",
    "Saya pilih kepastian daripada fleksibilitas.",
    "Saya stres tanpa daftar tugas.",
    "Saya selesaikan proyek sebelum bersantai.",
    "Saya rapi dan terorganisir.",
    "Saya suka keputusan cepat.",
    "Saya tidak nyaman dengan perubahan mendadak.",
    "Saya suka aturan jelas."
]

# --- Kategori Index ---
categories = {
    "E/I": (0, 10),
    "S/N": (10, 20),
    "T/F": (20, 30),
    "J/P": (30, 40)
}
threshold = 30.5

# --- MBTI DATA ---
mbti_data = {
    "INTJ": {"deskripsi": "Perencana strategis", "pekerjaan": ["System Analyst", "Project Manager"]},
    "ENFP": {"deskripsi": "Pemberi semangat", "pekerjaan": ["Product Manager", "Kreator Konten"]},
    # tambahkan lainnya jika perlu
}

# --- Init State ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = []
    st.session_state.cat_scores = {k: 0 for k in categories}

# --- Fungsi ---
def get_category(idx):
    for cat, (start, end) in categories.items():
        if start <= idx < end:
            return cat
    return None

def jump_to_next_category(idx):
    keys = list(categories.keys())
    curr = get_category(idx)
    i = keys.index(curr)
    return categories[keys[i + 1]][0] if i + 1 < len(keys) else len(questions)

def advance(skor):
    idx = st.session_state.current_q
    cat = get_category(idx)
    st.session_state.scores.append(skor)
    st.session_state.cat_scores[cat] += skor

    # Debug info
    st.write(f"Kategori: {cat}, Skor Baru: {st.session_state.cat_scores[cat]}")

    if st.session_state.cat_scores[cat] >= threshold:
        st.session_state.current_q = jump_to_next_category(idx)
    else:
        st.session_state.current_q += 1

    st.experimental_rerun()

# --- Tampilan ---
st.title("Tes MBTI Sederhana")
st.caption("Skala 1 = Tidak Setuju → 5 = Sangat Setuju")

if st.session_state.current_q < len(questions):
    idx = st.session_state.current_q
    skor = st.slider(questions[idx], 1, 5, 3, key=f"q_{idx}")
    if st.button("Berikutnya"):
        advance(skor)
else:
    score = st.session_state.cat_scores
    tipe = ""
    tipe += "E" if score["E/I"] > threshold else "I"
    tipe += "S" if score["S/N"] > threshold else "N"
    tipe += "T" if score["T/F"] > threshold else "F"
    tipe += "J" if score["J/P"] > threshold else "P"

    st.success(f"Tipe MBTI Anda: {tipe}")
    if tipe in mbti_data:
        st.write(f"Deskripsi: {mbti_data[tipe]['deskripsi']}")
        st.write("Pekerjaan Cocok:")
        for i, job in enumerate(mbti_data[tipe]['pekerjaan'], 1):
            st.write(f"{i}. {job}")
    else:
        st.warning("Belum ada data lengkap untuk tipe ini.")

    if st.button("Ulangi Tes"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
