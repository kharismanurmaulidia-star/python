import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman & Judul ---
st.set_page_config(layout="wide", page_title="Virtual Lab Trigonometri")

st.title("🔬 Virtual Lab: Eksplorasi Fungsi Trigonometri")
st.markdown("""
Eksplorasi interaktif bagaimana perubahan parameter **A, B, C, dan D** memengaruhi grafik 
**Sinus** dan **Kosinus**.

Bentuk umum fungsinya adalah: $$y = A \cdot f(B(x + C)) + D$$
""")
st.markdown("---")

# --- Fungsi Plotting ---

def plot_trigonometry(func_type, A, B, C, D):
    """Menghasilkan data dan plot fungsi trigonometri."""
    
    # Membuat rentang nilai x (dari -2π hingga 2π)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    
    # Menghitung fungsi
    if func_type == 'Sinus':
        y_original = np.sin(x)
        y_transformed = A * np.sin(B * (x + C)) + D
    elif func_type == 'Kosinus':
        y_original = np.cos(x)
        y_transformed = A * np.cos(B * (x + C)) + D
    
    # --- Plotting dengan Matplotlib ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot fungsi standar (Referensi)
    ax.plot(x, y_original, 'k--', alpha=0.5, label=f"y = {func_type.lower()}(x) Standar")

    # Plot fungsi hasil transformasi
    ax.plot(x, y_transformed, 'r-', linewidth=3, label="Hasil Transformasi")
    
    # Garis Tengah (D)
    ax.axhline(D, color='blue', linestyle='-.', alpha=0.7, label=f"Garis Tengah (y={D:.1f})")
    
    # Sumbu koordinat
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.7)

    # Label sumbu x dalam radian
    pi_ticks = [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi]
    pi_labels = ['-2π', '-π', '0', 'π', '2π']
    ax.set_xticks(pi_ticks)
    ax.set_xticklabels(pi_labels)
    
    # Batas y disesuaikan secara dinamis
    y_limit = max(abs(A) + abs(D) + 1, 3)
    ax.set_ylim(-y_limit, y_limit)
        
    ax.legend(loc='upper right')
    ax.set_title(f'Grafik {func_type} Terubah', fontsize=16)
    ax.set_xlabel('Nilai x (radian)')
    ax.set_ylabel('Nilai y')
    
    st.pyplot(fig)
    return

# --- Sidebar (Input Kontrol) ---

st.sidebar.header("Kontrol Fungsi")
func_type = st.sidebar.selectbox(
    "1. Pilih Fungsi Dasar:",
    ('Sinus', 'Kosinus')
)
st.sidebar.markdown("---")

st.sidebar.header("Atur Parameter $A, B, C, D$")

# Amplitudo (A)
A = st.sidebar.slider(
    "A: Amplitudo (Tinggi Gelombang)", 
    min_value=-3.0, max_value=3.0, value=1.0, step=0.1, key='A_val'
)

# Periode (B)
B = st.sidebar.slider(
    "B: Faktor Periode (Lebar Gelombang)", 
    min_value=0.1, max_value=3.0, value=1.0, step=0.1, key='B_val'
)

# Pergeseran Fase (C)
C = st.sidebar.slider(
    "C: Pergeseran Fase (Horizontal)", 
    min_value=-np.pi, max_value=np.pi, value=0.0, step=0.1, key='C_val',
    format="%.2f rad"
)

# Pergeseran Vertikal (D)
D = st.sidebar.slider(
    "D: Pergeseran Vertikal (Garis Tengah)", 
    min_value=-2.0, max_value=2.0, value=0.0, step=0.1, key='D_val'
)

# --- Visualisasi Utama ---

col1, col2 = st.columns([7, 3])

with col1:
    st.subheader("Visualisasi Grafik Fungsi")
    
    # Panggil fungsi plotting
    plot_trigonometry(func_type, A, B, C, D)
    

with col2:
    st.subheader("Analisis Hasil")
    
    # Amplitudo
    st.metric(label="Amplitudo ($|A|$)", value=f"{abs(A):.2f}")
    
    # Periode
    periode = abs(2 * np.pi / B)
    st.metric(label="Periode Baru", value=f"{periode:.2f} (≈ {periode/np.pi:.2f}π)")
    
    # Garis Tengah
    st.metric(label="Garis Tengah (D)", value=f"y = {D:.1f}")
    
    # Pergeseran Fase
    direction = "Kiri" if C > 0.01 else ("Kanan" if C < -0.01 else "Tidak Ada")
    st.metric(label="Pergeseran Fase", value=f"{abs(C):.2f} {direction}")

    st.markdown("---")
    st.subheader("Rumus yang Digambar")
    
    # Membangun string LaTeX yang spesifik dan aman
    func = r"\sin" if func_type == 'Sinus' else r"\cos"
    
    # Menyederhanakan tampilan jika C atau D nol
    term_C = ""
    if abs(C) > 0.01:
        term_C = f" + {C:.2f}"
    
    term_D = ""
    if abs(D) > 0.01:
        term_D = f" + {D:.2f}"
    elif abs(D) < 0.01 and D != 0:
        # Menangani jika D sangat kecil mendekati nol
        term_D = "" 

    rumus = f"y = {A:.2f} {func}\\left({B:.2f} (x {term_C})\\right) {term_D}"
    
    st.latex(rumus)


# --- Penjelasan Konsep (Bawah) ---
st.markdown("---")
st.header("💡 Konsep Dasar Transformasi")

st.markdown("""
Setiap parameter pada fungsi $y = A \cdot f(B(x + C)) + D$ memiliki peran spesifik:
""")

st.subheader("1. Amplitudo ($A$)")
st.markdown(r"""
Mengontrol **tinggi** gelombang. Amplitudo adalah jarak vertikal maksimum dari garis tengah.
* Jika $|A| > 1$, grafik **diregangkan** vertikal.
* Jika $A < 0$, grafik **direfleksikan** terhadap garis tengah.
""")

st.subheader("2. Faktor Periode ($B$)")
st.markdown(r"""
Mengontrol **lebar** gelombang. Periode adalah panjang satu siklus lengkap.
* Periode dihitung dengan $\frac{2\pi}{|B|}$.
* Jika $B > 1$, periode **memendek** (gelombang rapat).
* Jika $B < 1$, periode **memanjang** (gelombang renggang).
""")

st.subheader("3. Pergeseran Fase ($C$)")
st.markdown("""
Mengontrol pergeseran **horizontal** (kiri-kanan).
* $y = f(x+C)$: bergeser **ke KIRI** sejauh $C$ (jika $C>0$).
* $y = f(x-C)$: bergeser **ke KANAN** sejauh $C$ (jika $C>0$ dimasukkan sebagai $-C$).
""")

st.subheader("4. Pergeseran Vertikal ($D$)")
st.markdown("""
Mengontrol pergeseran **garis tengah** (atas-bawah).
* Garis tengah baru adalah $y = D$.
""")
