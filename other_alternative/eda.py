import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE
#st.set_page_config(layout="wide")
#lottie_book = load_lottieurl('https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json')

def load_page(df_metadata_complete):

    ###Streamlit app
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((0.01, 3.2, 0.01))

    with row1_1:
        st.markdown("# 📊 Exploratory Data Analysis")