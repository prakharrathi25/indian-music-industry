import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import scrape_playlist_data # import your pages here

# Title of the main page
st.title("Streamlit Data Collection")
