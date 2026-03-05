import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Kecocokan Jurusan Politeknik",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Gradient header */
.main-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.main-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
.main-header p  { font-size: 1rem; opacity: 0.85; margin: 0.5rem 0 0; }

/* Section cards */
.section-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,.07);
}

/* Result card with colour coding */
.result-card {
    border-radius: 14px;
    padding: 1.5rem;
    margin: 0.6rem 0;
    border-left: 5px solid;
    transition: transform .15s;
}
.result-card:hover { transform: translateX(4px); }
.result-high   { background:#eff6ff; border-color:#2563eb; }
.result-medium { background:#f0fdf4; border-color:#16a34a; }
.result-low    { background:#fff7ed; border-color:#ea580c; }

/* Score badge */
.score-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.95rem;
}
.badge-high   { background:#dbeafe; color:#1d4ed8; }
.badge-medium { background:#dcfce7; color:#15803d; }
.badge-low    { background:#ffedd5; color:#c2410c; }

/* Info chips */
.chip {
    display:inline-block;
    background:#f1f5f9;
    border:1px solid #cbd5e1;
    color:#334155;
    border-radius:20px;
    padding:3px 12px;
    font-size:0.8rem;
    margin:3px;
}

/* Step indicator */
.step-box {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.step-num {
    width:32px; height:32px;
    background:#2563eb; color:white;
    border-radius:50%;
    display:inline-flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.95rem;
    margin-bottom:0.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] { background: #f0f4ff; }

/* Button */
div.stButton > button {
    background: linear-gradient(135deg,#1e3a8a,#3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
}
div.stButton > button:hover { opacity: 0.9 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data: Jurusan Profiles ───────────────────────────────────────────────────
JURUSAN = {
    "💼 Bisnis Digital": {
        "deskripsi": "Menggabungkan ilmu bisnis dengan teknologi digital untuk transformasi usaha modern.",
        "icon": "💼",
        "warna": "#2563eb",
        "prospek": ["Digital Marketing", "E-Commerce Manager", "Business Analyst", "Entrepreneur Digital", "Data Analyst Bisnis"],
        "kriteria": {
            "Minat Bisnis & Kewirausahaan": 0.25,
            "Kemampuan Matematika": 0.15,
            "Literasi Digital & Teknologi": 0.20,
            "Kemampuan Komunikasi": 0.20,
            "Kreativitas & Inovasi": 0.20,
        },
        "mata_pelajaran": ["Ekonomi", "TIK", "Matematika", "Bahasa Indonesia", "Bahasa Inggris"],
    },
    "💻 Rekayasa Perangkat Lunak": {
        "deskripsi": "Merancang dan membangun aplikasi serta sistem perangkat lunak berbasis teknologi terkini.",
        "icon": "💻",
        "warna": "#7c3aed",
        "prospek": ["Software Developer", "Mobile App Developer", "Web Developer", "QA Engineer", "DevOps Engineer"],
        "kriteria": {
            "Kemampuan Matematika": 0.25,
            "Logika & Pemecahan Masalah": 0.25,
            "Literasi Digital & Teknologi": 0.25,
            "Kreativitas & Inovasi": 0.15,
            "Kemampuan Komunikasi": 0.10,
        },
        "mata_pelajaran": ["Matematika", "Fisika", "TIK", "Logika", "Bahasa Inggris"],
    },
    "⚙️ Rekayasa Elektrikal Mekanik": {
        "deskripsi": "Mengintegrasikan sistem kelistrikan dan mekanik untuk industri dan manufaktur modern.",
        "icon": "⚙️",
        "warna": "#dc2626",
        "prospek": ["Teknisi Industri", "Electrical Engineer", "Maintenance Engineer", "Automation Specialist", "PLC Programmer"],
        "kriteria": {
            "Kemampuan Matematika": 0.25,
            "Minat Sains & Teknik": 0.30,
            "Logika & Pemecahan Masalah": 0.20,
            "Ketelitian & Presisi": 0.15,
            "Kemampuan Fisik & Praktikal": 0.10,
        },
        "mata_pelajaran": ["Matematika", "Fisika", "Kimia", "TIK", "Prakarya"],
    },
    "🤝 Relasi Industri": {
        "deskripsi": "Mengelola hubungan tenaga kerja, SDM, dan kebijakan ketenagakerjaan di dunia industri.",
        "icon": "🤝",
        "warna": "#059669",
        "prospek": ["HR Manager", "Industrial Relations Officer", "Labor Law Consultant", "Recruitment Specialist", "Training & Development"],
        "kriteria": {
            "Kemampuan Komunikasi": 0.30,
            "Minat Bisnis & Kewirausahaan": 0.15,
            "Empati & Kepedulian Sosial": 0.25,
            "Literasi Digital & Teknologi": 0.10,
            "Kreativitas & Inovasi": 0.20,
        },
        "mata_pelajaran": ["Bahasa Indonesia", "Bahasa Inggris", "Ekonomi", "Sosiologi", "PKn"],
    },
}

KRITERIA_ALL = [
    "Kemampuan Matematika",
    "Logika & Pemecahan Masalah",
    "Literasi Digital & Teknologi",
    "Minat Bisnis & Kewirausahaan",
    "Minat Sains & Teknik",
    "Kemampuan Komunikasi",
    "Kreativitas & Inovasi",
    "Empati & Kepedulian Sosial",
    "Ketelitian & Presisi",
    "Kemampuan Fisik & Praktikal",
]

MINAT_LIST = [
    "Coding / Pemrograman", "Desain Grafis", "Bisnis & Dagang",
    "Elektronika / Robotika", "Menulis & Berkomunikasi",
    "Analisis Data", "Mesin & Otomotif", "Kepemimpinan & Organisasi",
    "Sosial & Kemanusiaan", "Seni & Kreatif",
]

MAPEL_LIST = [
    "Matematika", "Fisika", "Kimia", "Biologi",
    "TIK / Informatika", "Bahasa Indonesia", "Bahasa Inggris",
    "Ekonomi", "Sosiologi", "PKn", "Prakarya",
]

# ─── Helper Functions ─────────────────────────────────────────────────────────
def hitung_skor(nilai_kriteria: dict) -> dict:
    hasil = {}
    for nama_jurusan, info in JURUSAN.items():
        skor = sum(
            nilai_kriteria.get(k, 0) * w
            for k, w in info["kriteria"].items()
        )
        # Normalize to 0-100
        max_skor = sum(10 * w for w in info["kriteria"].values())
        hasil[nama_jurusan] = round((skor / max_skor) * 100, 1)
    return hasil

def level_warna(skor):
    if skor >= 75: return "high",   "badge-high",   "🟢 Sangat Cocok"
    if skor >= 55: return "medium", "badge-medium", "🟡 Cukup Cocok"
    return             "low",    "badge-low",    "🔴 Kurang Cocok"

def hex_to_rgba(hex_color, alpha=0.2):
    """Convert hex color like #2563eb to rgba(r,g,b,alpha)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def radar_chart(nilai_kriteria, jurusan_name):
    info = JURUSAN[jurusan_name]
    cats = list(info["kriteria"].keys())
    vals_user = [nilai_kriteria.get(c, 0) for c in cats]
    vals_ideal = [10] * len(cats)

    cats_closed = cats + [cats[0]]
    vals_user_c = vals_user + [vals_user[0]]
    vals_ideal_c = vals_ideal + [vals_ideal[0]]

    fill_color = hex_to_rgba(info["warna"], 0.2)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals_ideal_c, theta=cats_closed,
        fill='toself', name='Ideal',
        line=dict(color='rgba(200,200,200,0.8)', width=1),
        fillcolor='rgba(200,200,200,0.15)'))
    fig.add_trace(go.Scatterpolar(r=vals_user_c, theta=cats_closed,
        fill='toself', name='Kamu',
        line=dict(color=info["warna"], width=2.5),
        fillcolor=fill_color))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True, height=320,
        margin=dict(l=40, r=40, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def bar_comparison(skor_dict):
    df = pd.DataFrame({
        "Jurusan": list(skor_dict.keys()),
        "Kecocokan (%)": list(skor_dict.values()),
    }).sort_values("Kecocokan (%)", ascending=True)
    warna_map = {n: JURUSAN[n]["warna"] for n in JURUSAN}
    fig = px.bar(df, x="Kecocokan (%)", y="Jurusan", orientation='h',
                 color="Jurusan", color_discrete_map=warna_map,
                 text="Kecocokan (%)")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        showlegend=False, height=280,
        xaxis=dict(range=[0, 110], title=""),
        yaxis=dict(title=""),
        margin=dict(l=10, r=60, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Panduan Penggunaan")
    for i, step in enumerate([
        "Isi data diri kamu",
        "Nilai minat & kemampuan",
        "Pilih mata pelajaran favorit",
        "Klik **Analisis** dan lihat hasilnya",
    ], 1):
        st.markdown(f"""
        <div class="step-box" style="margin-bottom:8px;">
            <div class="step-num">{i}</div>
            <div style="font-size:0.85rem;color:#475569;">{step}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏛️ Jurusan Tersedia")
    for nama, info in JURUSAN.items():
        st.markdown(f"""
        <div style="background:white;border-left:4px solid {info['warna']};
             padding:8px 12px;border-radius:6px;margin:4px 0;font-size:0.85rem;">
            <b>{nama}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2025 Sistem Analisis Jurusan Politeknik")

# ─── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎓 Analisis Kecocokan Jurusan Politeknik</h1>
    <p>Temukan jurusan yang paling sesuai dengan minat, kemampuan, dan kepribadianmu</p>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: Data Diri ──────────────────────────────────────────────────────────
st.markdown("### 👤 Data Diri")
col1, col2, col3 = st.columns(3)
with col1:
    nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama kamu...")
with col2:
    asal_sekolah = st.text_input("Asal Sekolah", placeholder="SMA/SMK/MA...")
with col3:
    jurusan_asal = st.selectbox("Jurusan Asal", [
        "IPA", "IPS", "Bahasa", "SMK Teknik",
        "SMK Bisnis & Manajemen", "SMK Lainnya", "Lainnya"
    ])

# ── STEP 2: Nilai Kriteria ─────────────────────────────────────────────────────
st.markdown("### 🧠 Nilai Minat & Kemampuan")
st.caption("Berikan skor 1 (sangat rendah) hingga 10 (sangat tinggi) untuk setiap aspek berikut.")

nilai_kriteria = {}
cols = st.columns(2)
for i, kriteria in enumerate(KRITERIA_ALL):
    with cols[i % 2]:
        nilai_kriteria[kriteria] = st.slider(
            kriteria, min_value=1, max_value=10, value=5,
            help=f"Seberapa tinggi {kriteria.lower()} kamu?",
            key=f"slider_{kriteria}"
        )

# ── STEP 3: Minat & Mapel ─────────────────────────────────────────────────────
st.markdown("### 🌟 Minat & Mata Pelajaran Favorit")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Pilih minat kamu (boleh lebih dari satu):**")
    minat_dipilih = []
    minat_cols = st.columns(2)
    for i, m in enumerate(MINAT_LIST):
        with minat_cols[i % 2]:
            if st.checkbox(m, key=f"minat_{i}"):
                minat_dipilih.append(m)

with col_b:
    st.markdown("**Pilih mata pelajaran favorit:**")
    mapel_dipilih = []
    mapel_cols = st.columns(2)
    for i, mp in enumerate(MAPEL_LIST):
        with mapel_cols[i % 2]:
            if st.checkbox(mp, key=f"mapel_{i}"):
                mapel_dipilih.append(mp)

# ── Booster dari minat & mapel ─────────────────────────────────────────────────
MINAT_BOOST = {
    "💼 Bisnis Digital": ["Bisnis & Dagang", "Desain Grafis", "Analisis Data", "Kepemimpinan & Organisasi"],
    "💻 Rekayasa Perangkat Lunak": ["Coding / Pemrograman", "Analisis Data", "Desain Grafis"],
    "⚙️ Rekayasa Elektrikal Mekanik": ["Elektronika / Robotika", "Mesin & Otomotif"],
    "🤝 Relasi Industri": ["Kepemimpinan & Organisasi", "Sosial & Kemanusiaan", "Menulis & Berkomunikasi"],
}

# ── ANALISIS Button ────────────────────────────────────────────────────────────
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analisis = st.button("🔍 Analisis Kecocokan Jurusan Saya")

if analisis:
    if not nama.strip():
        st.warning("⚠️ Harap masukkan nama lengkap kamu terlebih dahulu.")
    else:
        # Hitung skor dasar
        skor = hitung_skor(nilai_kriteria)

        # Terapkan boost dari minat
        for j, boosts in MINAT_BOOST.items():
            overlap = len(set(minat_dipilih) & set(boosts))
            skor[j] = min(100, skor[j] + overlap * 1.5)

        # Boost dari mapel
        for j, info in JURUSAN.items():
            overlap = len(set(mapel_dipilih) & set(info["mata_pelajaran"]))
            skor[j] = min(100, skor[j] + overlap * 1.0)

        # Urutkan
        skor_sorted = dict(sorted(skor.items(), key=lambda x: x[1], reverse=True))
        jurusan_terbaik = list(skor_sorted.keys())[0]

        # ── HASIL UTAMA ────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(f"## 📊 Hasil Analisis untuk **{nama}**")

        # Banner rekomendasi utama
        j_info = JURUSAN[jurusan_terbaik]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{j_info['warna']}22,{j_info['warna']}11);
             border:2px solid {j_info['warna']};border-radius:16px;padding:1.5rem 2rem;
             margin-bottom:1.5rem;text-align:center;">
            <div style="font-size:3rem;">{j_info['icon']}</div>
            <h2 style="color:{j_info['warna']};margin:0.3rem 0;">Jurusan Terbaik Untukmu</h2>
            <h1 style="color:#1e293b;margin:0;">{jurusan_terbaik}</h1>
            <p style="color:#64748b;margin:0.5rem 0 0;">{j_info['deskripsi']}</p>
            <div style="margin-top:1rem;">
                <span style="background:{j_info['warna']};color:white;padding:6px 20px;
                      border-radius:20px;font-weight:700;font-size:1.2rem;">
                    {skor_sorted[jurusan_terbaik]:.1f}% Kecocokan
                </span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Grafik Perbandingan ────────────────────────────────────────────────
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            st.markdown("#### 📈 Perbandingan Kecocokan")
            st.plotly_chart(bar_comparison(skor_sorted), use_container_width=True)

        with col_g2:
            st.markdown(f"#### 🕸️ Profil Kemampuan — {jurusan_terbaik}")
            st.plotly_chart(radar_chart(nilai_kriteria, jurusan_terbaik), use_container_width=True)

        # ── Daftar semua jurusan ───────────────────────────────────────────────
        st.markdown("### 📋 Detail Kecocokan Semua Jurusan")
        for rank, (j_name, skor_val) in enumerate(skor_sorted.items(), 1):
            level, badge_cls, label = level_warna(skor_val)
            info = JURUSAN[j_name]
            with st.expander(f"{'🥇' if rank==1 else '🥈' if rank==2 else '🥉' if rank==3 else '4️⃣'} #{rank} {j_name} — {skor_val:.1f}%", expanded=(rank == 1)):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"""
                    <div class="result-card result-{level}">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
                            <div>
                                <span style="font-size:1.8rem;">{info['icon']}</span>
                                <span style="font-size:1.1rem;font-weight:700;color:#1e293b;margin-left:0.5rem;">{j_name}</span>
                            </div>
                            <span class="score-badge {badge_cls}">{skor_val:.1f}% — {label}</span>
                        </div>
                        <p style="color:#475569;margin:0 0 0.8rem;">{info['deskripsi']}</p>
                        <div><b>Prospek Karier:</b><br>
                        {"".join(f'<span class="chip">💼 {p}</span>' for p in info["prospek"])}
                        </div>
                        <div style="margin-top:0.8rem;"><b>Mata Pelajaran Pendukung:</b><br>
                        {"".join(f'<span class="chip">📚 {mp}</span>' for mp in info["mata_pelajaran"])}
                        </div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.plotly_chart(radar_chart(nilai_kriteria, j_name), use_container_width=True)

        # ── Rekomendasi Personal ───────────────────────────────────────────────
        st.markdown("### 💡 Rekomendasi Personal")
        tips_col1, tips_col2 = st.columns(2)
        with tips_col1:
            st.markdown(f"""
            <div class="section-card">
                <h4>✅ Kekuatan Kamu</h4>
                <ul>
                {"".join(f"<li><b>{k}</b>: {v}/10</li>" for k, v in sorted(nilai_kriteria.items(), key=lambda x: -x[1])[:4])}
                </ul>
            </div>""", unsafe_allow_html=True)
        with tips_col2:
            st.markdown(f"""
            <div class="section-card">
                <h4>📈 Area Pengembangan</h4>
                <ul>
                {"".join(f"<li><b>{k}</b>: {v}/10 → tingkatkan</li>" for k, v in sorted(nilai_kriteria.items(), key=lambda x: x[1])[:4])}
                </ul>
            </div>""", unsafe_allow_html=True)

        # ── Minat & Mapel dipilih ─────────────────────────────────────────────
        if minat_dipilih or mapel_dipilih:
            st.markdown("""<div class="section-card">
                <h4>🌟 Profil Pilihan Kamu</h4>""", unsafe_allow_html=True)
            if minat_dipilih:
                st.markdown("**Minat:** " + " ".join(f'<span class="chip">{m}</span>' for m in minat_dipilih), unsafe_allow_html=True)
            if mapel_dipilih:
                st.markdown("**Mapel Favorit:** " + " ".join(f'<span class="chip">{mp}</span>' for mp in mapel_dipilih), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.success(f"✅ Analisis selesai! Berdasarkan profil kamu, **{jurusan_terbaik}** adalah jurusan yang paling direkomendasikan.")
        st.balloons()

else:
    # ── Placeholder sebelum analisis ──────────────────────────────────────────
    st.markdown("### 🏛️ Tentang Jurusan")
    cols = st.columns(4)
    for i, (j_name, info) in enumerate(JURUSAN.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background:white;border:2px solid {info['warna']}44;border-top:4px solid {info['warna']};
                 border-radius:12px;padding:1.2rem;text-align:center;height:100%;">
                <div style="font-size:2.5rem;">{info['icon']}</div>
                <h4 style="color:{info['warna']};margin:0.5rem 0;font-size:0.95rem;">{j_name}</h4>
                <p style="font-size:0.8rem;color:#64748b;margin:0 0 0.8rem;">{info['deskripsi']}</p>
                <hr style="border-color:{info['warna']}33;">
                <p style="font-size:0.78rem;font-weight:600;color:#374151;">Prospek Karier:</p>
                {"".join(f'<div style="font-size:0.75rem;color:#475569;">• {p}</div>' for p in info["prospek"][:3])}
            </div>""", unsafe_allow_html=True)
    st.info("👆 Silakan isi form di atas dan klik **Analisis Kecocokan Jurusan Saya** untuk melihat hasilnya!")
