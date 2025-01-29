import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
con = sqlite3.connect(r"C:\Users\Nevai\OneDrive\Desktop\Skolarbete\Data Science\Kunskapskontrol_3\Köksglädje.db")

st.markdown("<h1 style='text-align: center;'>Köksglädje AB</h1>", unsafe_allow_html=True)

# Bild på startsidan
image_path = r"C:\Users\Nevai\OneDrive\Desktop\Skolarbete\Data Science\Kunskapskontrol_3\KGAB 1.webp"

# Skapar columner för att centrera bilden
col1, col2, col3 = st.columns([1, 3, 1])  
with col2:
    st.image(image_path)


# Skriver ut kort beskrivning på startsidan
st.markdown("<h6 style='text-align: center;'>Vi på MGJ Consulting har på uppdrag av Köksglädje AB genomfört inläsning av deras samlade data för samtliga butiker i koncernen. Vi har på ett systematiskt och noggrant vis analyserat deras data. Resultatet presenteras efter överenskommelse med Köksglädje AB.</h1>", unsafe_allow_html=True)

# st.write('''Vi på MGJ (read MJ) Consulting har på uppdrag av Köksglädje AB genomfört inläsning av deras samlade data för samtliga butiker i koncernen. Vi har på ett systematiskt och noggrant vis analyserat deras data. Resultatet presenteras efter överenskommelse med Köksglädje AB.''')