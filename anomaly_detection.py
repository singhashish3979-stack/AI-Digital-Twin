import pandas as pd


def detect_anomaly(temperature, vibration, rpm, pressure):

    reasons = []

    # Temperature
    if temperature > 80:
        reasons.append("High Temperature")

    # Vibration
    if vibration > 4:
        reasons.append("High Vibration")

    # RPM
    if rpm > 1800 or rpm < 1000:
        reasons.append("Abnormal RPM")

    # Pressure
    if pressure > 7 or pressure < 2:
        reasons.append("Abnormal Pressure")

    # Final decision
    if len(reasons) >= 2:
        status = "ANOMALY"

    elif len(reasons) == 1:
        status = "WARNING"

    else:
        status = "NORMAL"

    return status, reasons