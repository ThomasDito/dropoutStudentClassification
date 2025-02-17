import streamlit as st
import numpy as np
import joblib

# Load model dan scaler terbaru
model = joblib.load('./model.pkl')
scaler = joblib.load('./scaler.pkl')

# Title aplikasi
st.title("Prediksi Dropout Mahasiswa - Jaya Jaya Institut")

# Input data user
st.header("Masukkan Data Mahasiswa")

admission_grade = st.number_input("Nilai Masuk (Admission_grade) (0-200)", min_value=0.0, max_value=200.0, step=1.0)
curricular_1st_enrolled = st.number_input("Mata Kuliah Diambil (Curricular_units_1st_sem_enrolled) (Semester 1)", min_value=0, step=1)
curricular_1st_approved = st.number_input("Mata Kuliah Disetujui (Curricular_units_1st_sem_approved) (Semester 1)", min_value=0, step=1)
tuition_fees_up_to_date = st.selectbox("Biaya Kuliah Terbayar Tepat Waktu? (Tuition_fees_up_to_date)", [1, 0])
scholarship_holder = st.selectbox("Penerima Beasiswa? (Scholarship_holder)", [1, 0])
age_at_enrollment = st.number_input("Usia Saat Masuk (Age_at_enrollment)", min_value=17, max_value=40, step=1)
marital_status = st.selectbox("Status Pernikahan (Marital_status)", [1, 2, 3, 4, 5, 6])
application_mode = st.selectbox("Metode Aplikasi (Application_mode)", [1, 2, 5, 7, 10, 15, 16, 17, 18, 26, 27, 39, 42, 43, 44, 51, 53, 57])
course = st.number_input("Kode Program Studi (Course)", min_value=1, step=1)
previous_qualification = st.number_input("Kualifikasi Sebelumnya (Previous_qualification)", min_value=1, step=1)
gender = st.selectbox("Jenis Kelamin (Gender) (1 = Laki-laki, 0 = Perempuan)", [1, 0])
curricular_2nd_enrolled = st.number_input("Mata Kuliah Diambil (Curricular_units_2nd_sem_enrolled) (Semester 2)", min_value=0, step=1)
curricular_2nd_approved = st.number_input("Mata Kuliah Disetujui (Curricular_units_2nd_sem_approved) (Semester 2)", min_value=0, step=1)
unemployment_rate = st.number_input("Tingkat Pengangguran (Unemployment_rate) (%)", step=0.1)
inflation_rate = st.number_input("Tingkat Inflasi (Inflation_rate) (%)", step=0.1)
gdp = st.number_input("GDP (Gross Domestic Product)", step=0.1)

# Prediksi jika tombol ditekan
if st.button("Prediksi Status Mahasiswa"):
    # Menggabungkan input user
    input_data = np.array([[admission_grade, curricular_1st_enrolled, curricular_1st_approved,
                            tuition_fees_up_to_date, scholarship_holder, age_at_enrollment,
                            marital_status, application_mode, course, previous_qualification,
                            gender, curricular_2nd_enrolled, curricular_2nd_approved,
                            unemployment_rate, inflation_rate, gdp]])
    
    # Normalisasi data
    input_data_scaled = scaler.transform(input_data)
    
    # Prediksi dengan model
    prediction = model.predict(input_data_scaled)[0]
    label_map = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
    
    # Menampilkan hasil prediksi
    st.subheader(f"Prediksi: {label_map[prediction]}")
