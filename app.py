
import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from anomaly_detection import detect_anomaly

st.set_page_config(
    page_title="AI Digital Twin",
    page_icon="⚙️",
    layout="wide"
)

st.title("AI Driven Digital Twin")
st.subheader("Smart Factory Machine Monitoring Dashboard")
st.caption("Online demo | Simulated machine readings")

# Store readings during the current app session
if "history" not in st.session_state:
    st.session_state.history = []

# Generate one simulated machine reading
reading = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "temperature": round(random.uniform(50, 85), 2),
    "vibration": round(random.uniform(1, 4.5), 2),
    "rpm": random.randint(1200, 1800),
    "pressure": round(random.uniform(3, 6), 2),
}

st.session_state.history.append(reading)
st.session_state.history = st.session_state.history[-100:]

history = pd.DataFrame(st.session_state.history)
latest = history.iloc[-1]

temperature = float(latest["temperature"])
vibration = float(latest["vibration"])
rpm = float(latest["rpm"])
pressure = float(latest["pressure"])

status, reasons = detect_anomaly(
    temperature, vibration, rpm, pressure
)

st.divider()
st.subheader("Machine Status")

if status == "ANOMALY":
    st.error("AI ANOMALY DETECTED")
elif status == "WARNING":
    st.warning("AI WARNING")
else:
    st.success("AI NORMAL")

if reasons:
    st.write("Detected issues: " + ", ".join(reasons))

st.divider()
st.subheader("Live Sensor Readings")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Temperature", f"{temperature:.2f} °C")
col2.metric("Vibration", f"{vibration:.2f} mm/s")
col3.metric("RPM", f"{rpm}")
col4.metric("Pressure", f"{pressure:.2f} bar")

st.divider()
st.subheader("Machine Data Trend")

st.line_chart(
    history.set_index("timestamp")[
        ["temperature", "vibration", "rpm", "pressure"]
    ]
)

st.subheader("Latest Sensor Records")
st.dataframe(history.tail(10), width="stretch", hide_index=True)

st.caption("Refresh interval: 2 seconds | Demo data only")

time.sleep(2)
st.rerun()
