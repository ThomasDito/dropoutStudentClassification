# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lRHYqHc_zA4QQilKpTR2h_-IlkGLElY6

# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

- Nama: Thomas Dito Rigorastio
- Email: B244019E@devacademy.id
- Id Dicoding: B244019E

## Pertanyaan Bisnis Sebagai Acuan Untuk EDA & Visualisasi

1. Bagaimana hubungan antara nilai masuk (Admission Grade) dengan kemungkinan dropout?
2. Bagaimana pengaruh jumlah mata kuliah yang diambil dan tingkat keberhasilannya terhadap dropout?
3. Apakah ada korelasi antara kondisi sosial-ekonomi (pendidikan orang tua, beasiswa, dan status pembayaran biaya kuliah) dengan dropout?
4. Bagaimana pengaruh usia saat masuk terhadap kemungkinan dropout?
5. Apakah ada tren dropout berdasarkan program studi tertentu?
6. Apa faktor penting dalam memonitor performa siswa atau mencegah dropout?

## Persiapan

### Menyiapkan library yang dibutuhkan
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.metrics import precision_score, recall_score, f1_score

"""### Menyiapkan data yang akan diguankan"""

df = pd.read_csv('data.csv', delimiter=";")
df.head()

"""## Data Understanding"""

df.info()

"""catatan:
- melihat basic information dari dataset
- terlihat tidak ada missing value pada kolom attrition
"""

df.isna().sum()

"""catatang:
- melakukan pengecekan dengan isna() untuk mengetahui missing value dengan spesifik
- ternyata tidak ditemukan adanya missing value
"""

print("jumlah duplikasi data: ", df.duplicated().sum())
df.describe()

"""catatan
- melakukan pengecekan pada duplikasi data dan deskripsi statistik
- tidak ada duplikasi data
- parameter statistik pun terlihat normal
- dataset benar-benar bersih dengan tidak adanya, missing value, duplikasi data, dan parameter statistik pun tergolong baik

## EDA & Visualisasi data
"""

# upload database ke supabase

# passdb = admin123
URL = "postgresql://postgres.ujazzozilvccnvbppftr:admin123@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(URL)
df.to_sql('edutech', engine)

# Count plot untuk distribusi status siswa
status_counts = df['Status'].value_counts()

# Plot distribusi
plt.figure(figsize=(8, 5))
status_counts.plot(kind='bar', color=['red', 'blue', 'green'])
plt.title('Distribusi Status Mahasiswa')
plt.xlabel('Status Mahasiswa')
plt.ylabel('Jumlah')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Grafik di atas menunjukkan distribusi status mahasiswa di Jaya Jaya Institut, termasuk jumlah mahasiswa yang dropout, masih enrolled, atau telah graduate.
- terlihat status mahasiswa yang lulus merupakan yang paling banyak
- namun, status dropout jugalah sangat banyak, merupakan kedua terbanyak

1. Bagaimana hubungan antara nilai masuk (Admission Grade) dengan kemungkinan dropout?
"""

# Visualisasi hubungan antara Admission Grade dan Status mahasiswa

plt.figure(figsize=(10, 6))
sns.boxplot(x='Status', y='Admission_grade', data=df, palette={'Dropout': 'red', 'Enrolled': 'blue', 'Graduate': 'green'})
plt.title('Distribusi Admission Grade Berdasarkan Status Mahasiswa')
plt.xlabel('Status Mahasiswa')
plt.ylabel('Admission Grade')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Mahasiswa yang dropout cenderung memiliki nilai admission yang lebih rendah dibandingkan mahasiswa yang lulus.
- Mahasiswa yang graduate cenderung memiliki median Admission Grade yang lebih tinggi dibandingkan yang dropout.
- Terdapat outlier dalam setiap kategori, yang bisa dianalisis lebih lanjut.

2. Bagaimana pengaruh jumlah mata kuliah yang diambil dan tingkat keberhasilannya terhadap dropout?
"""

# Visualisasi dengan Bar Chart: Rata-rata jumlah mata kuliah yang diambil dan disetujui berdasarkan status mahasiswa

# Menghitung rata-rata mata kuliah yang diambil dan disetujui untuk setiap status
enrolled_avg = df.groupby('Status')[['Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_approved']].mean()

