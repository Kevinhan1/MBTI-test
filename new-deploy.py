import streamlit as st
import random

# Threshold untuk menyimpulkan preferensi
EVIDENCE_THRESHOLD = 5  # Kamu bisa ubah ini nanti

# Pool pertanyaan
question_pool_data = {
    'EI': [
        ("Apakah Anda merasa berenergi setelah bersosialisasi dengan banyak orang?", "E", "I"),
        ("Apakah Anda lebih suka berbicara di grup besar atau percakapan satu lawan satu?", "E", "I"),
        ("Apakah Anda biasanya memulai percakapan dengan orang asing?", "E", "I"),
        ("Apakah Anda lebih suka berada di tempat ramai daripada menyendiri?", "E", "I"),
        ("Apakah Anda menikmati menjadi pusat perhatian?", "E", "I"),
        ("Apakah Anda cenderung bertindak terlebih dahulu lalu berpikir, atau berpikir dulu lalu bertindak?", "E", "I"),
        ("Ketika sendirian dalam waktu lama, apakah Anda merasa kesepian?", "E", "I"),
        ("Apakah Anda lebih sering berbicara atau mendengarkan dalam percakapan?", "E", "I"),
        ("Apakah Anda lebih suka aktivitas kelompok daripada aktivitas individu?", "E", "I"),
    ],
    'SN': [
        ("Apakah Anda fokus pada detail atau gambaran besar?", "S", "N"),
        ("Apakah Anda lebih suka informasi konkret atau ide abstrak?", "S", "N"),
        ("Apakah Anda cenderung memperhatikan fakta atau kemungkinan?", "S", "N"),
        ("Apakah Anda lebih suka instruksi langkah demi langkah atau eksplorasi bebas?", "S", "N"),
        ("Apakah Anda lebih tertarik pada apa yang nyata atau apa yang mungkin?", "S", "N"),
        ("Apakah Anda menikmati rutinitas atau variasi?", "S", "N"),
        ("Apakah Anda memercayai hal yang bisa dibuktikan atau ide yang belum terbukti?", "S", "N"),
        ("Apakah Anda biasanya mendeskripsikan sesuatu secara literal atau menggunakan perbandingan/metafora?", "S", "N"),
        ("Apakah Anda lebih suka fakta atau teori?", "S", "N"),
    ],
    'TF': [
        ("Dalam membuat keputusan, apakah Anda lebih mengandalkan logika atau perasaan?", "T", "F"),
        ("Apakah Anda lebih menghargai keadilan atau empati?", "T", "F"),
        ("Apakah Anda merasa nyaman memberi kritik langsung?", "T", "F"),
        ("Apakah Anda lebih sering menyelesaikan konflik dengan debat atau dengan kompromi?", "T", "F"),
        ("Apakah Anda merasa keputusan harus adil atau mempertimbangkan perasaan semua orang?", "T", "F"),
        ("Apakah Anda lebih sering berpikir objektif atau subjektif?", "T", "F"),
        ("Apakah Anda menilai diri Anda lebih rasional atau penuh empati?", "T", "F"),
        ("Apakah Anda cenderung fokus pada hasil atau dampak emosional?", "T", "F"),
        ("Apakah Anda merasa nyaman membuat keputusan sulit tanpa terpengaruh emosi?", "T", "F"),
    ],
    'JP': [
        ("Apakah Anda lebih suka memiliki rencana yang jelas atau fleksibilitas?", "J", "P"),
        ("Apakah Anda menyelesaikan tugas jauh sebelum tenggat atau mendekati akhir?", "J", "P"),
        ("Apakah Anda merasa terganggu saat rencana berubah tiba-tiba?", "J", "P"),
        ("Apakah Anda lebih produktif dengan jadwal atau spontanitas?", "J", "P"),
        ("Apakah Anda suka menyelesaikan tugas sebelum bersantai atau sebaliknya?", "J", "P"),
        ("Apakah Anda suka membuat to-do list atau mengikuti alur?", "J", "P"),
        ("Apakah Anda merasa nyaman dengan struktur atau fleksibilitas waktu?", "J", "P"),
        ("Apakah Anda merasa stres jika sesuatu tidak selesai tepat waktu?", "J", "P"),
        ("Apakah Anda suka menyusun rencana atau spontan menghadapi hari?", "J", "P"),
    ]
}

# Inisialisasi session state
if "scores" not in st.session_state:
    st.session_state.scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    st.session_state.questions = {k: v.copy() for k, v in question_pool_data.items()}
    st.session_state.concluded = {'EI': False, 'SN': False, 'TF': False, 'JP': False}
    st.session_state.current = None
    st.session_state.result = None

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
        q = st.session_state.questions[dichotomy].pop(0)

        st.subheader(q[0])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("1", key="1"):
                st.session_state.scores[pref1] += 1
                if abs(st.session_state.scores[pref1] - st.session_state.scores[pref2]) >= EVIDENCE_THRESHOLD:
                    st.session_state.concluded[dichotomy] = True
                st.rerun()
        with col2:
            if st.button("2", key="2"):
                st.session_state.scores[pref2] += 1
                if abs(st.session_state.scores[pref1] - st.session_state.scores[pref2]) >= EVIDENCE_THRESHOLD:
                    st.session_state.concluded[dichotomy] = True
                st.rerun()

    else:
        # Jika semua pertanyaan habis
        for d in st.session_state.concluded:
            st.session_state.concluded[d] = True
        st.rerun()
else:
    mbti_result = get_mbti(st.session_state.scores)
    st.success(f"Tipe MBTI Anda adalah: **{mbti_result}**")
    st.write("Skor akhir:", st.session_state.scores)

    # Input nomor WhatsApp
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