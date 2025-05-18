import streamlit as st
import random

# Threshold untuk menyimpulkan preferensi
EVIDENCE_THRESHOLD = 5

# Pertanyaan dengan opsi deskriptif
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

# Inisialisasi session state
if "scores" not in st.session_state:
    st.session_state.scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    st.session_state.questions = {k: v.copy() for k, v in question_pool.items()}
    st.session_state.concluded = {'EI': False, 'SN': False, 'TF': False, 'JP': False}

st.title("Tes MBTI Sederhana")
st.write("Pilih jawaban yang paling menggambarkan Anda. Sistem akan berhenti saat sudah cukup bukti untuk menentukan MBTI.")

# Fungsi menghitung MBTI
def get_mbti(scores):
    return ''.join([
        'E' if scores['E'] > scores['I'] else 'I',
        'S' if scores['S'] > scores['N'] else 'N',
        'T' if scores['T'] > scores['F'] else 'F',
        'J' if scores['J'] > scores['P'] else 'P',
    ])

# Proses pertanyaan
if not all(st.session_state.concluded.values()):
    available = [k for k, v in st.session_state.concluded.items() if not v and st.session_state.questions[k]]
    if available:
        dichotomy = random.choice(available)
        pref1, pref2 = dichotomy[0], dichotomy[1]
        q_text, opt1, opt2 = st.session_state.questions[dichotomy].pop(0)

        st.subheader(q_text)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(opt1, key="1"):
                st.session_state.scores[pref1] += 1
                if abs(st.session_state.scores[pref1] - st.session_state.scores[pref2]) >= EVIDENCE_THRESHOLD:
                    st.session_state.concluded[dichotomy] = True
                st.rerun()
        with col2:
            if st.button(opt2, key="2"):
                st.session_state.scores[pref2] += 1
                if abs(st.session_state.scores[pref1] - st.session_state.scores[pref2]) >= EVIDENCE_THRESHOLD:
                    st.session_state.concluded[dichotomy] = True
                st.rerun()
    else:
        for d in st.session_state.concluded:
            st.session_state.concluded[d] = True
        st.rerun()
else:
    mbti_result = get_mbti(st.session_state.scores)
    st.success(f"Tipe MBTI Anda adalah: **{mbti_result}**")
    st.write("Skor akhir:", st.session_state.scores)

    phone = st.text_input("Masukkan nomor WhatsApp Anda (format 628xxxxxxxxxx):")
    if phone:
        message = f"Halo! Ini hasil tes MBTI Anda: {mbti_result}\nSkor: {st.session_state.scores}"
        encoded_message = message.replace(' ', '%20').replace('\n', '%0A')
        wa_url = f"https://wa.me/{phone}?text={encoded_message}"
        st.markdown(f"[Klik di sini untuk kirim hasil ke WhatsApp Anda]({wa_url})", unsafe_allow_html=True)

    if st.button("Ulangi Tes"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
