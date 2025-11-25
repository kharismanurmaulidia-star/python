import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Fungsi Generasi Grafik ---

def plot_trigonometry(func_type, A, B, C, D):
    """
    Menghasilkan data dan plot fungsi trigonometri:
    y = A * f(B * (x + C)) + D
    """
    
    # Membuat rentang nilai x
    x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    
    # Menghitung nilai y berdasarkan fungsi yang dipilih
    if func_type == 'Sinus':
        y_original = np.sin(x)
        y_transformed = A * np.sin(B * (x + C)) + D
        formula = f"y = {A} sin({B} (x + {C:.2f})) + {D}"
    elif func_type == 'Kosinus':
        y_original = np.cos(x)
        y_transformed = A * np.cos(B * (x + C)) + D
        formula = f"y = {A} cos({B} (x + {C:.2f})) + {D}"
    elif func_type == 'Tangen':
        # Tangen memiliki asimtot, kita perlu rentang x yang berbeda
        x_tan = np.linspace(-1.5 * np.pi, 1.5 * np.pi, 500)
        y_original = np.tan(x_tan)
        y_transformed = A * np.tan(B * (x_tan + C)) + D
        formula = f"y = {A} tan({B} (x + {C:.2f})) + {D}"
        x = x_tan # Gunakan rentang x yang disesuaikan

    # --- Plotting dengan Matplotlib ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot fungsi standar (sebagai referensi)
    ax.plot(x, y_original, 'k--', alpha=0.5, label=f"y = {func_type.lower()}(x)")

    # Plot fungsi hasil transformasi
    ax.plot(x, y_transformed, 'r-', linewidth=3, label=f"Hasil Transformasi")
    
    # Batas dan Sumbu
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.7)

    # Label sumbu x dalam radian
    pi_ticks = [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi]
    pi_labels = ['-2π', '-π', '0', 'π', '2π']
    ax.set_xticks(pi_ticks)
    ax.set_xticklabels(pi_labels)
    
    # Batas y disesuaikan
    y_limit = max(abs(A) + abs(D) + 1, 5)
    if func_type != 'Tangen':
        ax.set_ylim(-y_limit, y_limit)
        
    ax.legend()
    ax.set_title(f'Grafik {func_type} Terubah: {formula}', fontsize=16)
    ax.set_xlabel('Nilai x (radian)')
    ax.set_ylabel('Nilai y')
    
    st.pyplot(fig)
    return formula

# --- Aplikasi Streamlit Utama ---

st.title("🔬 Virtual Lab Fungsi Trigonometri")
st.markdown("Eksplorasi interaktif bagaimana perubahan parameter memengaruhi grafik **Sinus, Kosinus, dan Tangen**.")

st.markdown("---")

# 1. Pilih Fungsi
st.header("1. Pilih Jenis Fungsi")
func_type = st.selectbox(
    "Pilih Fungsi Dasar:",
    ('Sinus', 'Kosinus', 'Tangen')
)

# 2. Pengaturan Parameter
st.header("2. Atur Parameter (A, B, C, D)")
st.subheader(f"Bentuk Umum: $y = A \cdot f(B(x + C)) + D$")

st.markdown("---")

col_A, col_B = st.columns(2)

with col_A:
    st.markdown("### Parameter A (Amplitudo)")
    A = st.slider(
        "Amplitudo (A): Mengubah tinggi gelombang.", 
        min_value=-5.0, max_value=5.0, value=1.0, step=0.1
    )
    if A > 1:
        st.info("💡 A > 1: Grafik **diregangkan** secara vertikal.")
    elif 0 < A < 1:
        st.info("💡 0 < A < 1: Grafik **ditekan** secara vertikal.")
    elif A < 0:
        st.info("💡 A < 0: Grafik mengalami **refleksi** terhadap sumbu x.")


with col_B:
    st.markdown("### Parameter B (Periode)")
    B = st.slider(
        "Faktor B: Mempengaruhi periode (lebar) gelombang.", 
        min_value=0.1, max_value=4.0, value=1.0, step=0.1
    )
    
    if func_type != 'Tangen':
        periode_baru = abs(2 * np.pi / B)
        st.metric(label="Periode Baru", value=f"{periode_baru:.2f} (≈ {periode_baru/np.pi:.2f}π)")
    else:
        periode_baru = abs(np.pi / B)
        st.metric(label="Periode Baru", value=f"{periode_baru:.2f} (≈ {periode_baru/np.pi:.2f}π)")

    if B > 1:
        st.info("💡 B > 1: Grafik **ditekan** secara horizontal (periode lebih pendek).")
    elif 0 < B < 1:
        st.info("💡 0 < B < 1: Grafik **diregangkan** secara horizontal (periode lebih panjang).")
        
st.markdown("---")
        
col_C, col_D = st.columns(2)

with col_C:
    st.markdown("### Parameter C (Pergeseran Fase)")
    C = st.slider(
        "Pergeseran Fase (C): Menggeser gelombang horizontal.", 
        min_value=-np.pi, max_value=np.pi, value=0.0, step=0.1
    )
    if C > 0.01:
        st.info("💡 C > 0: Grafik bergeser **ke kiri** sejauh C.")
    elif C < -0.01:
        st.info("💡 C < 0: Grafik bergeser **ke kanan** sejauh |C|.")

with col_D:
    st.markdown("### Parameter D (Pergeseran Vertikal)")
    D = st.slider(
        "Pergeseran Vertikal (D): Menggeser garis tengah.", 
        min_value=-3.0, max_value=3.0, value=0.0, step=0.1
    )
    st.metric(label="Garis Tengah Baru", value=f"y = {D}")
    if D != 0:
        st.info(f"💡 D ≠ 0: Grafik bergeser vertikal sejauh {D}.")

st.markdown("---")

# 3. Visualisasi
st.header("📊 Visualisasi Grafik")


# Panggil fungsi plotting
final_formula = plot_trigonometry(func_type, A, B, C, D)

st.subheader("Rumus Hasil")
st.latex(final_formula.replace("sin", r"\sin").replace("cos", r"\cos").replace("tan", r"\tan"))

# Penjelasan Tambahan
st.subheader("📚 Kesimpulan Eksplorasi")
st.markdown(f"""
Dengan menggunakan slider di atas, Anda telah mempraktikkan konsep:
* **Amplitudo (A):** Jarak maksimum vertikal dari garis tengah ke puncak gelombang. $A = |A|$.
* **Periode:** Panjang satu siklus lengkap gelombang. Diperoleh dari $\\frac{{2\pi}}{|B|}$ (untuk Sinus dan Kosinus) atau $\\frac{{\pi}}{|B|}$ (untuk Tangen).
* **Pergeseran Fase (C):** Pergeseran horizontal. Positif berarti bergeser ke kiri, Negatif berarti bergeser ke kanan.
* **Garis Tengah (D):** Garis horizontal $y=D$ yang membagi gelombang secara simetris.
""")
