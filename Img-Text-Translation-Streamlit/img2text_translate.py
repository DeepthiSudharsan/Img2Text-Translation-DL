import streamlit as st
from multipage import MultiPage
from pages import img_translate, text_translate ,welcome # import your pages here

# Adding an image to the side bar 
st.sidebar.image("https://rb.gy/2wwoq1", width=None)

# Create an instance of the app 
app = MultiPage()
# Add all your application here
app.add_page("Welcome - Namaste - Vanakkam",welcome.app)
app.add_page("Translate text from Images", img_translate.app)
app.add_page("Translate text", text_translate.app)
@st.cache
# The main app
app.run()

st.sidebar.subheader("Respective Github Repo : ")
st.sidebar.markdown("[![Github](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJGtP-Pq0P67Ptyv3tB7Zn2ZYPIT-lPGI7AA&usqp=CAU)](https://github.com/DeepthiSudharsan/Img2Text-Translation-DL)")
