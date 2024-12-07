import streamlit as st
import utils
import base64
import pandas as pd
import numpy as np
import time
import altair as alt
import polars as pl

def Test():
    utils.load_dataset()
    st.markdown(
        f"""
        <div style="
            border-radius: 8px; 
            padding: 16px; 
            background-color: #f9f9f9; 
            margin-bottom: 16px;">
            <div style="display: flex;">
                <i class="icon" style="font-size: 36px; color: blue; margin-right: 16px;">🎈</i>
                <div>
                    <h4 style="margin: 0; color: blue;">Ciao a tutti caciotti</h4>
                    <p style="font-size: 40px; font-weight: bold; color: blue; text-align: right;">ho cacato fuori</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
