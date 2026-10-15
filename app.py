import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Cấu hình trang web ---
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên",
    page_icon="🌸",
    layout="wide"
)

# --- 2. Tùy chỉnh CSS (Hồng pastel + Xám khói + Xanh mint) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF5F7;
        color: #2D3748;
    }
    h1 {
        color: #DB2777;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        color: #BE185D;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #FDE8EC;
        border-right: 1px solid #FBCFE8;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Hàm xử lý tính toán và xếp loại (Đã bỏ icon) ---
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

# Khởi tạo dữ liệu ban đầu vào Session State
if 'df' not in st.session_state:
    data = {
        'Ho_ten': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
        'Chuyen_can': [8.0, 9.0, 7.0, 8.5, 7.5, 6.0, 9.0, 7.0, 8.0, 9.5],
        'Giua_ky': [7.5, 8.0, 6.5, 9.0, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
        'Cuoi_ky': [8.0, 8.5, 7.0, 9.5, 7.5, 6.5, 8.5, 7.5, 7.5, 9.0]
    }
    df_init = pd.DataFrame(data)
    df_init['Tong_ket'] = (0.2 * df_init['Chuyen_can']) + (0.3 * df_init['Giua_ky']) + (0.5 * df_init['Cuoi_ky'])
    df_init['Xep_loai'] = df_init['Tong_ket'].apply(xep_loai)
    st.session_state['df'] = df_init

df = st.session_state['df']

# --- 4. THANH BÊN (SIDEBAR) ---
st.sidebar.title("✨ Menu Điều Hướng")
st.sidebar.markdown("---")

# Tác giả
st.sidebar.subheader("👤 Thông tin tác giả")
st.sidebar.info(
    "**Họ tên:** [Nguyễn Thanh Vy]\n\n"
    "**MSSV:** [068308007084]\n\n"
)
st.sidebar.markdown("---")

# Form thêm sinh viên mới trực tiếp trên web
st.sidebar.subheader("➕ Thêm sinh viên mới")
with st.sidebar.form("add_student_form"):
    new_name = st.text_input("Họ tên sinh viên:")
    new_cc = st.number_input("Điểm Chuyên cần:", 0.0, 10.0, 8.0)
    new_gk = st.number_input("Điểm Giữa kỳ:", 0.0, 10.0, 7.5)
    new_ck = st.number_input("Điểm Cuối kỳ:", 0.0, 10.0, 8.0)
    
    submit_btn = st.form_submit_button("Thêm vào danh sách")
    if submit_btn:
        if new_name.strip() != "":
            tong_ket_moi = (0.2 * new_cc) + (0.3 * new_gk) + (0.5 * new_ck)
            xep_loai_moi = xep_loai(tong_ket_moi)
            new_row = pd.DataFrame({
                'Ho_ten': [new_name],
                'Chuyen_can': [new_cc],
                'Giua_ky': [new_gk],
                'Cuoi_ky': [new_ck],
                'Tong_ket': [tong_ket_moi],
                'Xep_loai': [xep_loai_moi]
            })
            st.session_state['df'] = pd.concat([st.session_state['df'], new_row], ignore_index=True)
            st.sidebar.success(f"Đã thêm sinh viên {new_name} thành công!")
            st.rerun()
        else:
            st.sidebar.error("Vui lòng nhập tên sinh viên!")

# --- 5. GIAO DIỆN CHÍNH ---
st.title("🌸 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("<p align='center' style='color: #4A5568; font-size: 16px;'>Hệ thống quản lý học tập thông minh với biểu đồ trực quan và tương tác trực tiếp</p>", unsafe_allow_html=True)
st.markdown("---")

# Thẻ chỉ số nổi bật (st.metric)
st.subheader("📊 Thống kê tổng quan lớp học")
diem_tb_lop = df['Tong_ket'].mean()
max_row = df.loc[df['Tong_ket'].idxmax()]
min_row = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()
tong_so_sv = len(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng số sinh viên", f"{tong_so_sv} bạn")
col2.metric("Điểm TB của lớp", f"{diem_tb_lop:.2f}")
col3.metric("Sinh viên đạt (>=5đ)", f"{so_sv_dat} bạn")
col4.metric("Điểm cao nhất", f"{max_row['Ho_ten']} ({max_row['Tong_ket']:.2f})")

st.markdown("---")

# Hiển thị bảng điểm đầy đủ
st.subheader("📋 Bảng điểm chi tiết của lớp")
st.dataframe(df, use_container_width=True)

# Tra cứu thông tin cá nhân sinh viên bằng Selectbox
st.subheader("🔎 Tra cứu chi tiết cá nhân")
if len(df) > 0:
    selected_student = st.selectbox("✨ Chọn tên sinh viên để xem chi tiết:", df['Ho_ten'])
    student_info = df[df['Ho_ten'] == selected_student].iloc[0]
    st.markdown(f"""
    <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #FBCFE8;">
        <h4 style="color: #DB2777; margin-top: 0;">💌 Thông tin học tập của: {student_info['Ho_ten']}</h4>
        <ul style="list-style-type: none; padding-left: 0; color: #2D3748; font-size: 15px;">
            <li>🎒 <b>Điểm Chuyên cần:</b> {student_info['Chuyen_can']}</li>
            <li>📝 <b>Điểm Giữa kỳ:</b> {student_info['Giua_ky']}</li>
            <li>📖 <b>Điểm Cuối kỳ:</b> {student_info['Cuoi_ky']}</li>
            <li>✨ <b>Điểm Tổng kết:</b> <b>{student_info['Tong_ket']:.2f}</b></li>
            <li>📋 <b>Xếp loại:</b> <b>{student_info['Xep_loai']}</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Biểu đồ cột ngang
st.subheader("📈 Biểu đồ điểm tổng kết của toàn bộ lớp")
fig, ax = plt.subplots(figsize=(9, max(4, len(df)*0.4)))

bars = ax.barh(df['Ho_ten'], df['Tong_ket'], color='#F472B6', edgecolor='#10B981', linewidth=1.2)
ax.set_xlabel('Điểm tổng kết', color='#4A5568', fontweight='bold', fontsize=11)
ax.set_ylabel('Họ và tên sinh viên', color='#4A5568', fontweight='bold', fontsize=11)
ax.set_xlim(0, 10)
ax.invert_yaxis()

for i, v in enumerate(df['Tong_ket']):
    ax.text(v + 0.15, i, f"{v:.2f}", va='center', fontsize=10, color='#374151', fontweight='bold')

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
