import streamlit as st
from pathlib import Path
import os
print()

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

intro_markdown = read_markdown_file(f"{os.getcwd()}/paper/README.md")
st.markdown(intro_markdown, unsafe_allow_html=True)
