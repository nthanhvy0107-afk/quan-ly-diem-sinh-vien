import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Cấu hình trang web ---
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên - Modern Pastel",
    page_icon="🌸",
    layout="wide"
)

# --- 2. Tùy chỉnh CSS phối màu Hồng Pastel + Xám Khói + Xanh Mint (Cute, hiện đại, không sến) ---
st.markdown("""
    <style>
    /* Nền tổng thể: Hồng pastel cực nhạt, nhẹ nhàng */
    .stApp {
        background-color: #FFF5F7;
        color: #2D3748;
    }
    /* Tiêu đề chính: Hồng đậm vừa phải, sang trọng */
    h1 {
        color: #DB2777;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    /* Các tiêu đề phụ */
    h2, h3 {
        color: #BE185D;
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar: Hồng pastel ấm áp */
    [data-testid="stSidebar"] {
        background-color: #FDE8EC;
        border-right: 1px solid #FBCFE8;
    }
    /* Các khung thông báo (Success, Info...) mang màu Xanh Mint và Hồng nhạt */
    .stSuccess {
        background-color: #D1FAE5 !important;
        color: #065F46 !important;
        border-left: 4px solid #10B981;
    }
    .stInfo {
        background-color: #FCE7F3 !important;
        color: #831843 !important;
        border-left: 4px solid #EC4899;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Dữ liệu và tính toán điểm ---
data = {
    'Ho_ten': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyen_can': [8.0, 9.0, 7.0, 8.5, 7.5, 6.0, 9.0, 7.0, 8.0, 9.5],
    'Giua_ky': [7.5, 8.0, 6.5, 9.0, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuoi_ky': [8.0, 8.5, 7.0, 9.5, 7.5, 6.5, 8.5, 7.5, 7.5, 9.0]
}
df = pd.DataFrame(data)

# Tính điểm tổng kết
df['Tong_ket'] = (0.2 * df['Chuyen_can']) + (0.3 * df['Giua_ky']) + (0.5 * df['Cuoi_ky'])

# Hàm xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi 🌟'
    elif diem >= 7.0:
        return 'Khá 👍'
    elif diem >= 5.0:
        return 'Trung bình 📚'
    else:
        return 'Yếu ⚠️'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# --- 4. THANH BÊN (SIDEBAR) - THÔNG TIN TÁC GIẢ ---
st.sidebar.title("✨ Bảng Điều Khiển")
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Thông tin tác giả")
st.sidebar.info(
    "💖 **Họ tên:** [Họ và tên của bạn]\n\n"
    "🎓 **MSSV:** [MSSV của bạn]\n\n"
    "🏫 **Lớp:** [Tên lớp của bạn]"
)
st.sidebar.markdown("---")
st.sidebar.write("💡 *Ứng dụng quản lý điểm học tập sinh viên phong cách Pastel hiện đại.*")

# --- 5. GIAO DIỆN CHÍNH ---
st.title("🌸 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("<p align='center' style='color: #4A5568; font-size: 16px;'>Hệ thống trực quan hóa điểm số, thống kê và tra cứu thông tin học tập</p>", unsafe_allow_html=True)
st.markdown("---")

# Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# Thống kê chung
st.subheader("📊 Thống kê tổng quan lớp học")
diem_tb_lop = df['Tong_ket'].mean()
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

col1, col2 = st.columns(2)
with col1:
    st.success(f"📈 **Điểm tổng kết trung bình lớp:** {diem_tb_lop:.2f}")
    st.success(f"✨ **Số sinh viên đạt (>= 5.0):** {so_sv_dat} / 10 sinh viên")
with col2:
    st.info(f"🏆 **Điểm cao nhất:** {max_sv['Ho_ten']} ({max_sv['Tong_ket']:.2f} điểm)")
    st.info(f"📌 **Điểm thấp nhất:** {min_sv['Ho_ten']} ({min_sv['Tong_ket']:.2f} điểm)")

# Tra cứu sinh viên bằng Selectbox
st.subheader("🔍 Tra cứu chi tiết cá nhân")
selected_student = st.selectbox("✨ Chọn tên sinh viên để xem chi tiết:", df['Ho_ten'])

student_info = df[df['Ho_ten'] == selected_student].iloc[0]

# Hiển thị kết quả tra cứu dạng box nổi bật
st.markdown(f"""
<div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #FBCFE8;">
    <h4 style="color: #DB2777; margin-top: 0;">💌 Thông tin học tập của: {student_info['Ho_ten']}</h4>
    <ul style="list-style-type: none; padding-left: 0; color: #2D3748; font-size: 15px;">
        <li>🎒 <b>Điểm Chuyên cần:</b> {student_info['Chuyen_can']}</li>
        <li>📝 <b>Điểm Giữa kỳ:</b> {student_info['Giua_ky']}</li>
        <li>📖 <b>Điểm Cuối kỳ:</b> {student_info['Cuoi_ky']}</li>
        <li>✨ <b>Điểm Tổng kết:</b> <b>{student_info['Tong_ket']:.2f}</b></li>
        <li>🎀 <b>Xếp loại:</b> <b>{student_info['Xep_loai']}</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Biểu đồ cột ngang phối màu Hồng Pastel + Xanh Mint
st.subheader("📈 Biểu đồ cột điểm tổng kết của lớp")
fig, ax = plt.subplots(figsize=(9, 5))

# Dùng màu hồng pastel pha ánh tím nhẹ kết hợp viền xanh mint hiện đại
bars = ax.barh(df['Ho_ten'], df['Tong_ket'], color='#F472B6', edgecolor='#10B981', linewidth=1.2)

ax.set_xlabel('Điểm tổng kết', color='#4A5568', fontweight='bold', fontsize=11)
ax.set_ylabel('Họ và tên sinh viên', color='#4A5568', fontweight='bold', fontsize=11)
ax.set_xlim(0, 10)
ax.invert_yaxis() # Đảo chiều để sinh viên 'An' đứng đầu tiên

# Ghi chú giá trị điểm lên đầu mỗi cột
for i, v in enumerate(df['Tong_ket']):
    ax.text(v + 0.15, i, f"{v:.2f}", va='center', fontsize=10, color='#374151', fontweight='bold')

# Phối màu nền cho khung biểu đồ khớp với web
fig.patch.set_facecolor('#FFF5F7')
ax.set_facecolor('#FFF5F7')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
ax.spines['bottom'].set_color('#CBD5E1')

st.pyplot(fig)

# --- 6. FOOTER CUỐI TRANG ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6B7280; font-size: 13px;'>"
    "🌸 Developed with 💖 by <b>[Nguyễn Thanh Vy]</b> 🌸"
    "</p>", 
    unsafe_allow_html=True
)
