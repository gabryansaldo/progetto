import streamlit as st
from utils import load_dataset
from utils import units_per_day

def Daily_Statistics():
    load_dataset()
    st.write(units_per_day(st.session_state.passaggi))