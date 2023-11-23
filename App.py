import streamlit as st
import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import sqlite3
import streamlit.components.v1 as components


# Set page config
st.set_page_config(page_title="Machine Learning Image Classifier", initial_sidebar_state="collapsed")

# Add styles
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <style>
        .reportview-container {
            background-color: #f0f2f6;
        }
        .big-font {
            font-size: 30px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Load model
@st.cache(allow_output_mutation=True)
def load_my_model():
    return load_model('FYP.h5')

model = load_my_model()

# Initialize database
def init_db():
    con = sqlite3.connect('feedback.db')
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_data (
            feedback INTEGER
        )
    ''')
    con.commit()
    return con, cursor

def save_feedback(cursor, feedback):
    cursor.execute("INSERT INTO feedback_data (feedback) VALUES (?)", (feedback,))
    con.commit()

con, cursor = init_db()

# Function to predict image
def predict_image(img_array):
    predictions = model.predict(img_array)
    confidence_for_Normal_XRay = predictions[0][0]
    if confidence_for_Normal_XRay >= 0.5:
        return "Pneumonia X-Ray", confidence_for_Normal_XRay
    else:
        return "Normal X-Ray", 1 - confidence_for_Normal_XRay

# App layout
st.markdown('# Machine Learning Image Classifier', unsafe_allow_html=True)

st.markdown('### Download Test Images and Instructions:')
st.markdown('[Click here to download](https://drive.usercontent.google.com/download?id=1GkfpA2lZYBZFjyJVrUJ2JktLJCoQEtKW&export=download&authuser=0&confirm=t&uuid=bbc4d2fa-4d0a-496b-bd0b-f5d4cc66be6a&at=APZUnTXikZlI0iAScVYRFtv-pc8_:1699900643544)')

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    uploaded_file = st.file_uploader("📊 Choose an X-ray image.", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file:
        image = load_img(uploaded_file, target_size=(224, 224))

        img_array = img_to_array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Display the image
        st.image(image, caption='Succesfully uploaded Image.', use_column_width=True)

        predicted_class, confidence = predict_image(img_array)
        st.markdown(f"# Predicted Class: **{predicted_class}** with *{confidence * 100:.2f}%* confidence.", unsafe_allow_html=True)

# Feedback section
st.markdown('## 🌟 I value your feedback!', unsafe_allow_html=True)
feedback1 = st.slider("Rate your experience (1-10)", 1, 10, key="feedback_slider1")

if st.button("Submit Feedback"):
    save_feedback(cursor, feedback1)
    st.success(f"Thank you for your feedback! You rated the app as {feedback1}/10")

if st.button("Show Feedback Summary"):
    cursor.execute("SELECT feedback, COUNT(*) as count FROM feedback_data GROUP BY feedback")
    feedback_data = cursor.fetchall()
    df = pd.DataFrame(feedback_data, columns=["Feedback", "Count"])
    st.bar_chart(df.set_index("Feedback"))

st.markdown("""
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <h3 style="margin: 0;">👨‍💻 By Cormac :) </h3>
        <a href="https://urldefense.com/v3/__https://twitter.com/Cmac_GN__;!!ODpDvJZr5w!DdZF0JvUVsv3QtWGZvsA79wolrXVe5YvXo6k-gR0RNrsC3f7hVNIousCU4Fm2cHxXXJS-3OZ_AzBE1096ZiE5OsI$" target="_blank" style="margin-left: 10px;">
            <i class="fab fa-twitter-square" style="font-size: 24px;"></i>
        </a>
        <a href="https://urldefense.com/v3/__https://www.instagram.com/cmac_987/__;!!ODpDvJZr5w!DdZF0JvUVsv3QtWGZvsA79wolrXVe5YvXo6k-gR0RNrsC3f7hVNIousCU4Fm2cHxXXJS-3OZ_AzBE1096UT30p10$" target="_blank" style="margin-left: 10px;">
            <i class="fab fa-instagram" style="font-size: 24px;"></i>
        </a>
    </div>
""", unsafe_allow_html=True)
