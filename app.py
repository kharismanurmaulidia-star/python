import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Fungsi Transformasi Geometri ---

def translate(points, tx, ty):
    """Melakukan Translasi pada titik-titik."""
    # Matriks translasi (hanya perlu menambahkan offset ke koordinat)
    return points + np.array([tx, ty])

def rotate(points, angle_deg, cx=0, cy=0):
    """Melakukan Rotasi pada titik-titik di sekitar titik pusat (cx, cy)."""
    angle_rad = np.radians(angle_deg)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    
    # 1. Pindahkan ke pusat (0,0)
    temp_points = points - np.array([cx, cy])
    
    # 2. Lakukan Rotasi
    rotation_matrix = np.array([
        [c, -s],
        [s,  c]
    ])
    rotated_points = temp_points @ rotation_matrix.T
    
    # 3. Pindahkan kembali
    return rotated_points + np.array([cx, cy])

def reflect(points, axis):
    """Melakukan Refleksi (terhadap sumbu x atau y)."""
    if axis == 'Sumbu X (y=0)':
        # Matriks refleksi terhadap sumbu x: [[1, 0], [0, -1]]
        reflection_matrix = np.array([[1, 0], [0, -1]])
    elif axis == 'Sumbu Y (x=0)':
        # Matriks refleksi terhadap sumbu y: [[-1, 0], [0, 1]]
        reflection_matrix = np.array([[-1, 0], [0, 1]])
    elif axis == 'Garis y=x':
        # Matriks refleksi terhadap y=x: [[0, 1], [1, 0]]
        reflection_matrix = np.array([[0, 1], [1, 0]])
    elif axis == 'Garis y=-x':
        # Matriks refleksi terhadap y=-x: [[0, -1], [-1, 0]]
        reflection_matrix = np.array([[0, -1], [-1, 0]])
    else:
        return points # Refleksi tidak dikenali

    return points @ reflection_matrix.T

def dilate(points, kx, ky, cx=0, cy=0):
    """Melakukan Dilatasi pada titik-titik di sekitar titik pusat (cx, cy)."""
    # 1. Pindahkan ke pusat (0,0)
    temp_points = points - np.array([cx, cy])
    
    # 2. Lakukan Dilatasi
    dilation_matrix = np.array([
        [kx, 0],
        [0,  ky]
    ])
    dilated_points = temp_points @ dilation_matrix.T
    
    # 3. Pindahkan kembali
    return dilated_points + np.array([cx, cy])

# --- Fungsi Plotting ---

