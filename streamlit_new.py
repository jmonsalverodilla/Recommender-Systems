# importing libraries
import streamlit as st
import matplotlib.pyplot as plt


# define generic ploting function
def plot(x):
    fig, ax = plt.subplots()
    print(x)
    ax = plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    return fig


# create sidebar-selectbox for multi-pages
page = st.sidebar.selectbox(label='page', options=('Page One', 'Page Two'))

# define first page of app
if page == 'Page One':
    st.title(body='Plotting Page')

    # check if plot is already in session state
    if 'plot' in st.session_state:
        fig = st.session_state.plot
        st.pyplot(fig)
    elif st.button(label='Plot'):
        # create the plot then display it
        fig = plot(x=1)
        st.pyplot(fig)

        # save the plot to session state
        st.session_state.plot = fig

# define secon page of app
else:
    st.title(body='Second Page')
    if st.button(label='recall plot'):
        # recall plot from session state
        fig = st.session_state.plot
        st.pyplot(fig)