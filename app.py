import streamlit as st
import random
import json
from datetime import datetime

choices = [
    "Cơm tấm",
    "Bún chả",
    "Phở",
    "Bún riêu",
    "Cơm gà xối mỡ",
    "Bún cá"
]

if "used" not in st.session_state:
    st.session_state.used = []

def pick_today():
    remaining = [c for c in choices if c not in st.session_state.used]

    if not remaining:
        st.session_state.used = []
        remaining = choices.copy()

    choice = random.choice(remaining)
    st.session_state.used.append(choice)

    return choice

def get_week():
    return datetime.now().isocalendar()[1]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"week": get_week(), "used": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def pick_today():
    data = load_data()
    current_week = get_week()

    if data["week"] != current_week:
        data = {"week": current_week, "used": []}

    remaining = [c for c in choices if c not in data["used"]]

    if not remaining:
        data["used"] = []
        remaining = choices.copy()

    choice = random.choice(remaining)
    data["used"].append(choice)

    save_data(data)
    return choice

# UI
st.title("🎯 Random lựa chọn trong tuần")

if st.button("👉 Chọn hôm nay"):
    result = pick_today()
    st.success(f"Hôm nay: {result}")

data = load_data()
st.write("📅 Đã chọn trong tuần:", data["used"])