# Plot bar chart
enrolled_avg.plot(kind='bar', figsize=(10, 6), color=['orange', 'green'])

plt.title('Rata-rata Mata Kuliah yang Diambil dan Disetujui di Semester 1')
plt.xlabel('Status Mahasiswa')
plt.ylabel('Rata-rata Jumlah Mata Kuliah')
plt.xticks(rotation=0)
plt.legend(['Mata Kuliah Diambil', 'Mata Kuliah Disetujui'])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Mahasiswa dropout rata-rata mengambil lebih sedikit mata kuliah dibandingkan mahasiswa yang lulus.
- Rata-rata jumlah mata kuliah yang disetujui jauh lebih rendah untuk mahasiswa yang dropout dibandingkan mahasiswa yang graduate.
- Mahasiswa yang graduate memiliki rasio yang lebih tinggi antara jumlah mata kuliah yang diambil dan yang disetujui.

3. Apakah ada korelasi antara kondisi sosial-ekonomi (pendidikan orang tua, beasiswa, dan status pembayaran biaya kuliah) dengan dropout?
"""

# Visualisasi pengaruh status pembayaran biaya kuliah terhadap status mahasiswa menggunakan grouped bar chart yang dikelompokkan

tuition_grouped = df.groupby('Tuition_fees_up_to_date')['Status'].value_counts().unstack()

# Plot grouped bar chart
tuition_grouped.plot(kind='bar', figsize=(10, 6), color=['red', 'blue', 'green'])

plt.title('Pengaruh Status Pembayaran Biaya Kuliah terhadap Status Mahasiswa')
plt.xlabel('Biaya Kuliah Dibayar Tepat Waktu (0 = Tidak, 1 = Ya)')
plt.ylabel('Jumlah Mahasiswa')
plt.xticks(rotation=0)
plt.legend(['Dropout', 'Enrolled', 'Graduate'], title='Status Mahasiswa')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Mahasiswa yang tidak membayar biaya kuliah tepat waktu memiliki jumlah dropout yang jauh lebih tinggi dibandingkan yang membayar tepat waktu.
- Mahasiswa yang membayar tepat waktu memiliki jumlah graduate yang lebih banyak.
- Jumlah mahasiswa yang masih enrolled lebih seimbang antara yang membayar tepat waktu dan yang tidak.
"""

# Visualisasi pengaruh pendidikan orang tua terhadap status mahasiswa

# Mengelompokkan berdasarkan pendidikan ibu
mother_edu_grouped = df.groupby('Mothers_qualification')['Status'].value_counts().unstack()

# Plot bar chart pendidikan ibu
mother_edu_grouped.plot(kind='bar', figsize=(12, 6), color=['red', 'blue', 'green'])

plt.title('Pengaruh Pendidikan Ibu terhadap Status Mahasiswa')
plt.xlabel('Pendidikan Ibu')
plt.ylabel('Jumlah Mahasiswa')
plt.xticks(rotation=90)
plt.legend(['Dropout', 'Enrolled', 'Graduate'], title='Status Mahasiswa')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

"""insight:
- Mahasiswa dengan ibu yang memiliki tingkat pendidikan lebih rendah cenderung memiliki jumlah dropout yang lebih tinggi.
- Mahasiswa dengan ibu yang memiliki pendidikan tinggi (misalnya Master atau Doktor) cenderung memiliki jumlah graduate yang lebih banyak.
- Pendidikan ibu mungkin memiliki dampak tidak langsung terhadap performa akademik mahasiswa, kemungkinan terkait dengan dukungan akademik dan sosial yang diberikan.
"""

# Visualisasi pengaruh status beasiswa terhadap status mahasiswa

# Mengelompokkan berdasarkan status beasiswa
scholarship_grouped = df.groupby('Scholarship_holder')['Status'].value_counts().unstack()

# Plot grouped bar chart untuk status beasiswa
scholarship_grouped.plot(kind='bar', figsize=(10, 6), color=['red', 'blue', 'green'])

plt.title('Pengaruh Status Beasiswa terhadap Status Mahasiswa')
plt.xlabel('Penerima Beasiswa (0 = Tidak, 1 = Ya)')
plt.ylabel('Jumlah Mahasiswa')
plt.xticks(rotation=0)
plt.legend(['Dropout', 'Enrolled', 'Graduate'], title='Status Mahasiswa')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

