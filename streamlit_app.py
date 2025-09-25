import streamlit as st
import requests

st.title("Online Payment Fraud Detection")
st.write("Enter the transaction details to predict if it is fraudulent.")

# Input fields for the user
step = st.slider("Step (Unit of time, 1 hour)", 1, 743, 200)

transaction_type_options = {
    'PAYMENT': 0, 
    'CASH_IN': 1, 
    'DEBIT': 2, 
    'CASH_OUT': 3, 
    'TRANSFER': 4
}
type_str = st.selectbox("Transaction Type", list(transaction_type_options.keys()))
type_val = transaction_type_options[type_str]

amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
oldbalanceOrg = st.number_input("Old Balance (Originator)", min_value=0.0, format="%.2f")
oldbalanceDest = st.number_input("Old Balance (Recipient)", min_value=0.0, format="%.2f")

# The button to trigger the prediction
if st.button("Predict"):
    # Prepare the data to be sent to the FastAPI endpoint
    data = {
        "step": step,
        "type": type_val,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "oldbalanceDest": oldbalanceDest,
    }

    # Make the request to the FastAPI endpoint
    # You would use the deployed URL here in a real-world scenario
    fastapi_url = "http://127.0.0.1:8000/predict"
    try:
        response = requests.post(fastapi_url, json=data)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Prediction Result:")
            if result["is_fraud"]:
                st.error(f"This is a fraudulent transaction with a probability of {result['prediction_probability']:.2f}")
            else:
                st.success(f"This is a non-fraudulent transaction with a probability of {1 - result['prediction_probability']:.2f}")
        else:
            st.error(f"Error from API: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Please ensure it is running.")