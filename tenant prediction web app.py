# -*- coding: utf-8 -*-
"""
Tenant Rent Prediction App
Created on Wed Sep 24 23:23:11 2025
@author: GODSON
"""

import numpy as np
import pandas as pd
import pickle
import streamlit as st

# Load the saved model
loaded_model = pickle.load(open('C:/Users/user/Desktop/submission/tenant_model.sav', 'rb'))

# Function for prediction
def tenant_prediction(input_data):
    prediction = loaded_model.predict(input_data)
    predicted_rent = prediction[0]

    if predicted_rent > 90000:
        return predicted_rent, "⚠️ Tenant may struggle to pay on time (high rent)."
    else:
        return predicted_rent, "✅ Tenant is likely to pay rent on time."

# Streamlit UI
st.set_page_config(page_title="🏠 Tenant Rent Prediction", page_icon="💰", layout="wide")
st.title("🏠 Tenant Rent Payment Prediction System")
st.markdown("Enter tenant details below to predict rent and payment reliability.")

# Create two columns: left for input, right for history
col1, col2 = st.columns([2, 1])  # left wider, right narrow

with col1:
    st.header("📊 Enter Tenant Details")
    BHK = st.number_input("BHK (Bedrooms, Hall, Kitchen)", min_value=1, max_value=10, value=2)
    Size = st.number_input("Size (sq.ft)", min_value=100, max_value=10000, value=950)
    Bathroom = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)

    Furnishing_Status = st.text_input("Furnishing Status (e.g., Semi-Furnished)")
    Tenant_Preferred = st.text_input("Tenant Preferred (e.g., Family/Bachelors)")
    City = st.text_input("City / Location")
    Point_of_Contact = st.text_input("Point of Contact")
    Area_Locality = st.text_input("Area Locality")
    Posted_On = st.date_input("Posted On")
    Area_Type = st.text_input("Area Type (e.g., Super Area)")
    Floor = st.text_input("Floor (e.g., '5 out of 10')")

    # Predict Button
    if st.button("🔍 Predict Rent"):
        # Create dataframe from user inputs
        input_df = pd.DataFrame({
            'BHK': [BHK],
            'Size': [Size],
            'Bathroom': [Bathroom],
            'Furnishing Status': [Furnishing_Status],
            'Tenant Preferred': [Tenant_Preferred],
            'City': [City],
            'Point of Contact': [Point_of_Contact],
            'Area Locality': [Area_Locality],
            'Posted On': [str(Posted_On)],
            'Area Type': [Area_Type],
            'Floor': [Floor]
        })

        # Get prediction
        predicted_rent, message = tenant_prediction(input_df)

        # Display results
        st.success(f"💰 Predicted Rent: **{predicted_rent:,.2f}**")
        st.info(message)

        # Save inputs + result into session state
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "Inputs": input_df.to_dict(orient="records")[0],
            "Predicted Rent": predicted_rent,
            "Message": message
        })

with col2:
    st.header("📜 History")
    if "history" in st.session_state and st.session_state.history:
        # Enumerate history (reverse order: newest first)
        for i, record in enumerate(st.session_state.history[::-1]):
            entry_index = len(st.session_state.history) - 1 - i  # actual index in list

            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color:#f9f9f9; padding:10px; 
                                margin-bottom:10px; border-radius:10px;
                                box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#2c3e50;">Entry {i+1}</h4>
                        <p style="margin:2px 0;"><b>BHK:</b> {record['Inputs']['BHK']}, 
                        <b>Size:</b> {record['Inputs']['Size']} sq.ft, 
                        <b>Bath:</b> {record['Inputs']['Bathroom']}</p>
                        <p style="margin:2px 0;"><b>City:</b> {record['Inputs']['City']} | 
                        <b>Locality:</b> {record['Inputs']['Area Locality']}</p>
                        <p style="margin:2px 0;"><b>Rent:</b>  {record['Predicted Rent']:,.2f}</p>
                        <p style="margin:2px 0;">{record['Message']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Delete button for this entry
                if st.button(f"🗑️ Delete Entry {i+1}", key=f"del_{entry_index}"):
                    st.session_state.history.pop(entry_index)
                    st.rerun()
    else:
        st.info("No previous data yet.")
