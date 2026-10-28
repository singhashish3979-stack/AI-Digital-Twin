import streamlit as st
import pandas as pd
import json
import time
from pathlib import Path

from anomaly_detection import detect_anomaly


# =============================
# PAGE SETTINGS
# =============================

st.set_page_config(
    page_title="AI Digital Twin",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ AI Driven Digital Twin")
st.subheader("Smart Factory Machine Monitoring Dashboard")


# =============================
# FILE PATHS
# =============================

BASE_DIR = Path(__file__).parent

LIVE_FILE = BASE_DIR / "live_data.json"
HISTORY_FILE = BASE_DIR / "machine_data.csv"


# =============================
# READ LIVE DATA
# =============================

if not LIVE_FILE.exists():

    st.warning("Waiting for live machine data...")

    time.sleep(2)
    st.rerun()


try:

    with open(LIVE_FILE, "r") as file:
        latest = json.load(file)

except Exception:

    st.warning("Reading live machine data...")

    time.sleep(2)
    st.rerun()


# =============================
# SENSOR VALUES
# =============================

temperature = float(latest.get("temperature", 0))
vibration = float(latest.get("vibration", 0))
rpm = float(latest.get("rpm", 0))
pressure = float(latest.get("pressure", 0))


# =============================
# AI ANOMALY DETECTION
# =============================

status, reasons = detect_anomaly(
    temperature,
    vibration,
    rpm,
    pressure
)


if status == "ANOMALY":

    display_status = "🔴 AI ANOMALY DETECTED"

elif status == "WARNING":

    display_status = "🟡 AI WARNING"

else:

    display_status = "🟢 AI NORMAL"


# =============================
# LIVE SENSOR CARDS
# =============================

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌡️ Temperature",
        f"{temperature:.2f} °C"
    )


with col2:

    st.metric(
        "📳 Vibration",
        f"{vibration:.2f} mm/s"
    )


with col3:

    st.metric(
        "⚙️ RPM",
        f"{rpm:.0f}"
    )


with col4:

    st.metric(
        "🔵 Pressure",
        f"{pressure:.2f} bar"
    )


# =============================
# AI STATUS
# =============================

st.divider()

st.subheader("Machine Status")

st.markdown(f"# {display_status}")


if reasons:

    st.write("**AI Detection Reason:**")

    for reason in reasons:

        st.write("⚠️", reason)

else:

    st.write("AI detected no abnormal machine condition.")


# =============================
# SAVE HISTORY
# =============================

new_data = pd.DataFrame([
    {
        "temperature": temperature,
        "vibration": vibration,
        "rpm": rpm,
        "pressure": pressure
    }
])


if HISTORY_FILE.exists():

    try:

        old_data = pd.read_csv(HISTORY_FILE)

        history = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )

    except Exception:

        history = new_data

else:

    history = new_data


history = history.tail(100)

history.to_csv(
    HISTORY_FILE,
    index=False
)


# =============================
# LIVE CHART
# =============================

st.divider()

st.subheader("📊 Live Machine Data")

st.line_chart(
    history[
        [
            "temperature",
            "vibration",
            "rpm",
            "pressure"
        ]
    ]
)


# =============================
# RECENT DATA
# =============================

st.subheader("Latest Sensor Records")

st.dataframe(
    history.tail(10),
    width="stretch"
)


# =============================
# AUTO REFRESH
# =============================

time.sleep(2)

st.rerun()