import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
import uuid


# ---------------------------------------------------------
# PARAMETERS
# ---------------------------------------------------------

N = 5000

SEX = ["Male", "Female"]

DIAGNOSES = [
    "Malaria", "Typhoid", "URTI", "Pneumonia", "Diabetes Complication",
    "Hypertension", "Injury", "Pregnancy-related", "Gastroenteritis",
    "UTI", "COVID-19", "Non-specific Fever"
]

TRIAGE = ["Low", "Medium", "High", "Critical"]
TRIAGE_PROB = [0.55, 0.25, 0.15, 0.05]

DEPARTMENTS = ["OPD", "Emergency", "Pediatrics", "Maternity", "Surgery", "Diagnostics"]

LAB_TESTS = ["CBC", "Malaria RDT", "Blood Glucose", "Urinalysis", "Chest Xray", "COVID PCR"]

OUTCOMES = ["Discharged", "Admitted", "Referred", "Deceased"]
OUTCOME_PROB = [0.75, 0.18, 0.06, 0.01]


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def generate_age():
    """Generate age based on a realistic distribution skewed toward youth & adults."""
    age = np.random.choice(
        list(range(0, 95)),
        p=np.linspace(1, 0.1, 95) / np.linspace(1, 0.1, 95).sum()
    )
    return int(age)


def rand_time():
    """Generate time between 07:00 and 20:59."""
    hour = random.randint(7, 20)
    minute = random.randint(0, 59)
    return timedelta(hours=hour, minutes=minute)


def simulate_wait_time(triage):
    if triage == "Critical": return np.random.randint(1, 5)
    if triage == "High": return np.random.randint(5, 15)
    if triage == "Medium": return np.random.randint(10, 40)
    return np.random.randint(20, 120)


def simulate_consultation_time(age):
    """Older patients tend to take longer."""
    if age < 5: return np.random.randint(8, 20)
    if age < 18: return np.random.randint(6, 15)
    if age < 55: return np.random.randint(6, 18)
    return np.random.randint(12, 25)


def simulate_lab_turnaround(test):
    table = {
        "CBC": (30, 90),
        "Malaria RDT": (10, 20),
        "Blood Glucose": (5, 15),
        "Urinalysis": (20, 40),
        "Chest Xray": (25, 60),
        "COVID PCR": (180, 480)
    }
    return np.random.randint(*table[test])


def route_patient(triage, age):
    if triage == "Critical":
        return "Emergency"
    if age < 12:
        return "Pediatrics"
    if triage == "High":
        return random.choice(["Emergency", "Surgery"])
    if age > 60:
        return "OPD"
    return random.choice(DEPARTMENTS)


# ---------------------------------------------------------
# FULL SIMULATION
# ---------------------------------------------------------

def simulate_dataset(n=N):
    rows = []

    for _ in range(n):

        patient_id = str(uuid.uuid4())[:8]

        # date and arrival time
        visit_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))
        arrival_time = rand_time()
        arrival_dt = datetime.combine(visit_date.date(), datetime.min.time()) + arrival_time

        # demographics
        age = generate_age()
        sex = np.random.choice(SEX)

        # clinical workflow
        triage = np.random.choice(TRIAGE, p=TRIAGE_PROB)
        wait_time = simulate_wait_time(triage)
        consultation_time = simulate_consultation_time(age)

        # lab workflow
        tests = random.sample(LAB_TESTS, random.randint(1, 3))
        lab_turnaround = sum(simulate_lab_turnaround(t) for t in tests)

        # routing
        department = route_patient(triage, age)

        # timestamps
        consultation_start = arrival_dt + timedelta(minutes=wait_time)
        consultation_end = consultation_start + timedelta(minutes=consultation_time)
        departure_dt = consultation_end + timedelta(minutes=lab_turnaround)

        # clinical diagnosis and outcome
        diagnosis = random.choice(DIAGNOSES)
        outcome = np.random.choice(OUTCOMES, p=OUTCOME_PROB)

        # risk score based on triage
        risk = {
            "Low": np.random.uniform(0, 0.3),
            "Medium": np.random.uniform(0.3, 0.6),
            "High": np.random.uniform(0.6, 0.85),
            "Critical": np.random.uniform(0.85, 1.0)
        }[triage]

        rows.append({
            "patient_id": patient_id,
            "visit_date": visit_date.date(),
            "arrival_time": arrival_dt,
            "departure_time": departure_dt,
            "age": age,
            "sex": sex,
            "triage": triage,
            "department_routed": department,
            "wait_time_minutes": wait_time,
            "consultation_time_minutes": consultation_time,
            "lab_tests": ",".join(tests),
            "lab_turnaround_minutes": lab_turnaround,
            "diagnosis": diagnosis,
            "outcome": outcome,
            "total_visit_minutes": int((departure_dt - arrival_dt).total_seconds() / 60),
            "risk_score": round(risk, 3)
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

df = simulate_dataset()
print(df.head())
print("\nDataset shape:", df.shape)


# Optionally save to CSV
df.to_csv("simulated_healthcare_dataset.csv", index=False)

