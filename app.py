import streamlit as st
import random
from datetime import datetime
from supabase import create_client

# ===== CONFIG =====
SUPABASE_URL = "https://dkqfjylacjxggcvsmvxg.supabase.co"
SUPABASE_KEY = "sb_publishable_d7FJwPUA7Hv7J5OnG69jug_Lfz2REYW"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

choices = [
    "Cơm tấm",
    "Bún chả",
    "Phở",
    "Bún riêu",
    "Cơm gà xối mỡ",
    "Bún cá"
]

def get_week():
    return datetime.now().isocalendar()[1]

def get_data():
    week = get_week()
    res = supabase.table("weekly_choices").select("*").eq("week", week).execute()

    if res.data:
        return res.data[0]
    else:
        new_data = {
            "week": week,
            "used": []
        }
        supabase.table("weekly_choices").insert(new_data).execute()
        return new_data

def update_data(used):
    week = get_week()
    supabase.table("weekly_choices").update({"used": used}).eq("week", week).execute()

def pick_today():
    data = get_data()
    used = data["used"]

    remaining = [c for c in choices if c not in used]

    if not remaining:
        used = []
        remaining = choices.copy()

    choice = random.choice(remaining)
    used.append(choice)

    update_data(used)

    return choice, used

# ===== UI =====
st.set_page_config(page_title="Hôm nay ăn gì?", page_icon="🍜")

st.title("🍜 Hôm nay ăn gì?")
st.caption("Random không trùng trong tuần")

if st.button("🎯 Chọn món hôm nay"):
    result, used = pick_today()
    st.success(f"👉 Hôm nay ăn: {result}")

if st.button("🔄 Reset tuần"):
    supabase.table("weekly_choices").update({"used": []}).eq("week", get_week()).execute()
    st.success("✅ Đã reset tuần!")

data = get_data()
st.write("📅 Đã ăn trong tuần:", data["used"])
