import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Dữ liệu và tính toán ban đầu
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
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# --- 2. Giao diện Web App trên Streamlit ---

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm
st.subheader("Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df)

# Các thông tin thống kê
st.subheader("Thống kê chung")
diem_tb_lop = df['Tong_ket'].mean()
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

st.write(f"- **Điểm tổng kết trung bình của lớp:** {diem_tb_lop:.2f}")
st.write(f"- **Sinh viên có điểm tổng kết cao nhất:** {max_sv['Ho_ten']} ({max_sv['Tong_ket']:.2f})")
st.write(f"- **Sinh viên có điểm tổng kết thấp nhất:** {min_sv['Ho_ten']} ({min_sv['Tong_ket']:.2f})")
st.write(f"- **Số sinh viên đạt (>= 5.0 điểm):** {so_sv_dat}")

# Danh sách xổ xuống chọn sinh viên
st.subheader("Tra cứu thông tin theo sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên cần xem:", df['Ho_ten'])

# Lọc dữ liệu sinh viên được chọn
student_info = df[df['Ho_ten'] == selected_student].iloc[0]

st.info(f"Thông tin chi tiết của **{student_info['Ho_ten']}**:")
st.write(f"- Điểm Chuyên cần: {student_info['Chuyen_can']}")
st.write(f"- Điểm Giữa kỳ: {student_info['Giua_ky']}")
st.write(f"- Điểm Cuối kỳ: {student_info['Cuoi_ky']}")
st.write(f"- Điểm Tổng kết: **{student_info['Tong_ket']:.2f}**")
st.write(f"- Xếp loại: **{student_info['Xep_loai']}**")

# Biểu đồ cột ngang
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df['Ho_ten'], df['Tong_ket'], color='skyblue', edgecolor='blue')
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Họ và tên sinh viên')
ax.set_xlim(0, 10)
ax.invert_yaxis() # Đảo ngược để tên An ở trên cùng

# Hiển thị số điểm lên cột
for i, v in enumerate(df['Tong_ket']):
    ax.text(v + 0.1, i, f"{v:.2f}", va='center', fontsize=9)

st.pyplot(fig)

# Footer: Họ tên và MSSV chữ nhỏ ở cuối trang
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>"
    "Người tạo ứng dụng: [Họ tên của bạn] - [MSSV của bạn]"
    "</p>", 
    unsafe_allow_html=True
)