"""insight:
- Mahasiswa yang menerima beasiswa memiliki jumlah graduate yang tinggi, walaupun yang tidak menerima beasiswa memiliki jumlah graduate yang lebih tinggi.
- Mahasiswa yang tidak menerima beasiswa memiliki tingkat dropout yang lebih tinggi.
- Beasiswa kemungkinan membantu mahasiswa secara finansial dan akademik, sehingga meningkatkan kemungkinan mereka untuk menyelesaikan studi.

4. Bagaimana pengaruh usia saat masuk terhadap kemungkinan dropout?
"""

# Visualisasi pengaruh usia saat masuk terhadap kemungkinan dropout

plt.figure(figsize=(10, 6))
sns.boxplot(x='Status', y='Age_at_enrollment', data=df, palette={'Dropout': 'red', 'Enrolled': 'blue', 'Graduate': 'green'})
plt.title('Distribusi Usia saat Masuk Berdasarkan Status Mahasiswa')
plt.xlabel('Status Mahasiswa')
plt.ylabel('Usia saat Masuk')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Mahasiswa yang dropout cenderung memiliki usia masuk yang lebih tinggi dibandingkan mereka yang lulus.
- Mahasiswa yang graduate memiliki distribusi usia yang lebih rendah dibandingkan mahasiswa yang dropout.
- Ini menunjukkan bahwa mahasiswa yang masuk dengan usia lebih tua mungkin memiliki tantangan tambahan dalam menyelesaikan studi mereka.

5. Apakah ada tren dropout berdasarkan program studi tertentu?
"""

# Menghitung jumlah mahasiswa dropout per program studi
course_dropout = df[df['Status'] == 'Dropout']['Course'].value_counts()

# Plot bar chart dropout per program studi
plt.figure(figsize=(12, 6))
course_dropout.plot(kind='bar', color='red')

plt.title('Jumlah Mahasiswa Dropout Berdasarkan Program Studi')
plt.xlabel('Kode Program Studi')
plt.ylabel('Jumlah Dropout')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

"""insight:
- Terdapat beberapa program studi dengan tingkat dropout yang lebih tinggi dibandingkan yang lain.
- Program studi dengan jumlah dropout tinggi mungkin memiliki tingkat kesulitan lebih besar atau kurangnya dukungan akademik bagi mahasiswa.
- Perlu analisis lebih lanjut untuk mengetahui faktor spesifik yang menyebabkan dropout dalam program-program tersebut.

6. Apa faktor penting dalam memonitor performa siswa atau mencegah dropout? (Pertanyaan wajib)
"""

# Mengubah status mahasiswa menjadi nilai numerik untuk korelasi
status_mapping = {'Dropout': 1, 'Enrolled': 0, 'Graduate': -1}
df['Status_numeric'] = df['Status'].map(status_mapping)

# Memilih fitur yang relevan untuk korelasi dengan dropout
correlation_features = [
    'Admission_grade', 'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_approved',
    'Tuition_fees_up_to_date', 'Mothers_qualification', 'Fathers_qualification',
    'Scholarship_holder', 'Age_at_enrollment', 'Course'
]

# Menghitung matriks korelasi
correlation_matrix = df[correlation_features + ['Status_numeric']].corr()

# Visualisasi heatmap korelasi
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, annot_kws={"size": 10})
plt.title('Heatmap Korelasi Faktor-faktor Akademik dan Sosial terhadap Dropout')
plt.show()

"""insight:
1. Admission Grade (-0.12)
    - Memiliki korelasi negatif dengan dropout, yang berarti semakin tinggi nilai masuk, semakin kecil kemungkinan mahasiswa dropout.
    - Hal ini mendukung temuan sebelumnya bahwa mahasiswa dengan nilai masuk rendah memiliki risiko dropout lebih tinggi.

2. Curricular Units 1st Sem Enrolled (-0.16) & Approved (-0.53)
    - Mahasiswa yang mengambil lebih banyak mata kuliah dan menyelesaikannya dengan sukses memiliki kemungkinan dropout yang lebih kecil.
    - Korelasi yang lebih tinggi pada "Approved" menunjukkan bahwa kemampuan menyelesaikan mata kuliah lebih penting daripada hanya mendaftar.

