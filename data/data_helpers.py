from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import json
import gspread
from google.oauth2.service_account import Credentials

from utils.name_generator import generate_random_name

SHEET_ID = "19VAZuWBnzWHMfWsM7gq97AqdgNDPNviotSIOBrVZYzk"
SHEET_NAME = "Sheet1"

@st.cache_resource
def get_gspread_client():
    if "connections" not in st.secrets or "gsheets" not in st.secrets.connections:
        st.error("❌ Secrets not found. Check .streamlit/secrets.toml")
        st.stop()

    secrets_dict = dict(st.secrets.connections.gsheets)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_info(secrets_dict, scopes=scopes)
    return gspread.authorize(creds)


def save_score(seq: int, player_name: str, score: int, iterations: int, coords: np.ndarray):
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Get date
    date = datetime.now().strftime("%m/%d/%Y")

    # Convert coords to list, then json string
    coords_list = coords.tolist()
    coords_json = json.dumps(coords_list)

    # Row to add
    new_row = [seq, player_name, score, iterations, coords_json, date]

    try:
        # Existing data
        old_data = conn.read(worksheet="Sheet1", ttl=0)

        # New data as df
        new_data = pd.DataFrame([new_row],
                               columns=old_data.columns)

        # Append new row to df
        updated_df = pd.concat([old_data, new_data], ignore_index=True)

        # Update df
        conn.update(worksheet="Sheet1", data=updated_df)

        # Reset cache
        st.cache_data.clear()

        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

@st.cache_data(ttl=60) # Keep data for at least 60 seconds before fetching new data
def load_data():
    client = get_gspread_client()
    try:
        # Open the sheet
        workbook = client.open_by_key(SHEET_ID)
        sheet = workbook.worksheet(SHEET_NAME)

        # Get all records
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()