def plot_transformation(original, transformed, title, transformation_name):
    """Membuat plot interaktif menggunakan Matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Batas plot
    all_points = np.vstack([original, transformed])
    min_val = np.min(all_points) - 2
    max_val = np.max(all_points) + 2
    
    # Pastikan batas simetris
    limit = max(abs(min_val), abs(max_val), 10)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    # Sumbu koordinat
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Plot Titik atau Poligon Awal
    if len(original) == 1: # Titik tunggal
        ax.plot(original[0, 0], original[0, 1], 'bo', label='Titik Awal', markersize=10)
        ax.text(original[0, 0], original[0, 1] + 0.5, f'A({original[0, 0]:.1f}, {original[0, 1]:.1f})', color='b')
    else: # Poligon
        original_closed = np.vstack([original, original[0]])
        ax.plot(original_closed[:, 0], original_closed[:, 1], 'b-', marker='o', label='Bentuk Awal')
        
    # Plot Titik atau Poligon Hasil Transformasi
    if len(transformed) == 1: # Titik tunggal
        ax.plot(transformed[0, 0], transformed[0, 1], 'rX', label='Hasil Transformasi', markersize=10)
        ax.text(transformed[0, 0], transformed[0, 1] + 0.5, f"A'({transformed[0, 0]:.1f}, {transformed[0, 1]:.1f})", color='r')
        
        # Garis bantu (jika hanya 1 titik)
        ax.plot([original[0, 0], transformed[0, 0]], [original[0, 1], transformed[0, 1]], 'k--', alpha=0.5)
    else: # Poligon
        transformed_closed = np.vstack([transformed, transformed[0]])
        ax.plot(transformed_closed[:, 0], transformed_closed[:, 1], 'r--', marker='x', label='Hasil Transformasi')
        
    ax.set_title(f'Visualisasi {transformation_name}', fontsize=16)
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.set_aspect('equal', adjustable='box')
    ax.legend()
    
    st.pyplot(fig)

# --- Aplikasi Streamlit Utama ---

st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Eksplorasi interaktif **Translasi, Rotasi, Refleksi, dan Dilatasi**.")
st.markdown("---")

# 1. Input Titik Awal/Poligon
st.sidebar.header("Input Titik/Bentuk Awal")
coord_input = st.sidebar.text_area(
    "Masukkan koordinat awal (x, y) per baris:", 
    value="2, 3\n5, 3\n5, 6",
    help="Contoh: 2, 3 (untuk titik) atau 2, 3\\n5, 3\\n5, 6 (untuk segitiga)"
)

try:
    # Parsing input koordinat
    coords_list = []
    for line in coord_input.strip().split('\n'):
        if line.strip():
            x, y = map(float, line.split(','))
            coords_list.append([x, y])
            
    if not coords_list:
        st.error("Input koordinat tidak valid. Harap masukkan setidaknya satu koordinat (x, y).")
        st.stop()
        
    original_points = np.array(coords_list)
    
    st.sidebar.markdown(f"**Bentuk Awal:** {len(coords_list)} Titik")

except ValueError:
    st.error("Format input koordinat salah. Pastikan formatnya adalah 'x, y' per baris.")
    st.stop()

# 2. Pilihan Transformasi
st.header("Pilih Jenis Transformasi")
transformation_type = st.radio(
    "Pilih jenis transformasi yang ingin diuji:",
    ('Translasi', 'Rotasi', 'Refleksi', 'Dilatasi')
)

st.markdown("---")

transformed_points = original_points
explanation = ""
transformation_name = ""

# --- Logika Berdasarkan Pilihan Transformasi ---

if transformation_type == 'Translasi':
    st.subheader("➡️ Pengaturan Translasi (Pergeseran)")
    col1, col2 = st.columns(2)
    tx = col1.slider("Pergeseran pada Sumbu X ($T_x$)", -10.0, 10.0, 3.0, 0.1)
    ty = col2.slider("Pergeseran pada Sumbu Y ($T_y$)", -10.0, 10.0, -2.0, 0.1)
    
    transformed_points = translate(original_points, tx, ty)
    transformation_name = f"Translasi $T=({tx:.1f}, {ty:.1f})$"
    
    explanation = (
        "**Translasi** memindahkan setiap titik sejauh jarak tertentu dalam arah yang sama. "
        f"Setiap titik $(x, y)$ menjadi $(x+{tx:.1f}, y+{ty:.1f})$. "
        "Bentuk dan ukuran objek **tidak berubah**."
    )

elif transformation_type == 'Rotasi':
    st.subheader("🔄 Pengaturan Rotasi (Perputaran)")
    col1, col2 = st.columns(2)
    angle = col1.slider("Sudut Rotasi (derajat)", -360, 360, 90)
    
    st.markdown("**Pusat Rotasi (P)**")
    col3, col4 = st.columns(2)
    cx = col3.number_input("Pusat X ($C_x$)", value=0.0)
    cy = col4.number_input("Pusat Y ($C_y$)", value=0.0)
    
    transformed_points = rotate(original_points, angle, cx, cy)
    transformation_name = f"Rotasi ${angle}°$ di sekitar P({cx:.1f}, {cy:.1f})"
    
    explanation = (
        "**Rotasi** memutar setiap titik objek di sekitar titik pusat ($P$) dengan sudut tertentu. "
        "Rotasi positif berlawanan arah jarum jam. "
        "Bentuk, ukuran, dan jarak ke pusat rotasi **tidak berubah**."
    )

elif transformation_type == 'Refleksi':
    st.subheader("↔️ Pengaturan Refleksi (Pencerminan)")
    axis = st.selectbox(
        "Pilih Garis Cermin (Sumbu Refleksi):",
        ('Sumbu X (y=0)', 'Sumbu Y (x=0)', 'Garis y=x', 'Garis y=-x')
    )
    
    transformed_points = reflect(original_points, axis)
    transformation_name = f"Refleksi terhadap {axis}"
    
    explanation = (
        "**Refleksi** menghasilkan bayangan cermin dari objek terhadap garis tertentu (sumbu refleksi). "
        "Setiap titik pada objek memiliki jarak yang sama ke garis cermin dengan titik bayangannya. "
        "Bentuk dan ukuran objek **tidak berubah**, tetapi orientasi menjadi terbalik."
    )

elif transformation_type == 'Dilatasi':
    st.subheader("🔎 Pengaturan Dilatasi (Perkalian)")
    col1, col2 = st.columns(2)
    kx = col1.slider("Faktor Skala X ($k_x$)", -5.0, 5.0, 1.5, 0.1)
    ky = col2.slider("Faktor Skala Y ($k_y$)", -5.0, 5.0, 1.5, 0.1)
    
    st.markdown("**Pusat Dilatasi (P)**")
    col3, col4 = st.columns(2)
    cx = col3.number_input("Pusat X ($C_x$)", value=0.0)
    cy = col4.number_input("Pusat Y ($C_y$)", value=0.0)
    
    transformed_points = dilate(original_points, kx, ky, cx, cy)
    transformation_name = f"Dilatasi $k=({kx:.1f}, {ky:.1f})$ di sekitar P({cx:.1f}, {cy:.1f})"
    
    explanation = (
        "**Dilatasi** mengubah ukuran objek berdasarkan faktor skala ($k$) dari titik pusat ($P$). "
        "Jika $|k| > 1$, objek diperbesar. Jika $0 < |k| < 1$, objek diperkecil. "
        "Jika $k$ negatif, objek diperbesar/diperkecil dan juga direfleksikan melalui pusat $P$."
    )

# --- Visualisasi dan Hasil ---

st.header("📊 Visualisasi Hasil Transformasi")

col_plot, col_res = st.columns([2, 1])

with col_plot:
    plot_transformation(original_points, transformed_points, transformation_name, transformation_type)
    

[Image of geometric transformation translation rotation reflection dilation on a Cartesian plane]
with col_res:
    st.subheader("📚 Hasil & Rumus")
    
    st.markdown("**Koordinat Awal:**")
    for i, p in enumerate(original_points):
        st.write(f"Titik {i+1}: $A_{i+1}({p[0]:.1f}, {p[1]:.1f})$")
        
    st.markdown("**Koordinat Hasil Transformasi:**")
    for i, p in enumerate(transformed_points):
        st.write(f"Titik {i+1}': $A'_{i+1}({p[0]:.1f}, {p[1]:.1f})$")
        
    st.markdown("---")
    st.subheader("💡 Konsep Transformasi")
    st.markdown(explanation)
    
    # Menampilkan Matriks Transformasi (opsional - untuk tingkat lanjut)
    # st.subheader("Matriks Transformasi")
    # if transformation_type == 'Rotasi':
    #     angle_rad = np.radians(angle)
    #     c = np.cos(angle_rad)
    #     s = np.sin(angle_rad)
    #     st.latex(f"R = \\begin{{pmatrix}} {c:.2f} & {-s:.2f} \\\\ {s:.2f} & {c:.2f} \\end{{pmatrix}}")
    # ...

# --- Penutup ---
st.markdown("---")
st.info("Eksplorasi setiap jenis transformasi dengan mengubah parameter masukan. Amati bagaimana bentuk awal (biru) berubah menjadi bentuk hasil (merah)!")