3. Tuition Fees Up To Date (-0.41)
    - Korelasi negatif menunjukkan bahwa mahasiswa yang membayar biaya kuliah tepat waktu lebih kecil kemungkinan dropout.
    - Ini mengonfirmasi bahwa dukungan finansial atau fleksibilitas pembayaran dapat membantu mengurangi dropout.

4. Pendidikan Orang Tua (Mothers & Fathers Qualification) (0.04, 0.0)
    - Memiliki korelasi positif ringan, yang berarti semakin tinggi tingkat pendidikan orang tua, ada kemungkinan semakin kecil kemungkinan mahasiswa dropout, walaupun pada temuan sebelumnya, ada juga mahasiswa dengan pendidikan orang tua yang tinggi tetapi memiliki jumlah dropout yang cukup tinggi.
    - Hal ini mendukung temuan bahwa dukungan akademik dari keluarga bisa menjadi faktor penting dalam keberhasilan mahasiswa.

5. Scholarship Holder (-0.30)
    - Mahasiswa penerima beasiswa memiliki kemungkinan dropout yang lebih kecil.
    - Ini menegaskan bahwa beasiswa bisa menjadi faktor pelindung dalam mencegah dropout.

6. Age at Enrollment (0.24)
    - Korelasi positif menunjukkan bahwa mahasiswa yang masuk dengan usia lebih tua memiliki kemungkinan dropout yang lebih tinggi.
    - Ini mengonfirmasi temuan bahwa mahasiswa yang lebih tua mungkin memiliki tantangan lebih besar dalam menyelesaikan studi.

## Data Preparation / Preprocessing
"""

# Cek kategori asli sebelum encoding
print("Kategori Status sebelum encoding:", df['Status'].unique())

# Encode target variable (Status)
label_encoder = LabelEncoder()
df["Status"] = label_encoder.fit_transform(df["Status"])  # Dropout=0, Enrolled=1, Graduate=2

# Periksa hasil encoding
print("Status after encoding:", df['Status'].unique())

"""catatan:
- pada proses ini, fitur status yang merupakan target dari klasifikasi dilakukan encoding, menjadi fitur numerik
- Dropout=0, Enrolled=1, Graduate=2
"""

# Menentukan fitur yang akan digunakan dalam model
features = [
    "Admission_grade", "Curricular_units_1st_sem_enrolled", "Curricular_units_1st_sem_approved",
    "Tuition_fees_up_to_date", "Scholarship_holder", "Age_at_enrollment",
    "Marital_status", "Application_mode", "Course", "Previous_qualification",
    "Gender", "Curricular_units_2nd_sem_enrolled", "Curricular_units_2nd_sem_approved",
    "Unemployment_rate", "Inflation_rate", "GDP"
]

# Pisahkan fitur dan target
X = df[features]
y = df["Status"]

# Menampilkan beberapa baris pertama data yang telah diproses
X.head(), y.head()

"""catatan:
- proses ini memilih fitur-fitur yang saya rasa penting dan akan digunakan dalam model
- memisahkan fitur dan terget, kemudian saya masukan ke dalam variabel X dan y
"""

# Normalisasi fitur numerik
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset menjadi training (80%) dan testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Menampilkan bentuk data setelah split
X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""catatan:
- sebelum melakukan data split, semua fitur numerik yang dipilih dilakukan standarisasi dengan standardScaler()
- data dibagi menjadi data latih dan data uji dengan besaran banding 80:20
"""

# Menghitung panjang/jumlah data
print("Jumlah data: ", len(X))
# Menghitung panjang/jumlah data pada X_train
print("Jumlah data latih: ", len(X_train))
# Menghitung panjang/jumlah data pada X_test
print("Jumlah data test: ", len(X_test))

"""catatan:
- terlihat dataset sudah terbagi menjadi set data train dan test dengan detail besarannya seperti yang terlihat pada output cell

## Modeling
"""

# Inisialisasi model Random Forest
rf_model = RandomForestClassifier(random_state=42)

# Melatih model
rf_model.fit(X_train, y_train)

# Prediksi pada training dan test set
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)

