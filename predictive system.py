# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import pickle 
 # loading the saved model
loaded_model = pickle.load(open('C:/Users/user/Desktop/submission/tenant_model.sav', 'rb'))

    
input_data = pd.DataFrame({
    'BHK': [2],
    'Size': [950],
    'Bathroom': [2],
    'Furnishing Status': ['Semi-Furnished'],
    'Tenant Preferred': ['Bachelors/Family'],
    'City': ['Mumbai'],
    'Point of Contact': ['Contact Owner'],
    'Area Locality': ['Andheri West'],    # example locality
    'Posted On': ['2025-01-15'],          # sample date
    'Area Type': ['Super Area'],          # must be included
    'Floor': ['5 out of 10']              # must be included
})

prediction =loaded_model.predict(input_data)
predicted_rent = prediction[0]

print("Predicted Rent Payment:", predicted_rent)

# Scenario logic 
if predicted_rent > 30000:  
    print("⚠️ Tenant may struggle to pay on time (high rent).")
else:
    print("✅ Tenant is likely to pay rent on time.")
    
    