import streamlit as st

def hitung_imt(berat_kg, tinggi_m):
    """Menghitung Indeks Massa Tubuh (IMT)."""
    # Pastikan tinggi tidak nol untuk menghindari error ZeroDivisionError
    if tinggi_m > 0:
        imt = berat_kg / (tinggi_m ** 2)
        return imt
    return 0 # Kembalikan 0 jika tinggi nol

def tentukan_kategori(imt):
    """Menentukan kategori IMT dan warna untuk tampilan."""
    if imt == 0:
        return "Masukkan tinggi yang valid.", "info"
    elif imt < 18.5:
        return "Kurus/Kekurangan berat badan", "warning"
    elif 18.5 <= imt < 25.0:
        return "Normal/Ideal", "success"
    elif 25.0 <= imt < 30.0:
        return "Kelebihan berat badan", "warning"
    else:
        return "Obesitas", "error"

# --- Struktur Aplikasi Streamlit ---

st.title("🧮 Kalkulator Indeks Massa Tubuh (IMT)")
st.caption("Konversi dari aplikasi konsol Python.")

# 1. Mengganti `input()` dengan widget Streamlit
# Menggunakan st.number_input untuk input float (bilangan desimal)

berat = st.number_input(
    "Masukkan berat badan Anda (kg):",
    min_value=1.0, # Batasan minimum berat
    max_value=300.0, # Batasan maksimum berat
    value=65.0, # Nilai default
    step=0.1,
    format="%.1f"
)

tinggi = st.number_input(
    "Masukkan tinggi badan Anda (meter):",
    min_value=0.5, # Batasan minimum tinggi (misalnya 50 cm)
    max_value=2.5, # Batasan maksimum tinggi
    value=1.70, # Nilai default
    step=0.01,
    format="%.2f"
)

# 2. Pemicu Perhitungan (Opsional, tapi bagus untuk kontrol)
if st.button("Hitung IMT dan Kategori"):
    # Panggil fungsi hitung_imt
    hasil_imt = hitung_imt(berat, tinggi)
    
    # Panggil fungsi tentukan_kategori
    kategori, warna = tentukan_kategori(hasil_imt)

    st.markdown("---")
    st.header("✨ Hasil Perhitungan IMT")
    
    # Menampilkan nilai IMT dengan format yang lebih baik
    st.metric(label="Nilai IMT Anda", value=f"{hasil_imt:.2f}")

    # Menampilkan kategori dengan styling Streamlit
    if warna == "success":
        st.success(f"**Kategori:** {kategori}")
    elif warna == "warning":
        st.warning(f"**Kategori:** {kategori}")
    elif warna == "error":
        st.error(f"**Kategori:** {kategori}")
    else:
        st.info(f"**Kategori:** {kategori}")

    # Tambahan: Menampilkan penjelasan standar IMT
    st.markdown("""
    ---
    **Referensi Kategori IMT (WHO/Asia Pasifik):**
    * Kurus: < 18.5
    * Normal/Ideal: 18.5 – 24.9
    * Kelebihan berat badan: 25.0 – 29.9
    * Obesitas: $\\ge$ 30.0
    """)