# 4. Evaluasi model
def evaluate_model(y_true, y_pred, dataset_type="Dataset"):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')

    print(f"Evaluasi Model pada {dataset_type} Set:")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-score  : {f1:.4f}")
    print("-" * 40)

# Evaluasi pada data training
evaluate_model(y_train, y_train_pred, "Train")

# Evaluasi pada data testing
evaluate_model(y_test, y_test_pred, "Test")

"""Penjelasan algoritma yang digunakan:
- saya gunakan algoritma random forest untuk melakukan modeling
- mengapa? karena saya rasa random forest merupakan algoritma terbaik karena merupakan ensemble learning sehingga model lebih kompleks dibanding algoritma klasifikasi lainnya dan diharapkan akan menghasilkan hasil akurasi dan evaluasi dari metriks lainnya yang baik
- terlihat model rf(random forest) yang digunakan dilatih dan diuji pada data train dan test kemudian dievaluasi menggunakan 4 metriks evaluasi seperti hasil di atas
- terlihat hasil dari keempat metriks evaluasi di atas sangat baik pada data latih, namun performanya menurun pada data tes, kemungkinan hal ini terjadi karena adanya indikasi sedikit overfitting. Hal ini diharapkan bisa diperbaiki pada saat proses tuning model menggunakan hyperparameter tuning.

insight dari hasil pelatihan:
1. Overfitting:

    - Akurasi 99.97% pada train set → Model terlalu menghafal data training.
    - Akurasi hanya 75.82% pada test set → Model kurang generalizable pada data baru.

2. Precision & Recall Drop Signifikan:
    - Perbedaan kurang lebih ~20% antara Train & Test menunjukkan bahwa model terlalu kompleks tanpa regularisasi yang baik.

3. Solusi Overfitting:
    - Hyperparameter tuning (engan GridSearchCV)
    - Menambahkan regularisasi (min_samples_split, min_samples_leaf, max_depth)
    - Meningkatkan generalisasi model dengan tuning jumlah trees (n_estimators)

### Hyperparameter Tuning
"""

# Menentukan hyperparameter yang akan dituning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Inisialisasi model Random Forest
rf_tuned = RandomForestClassifier(random_state=42)

# GridSearchCV untuk mencari kombinasi hyperparameter terbaik
grid_search = GridSearchCV(estimator=rf_tuned, param_grid=param_grid,
                            cv=3, n_jobs=-1, verbose=1, scoring='accuracy')

# Melatih model dengan GridSearch
grid_search.fit(X_train, y_train)

# Menampilkan hasil hyperparameter terbaik
best_params = grid_search.best_params_
best_params

"""catatan:
- melakukan hyperparameter tuning menggunakan metode GridSearchCV
- dari hasil grid search, ditemukan kombinasi parameter terbaik seperti yang terlihat pada output cell
"""

# Inisialisasi model dengan hyperparameter terbaik dari tuning
best_rf_model = RandomForestClassifier(
    max_depth=20,
    min_samples_leaf=2,
    min_samples_split=10,
    n_estimators=300,
    random_state=42
)

# Melatih model dengan data training
best_rf_model.fit(X_train, y_train)

# Melakukan prediksi pada training dan testing set
y_train_best_pred = best_rf_model.predict(X_train)
y_test_best_pred = best_rf_model.predict(X_test)

# Evaluasi model setelah tuning
def evaluate_model(y_true, y_pred, dataset_type="Train"):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')

    print(f"Evaluasi Model pada {dataset_type} Set:")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-score  : {f1:.4f}")
    print("-" * 40)

# Menampilkan hasil evaluasi model
evaluate_model(y_train, y_train_best_pred, "Train (Tuned Model)")
evaluate_model(y_test, y_test_best_pred, "Test (Tuned Model)")

"""catatan:
- Setelah tuning, terlihat model lebih generalizable dan akurat tanpa overfitting yang ekstrem.
- model juga sudah lebih stabil, di mana akurasi pada set training menurun dari yang sebelumnya terlalu baik dalam belajar 97% -> 89%
- walaupun akurasi pada set testing masih lebih kecil, tetapi akurasinya meningkat dari saat sebelum tuning yang menandakan model lebih generalizable dan akurat

## Evaluation
"""

# Membuat perbandingan hasil evaluasi sebelum dan setelah tuning

