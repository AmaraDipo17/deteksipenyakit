import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Load the original training data
original_data = pd.read_csv('datasheet.csv')

# Split the data into features and target
x = original_data.drop(columns='Diagnosis', axis=1)
y = original_data['Diagnosis']

# Initialize or load your KNN model
scaler = StandardScaler()
scaler.fit(x)
standarized_data = scaler.transform(x)
x = standarized_data

# Split the data into training
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=2)

k = 5  # Number of neighbors
classifier = KNeighborsClassifier(n_neighbors=k)
classifier.fit(x_train, y_train)

st.title('Prediksi Penyakit')

# membagi kolom
col1, col2 = st.columns(2)

with col1:
    nama = st.text_input('Nama')
    Hb = st.text_input('Hb (gr%)')
    Sistol = st.text_input('Sistol')
    Diastol = st.text_input('Diastol')
    ProteinUrine = st.text_input('Protein Urine')
    Interval = st.text_input('Interval')

with col2:
    usia = st.text_input('Usia')
    Hight = st.text_input('Height')
    Weight = st.text_input('Weight')
    BMI = st.text_input('BMI')
    HistoryofPE = st.text_input('History of PE')
    HistoryofHipertensi = st.text_input('History of Hipertensi')

# Input untuk MAP
MAP = st.text_input('MAP')

# Create a user input DataFrame
input_data = pd.DataFrame({
    'Hb (gr%)': [Hb],
    'Sistol (mmHg)': [Sistol],
    'Diastol (mmHg)': [Diastol],
    'Protein Urine': [ProteinUrine],
    'Interval (month)': [Interval],
    'Hight (cm)': [Hight],
    'Weight (kg)': [Weight],
    'BMI': [BMI],
    'History of PE': [HistoryofPE],
    'History of Hipertensi': [HistoryofHipertensi],
    'MAP': [MAP]
})

# Predict the diagnosis
if st.button('Prediksi Penyakit'):
    input_data_as_numpy_array = np.array(input_data)
    input_data_reshape = input_data_as_numpy_array.reshape(1, -1)
    std_data = scaler.transform(input_data_reshape)
    prediction = classifier.predict(std_data)

    # Update the original training data with the new data point
    new_data_point = input_data.copy()
    new_data_point['Diagnosis'] = prediction[0]
    updated_data = pd.concat([original_data, new_data_point], ignore_index=True)

    # Save the updated data to a new CSV file
    updated_data.to_csv('updated_datasheet.csv', index=False)

    # Display the diagnosis
    if prediction[0] == 1:
        diagnosis = "Chronic Hypertension"
    elif prediction[0] == 2:
        diagnosis = "Hypertension in Pregnancy"
    elif prediction[0] == 3:
        diagnosis = "Preeclampsia"
    elif prediction[0] == 4:
        diagnosis = "Severe Preeclampsia"
    elif prediction[0] == 5:
        diagnosis = "Superimposed Preeclampsia"
    else:
        diagnosis = "Healthy Pregnant Women"

    # Display the name, age, and diagnosis
    st.success(f'Nama: {nama}')
    st.success(f'Usia: {usia}')
    st.success(diagnosis)