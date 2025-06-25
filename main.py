import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from get_longlat_from_ps import get_location_from_powershell
from get_ap_data import get_wifi_aps_pywifi_windows_robust_v2

def get_wifi_data_for_prediction():
    script_path = "get_location.ps1"
    aps_df = get_wifi_aps_pywifi_windows_robust_v2()
    loc_df = get_location_from_powershell(script_path)

    if aps_df.empty or loc_df.empty:
        return None, None, None

    if (aps_df['signal_dBm'] == 0).all():
        return "Pastikan berada di Rektorat Sindangsari", None, None

    strongest_ap = aps_df.loc[aps_df['signal_dBm'].idxmax()]
    bssid = strongest_ap['bssid']
    signal = strongest_ap['signal_dBm']
    freq = strongest_ap['frequency_MHz']
    lat = loc_df.iloc[0]['latitude']
    lon = loc_df.iloc[0]['longitude']

    return bssid, signal, freq, lat, lon

svm = joblib.load('svm_model.pkl')
scaler = StandardScaler()
df = pd.read_csv("dataset_model_per_lantai.csv")
feature_names = df.columns[:-1].tolist()

if "Unnamed: 33" in feature_names:
    feature_names.remove("Unnamed: 33")

scaler.fit(df[feature_names])

st.title("📡 Prediksi Tempat (Masih Terbatas pada Rektorat)")

input_mode = st.radio(
    "Pilih metode input data:",
    ["Otomatis (Wi-Fi Snapshot)", "Manual", "Upload CSV"] 
)

if input_mode == "Upload CSV":
    uploaded_file = st.file_uploader("📂 Unggah file CSV berisi nilai fitur", type=["csv"])
    if uploaded_file is not None:
        csv_df = pd.read_csv(uploaded_file, header=None)

        if csv_df.shape[1] > 32:
            csv_df = csv_df.drop(csv_df.columns[32], axis=1)

        if csv_df.shape[0] == 1:
            csv_df = csv_df.T

        if csv_df.shape[0] != len(feature_names):
            st.error(
                f"Jumlah nilai ({csv_df.shape[0]}) ≠ jumlah fitur "
                f"yang diharapkan ({len(feature_names)})."
            )
            st.stop()

        csv_df.index = feature_names
        csv_df = csv_df.T 

        if (csv_df == 0).all(axis=None):
            st.error(
                "Pastikan berada di Rektorat Sindangsari. "
                "Jika sudah di sana, silakan coba pindah lokasi."
            )
            st.stop()

        scaled_input = scaler.transform(csv_df[feature_names])
        preds = svm.predict(scaled_input)

        for i, pred in enumerate(preds, start=1):
            st.success(f"📍 Baris {i}: Prediksi Lantai → **{pred}**")

        st.write("🔧 Fitur yang digunakan:")
        st.dataframe(csv_df)

elif input_mode == "Otomatis (Wi-Fi Snapshot)":
    if st.button("🔍 Ambil Snapshot & Prediksi"):
        with st.spinner("Memindai jaringan dan lokasi..."):
            result = get_wifi_data_for_prediction()
            if result[0] is None:
                st.error("Gagal mendeteksi jaringan atau lokasi. Mohon pastikan Wi-Fi aktif dan lokasi berada di Rektorat Sindangsari.")
            else:
                bssid, signal, freq, lat, lon = result
                bssid_numeric = hash(bssid) % 1_000_000

                input_dict = {
                    'bssid': bssid_numeric,
                    'signal_dBm': signal,
                    'frequency_MHz': freq,
                    'latitude': lat,
                    'longitude': lon
                }

                for feature in feature_names:
                    if feature not in input_dict:
                        input_dict[feature] = 0.0

                input_df = pd.DataFrame([input_dict])[feature_names]

                # ⬇️ Tambahan: cek semua nol
                if (input_df == 0).all(axis=None):
                    st.error(
                        "Pastikan berada di Rektorat Sindangsari. "
                        "Jika sudah di sana, silakan coba pindah lokasi."
                    )
                else:
                    scaled_input = scaler.transform(input_df)
                    prediction = svm.predict(scaled_input)
                    st.success(f"📍 Prediksi Lantai: **{prediction[0]}**")
                    st.write("🔧 Fitur yang digunakan untuk prediksi:")
                    st.dataframe(input_df)

else:
    st.header("✍️ Masukkan Nilai Fitur Secara Manual")
    user_input = []
    for feature in feature_names:
        val = st.number_input(f"{feature}", value=0.0)
        user_input.append(val)

    if st.button("🧮 Prediksi dari Input Manual"):
        input_df = pd.DataFrame([user_input], columns=feature_names)

        # ⬇️ Tambahan: cek semua nol
        if (input_df == 0).all(axis=None):
            st.error(
                "Pastikan berada di Rektorat Sindangsari. "
                "Jika sudah di sana, silakan coba pindah lokasi."
            )
        else:
            scaled_input = scaler.transform(input_df)
            prediction = svm.predict(scaled_input)
            st.success(f"📍 Prediksi Lantai: **{prediction[0]}**")
            st.write("🔧 Fitur yang digunakan untuk prediksi:")
            st.dataframe(input_df)