# Evaluasi model sebelum tuning
accuracy_train = accuracy_score(y_train, y_train_pred)
f1_train = f1_score(y_train, y_train_pred, average='weighted')
precision_train = precision_score(y_train, y_train_pred, average='weighted')
recall_train = recall_score(y_train, y_train_pred, average='weighted')

accuracy_test = accuracy_score(y_test, y_test_pred)
f1_test = f1_score(y_test, y_test_pred, average='weighted')
precision_test = precision_score(y_test, y_test_pred, average='weighted')
recall_test = recall_score(y_test, y_test_pred, average='weighted')

# Evaluasi model setelah tuning
accuracy_train_best = accuracy_score(y_train, y_train_best_pred)
f1_train_best = f1_score(y_train, y_train_best_pred, average='weighted')
precision_train_best = precision_score(y_train, y_train_best_pred, average='weighted')
recall_train_best = recall_score(y_train, y_train_best_pred, average='weighted')

accuracy_test_best = accuracy_score(y_test, y_test_best_pred)
f1_test_best = f1_score(y_test, y_test_best_pred, average='weighted')
precision_test_best = precision_score(y_test, y_test_best_pred, average='weighted')
recall_test_best = recall_score(y_test, y_test_best_pred, average='weighted')

# Menyusun perbandingan hasil evaluasi sebelum dan setelah tuning
pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall",  "F1-Score"],
    "Before Tuning - Training": [accuracy_train, precision_train, recall_train, f1_train],
    "Before Tuning - Testing": [accuracy_test, precision_test, recall_test, f1_test],
    "After Tuning - Training": [accuracy_train_best, precision_train_best, recall_train_best, f1_train_best],
    "After Tuning - Testing": [accuracy_test_best, precision_test_best, recall_test_best, f1_test_best]
})

"""## Analisis Hasil Evaluasi Model:

1. Overfitting Berkurang Secara Signifikan
    - Sebelum tuning, model memiliki akurasi 99.97% di training set, yang menunjukkan bahwa model terlalu kompleks dan menghafal data training.
    - Setelah tuning, akurasi di training set turun ke 88.98%, yang lebih realistis dan menunjukkan model lebih generalizable.

2. Akurasi Model pada Data Uji Meningkat
    - Sebelum tuning, akurasi pada test set hanya 75.82%, sementara setelah tuning meningkat menjadi 78.08%.
    - Hal ini menunjukkan bahwa model lebih baik dalam mengenali pola pada data baru.

3. Precision & Recall Lebih Seimbang
    - Precision meningkat dari 74.04% → 76.90%, yang berarti model sekarang lebih baik dalam meminimalkan kesalahan dalam prediksi dropout atau graduate.
    - Recall meningkat dari 75.82% → 78.08%, yang berarti model lebih baik dalam menangkap semua kasus dropout, enrolled, dan graduate secara lebih akurat.

4. F1-Score Meningkat
    - F1-score meningkat dari 74.38% → 76.60%, yang menunjukkan peningkatan keseimbangan antara precision dan recall.
    - Ini berarti model lebih stabil dalam memprediksi berbagai kategori tanpa bias terhadap satu kategori tertentu.

5. Kesimpulan:
    - ✅ Model setelah tuning memiliki generalisasi yang lebih baik dan tidak lagi overfitting.
    - ✅ Akurasi meningkat 2.26% pada test set, yang menunjukkan peningkatan performa pada data baru.
    - ✅ Precision & Recall lebih tinggi, sehingga model lebih stabil dan akurat.
    - ✅ Model lebih siap untuk digunakan dalam aplikasi Streamlit untuk prediksi dropout mahasiswa.

6. Rekomendasi Lanjutan:
    - Model sudah lebih baik setelah tuning, tetapi bisa lebih dioptimalkan dengan XGBoost atau LightGBM.
    - Menyeimbangkan dataset dengan SMOTE bisa meningkatkan prediksi kelas "Enrolled".
    - SHAP bisa ditambahkan untuk memberikan interpretasi model yang lebih baik bagi pengguna.

## Save model final
"""

# save model
final_model_filename = "./dashboard/model.pkl"

joblib.dump(best_rf_model, final_model_filename)

final_model_filename

# Simpan scaler ke file
joblib.dump(scaler, "scaler.pkl")