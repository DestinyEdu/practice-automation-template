#!/usr/bin/env python3
"""Generate fake appointments for demos. Uses obviously fake numbers (+27000000xxx).
Usage: python scripts/generate_demo_data.py [rows]  -> writes sheets/appointments.demo.csv
"""
import csv, random, sys
from datetime import datetime, timedelta

rows = int(sys.argv[1]) if len(sys.argv) > 1 else 20
random.seed(42)
first = ["Demo", "Sample", "Test"]
last = ["Patient", "Person", "Client"]
types = ["Consultation", "Follow-up", "Vaccination", "Check-up & clean", "Filling"]
statuses = ["booked", "confirmed", "cancelled", "no-show"]
fields = ["appointment_id","full_name","mobile","email","appointment_type","date_time","status","consent",
          "payment_type","medical_aid_name","medical_aid_number","medical_aid_check","booked_for",
          "patient_full_name","patient_age","reminder_48h_sent","reminder_2h_sent","notes_flag"]
start = datetime(2026, 10, 14, 8, 0)
with open("sheets/appointments.demo.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=fields)
    wr.writeheader()
    for i in range(1, rows + 1):
        aid = random.random() < 0.5
        wr.writerow({
            "appointment_id": f"D{i:04d}",
            "full_name": f"{random.choice(first)} {random.choice(last)} {i}",
            "mobile": f"+27000000{i:03d}",
            "email": f"demo{i}@example.com",
            "appointment_type": random.choice(types),
            "date_time": (start + timedelta(minutes=30 * i)).strftime("%Y-%m-%d %H:%M"),
            "status": random.choice(statuses),
            "consent": "yes",
            "payment_type": "medical_aid" if aid else "cash",
            "medical_aid_name": "DemoScheme" if aid else "",
            "medical_aid_number": f"DEMO-{i:04d}" if aid else "",
            "medical_aid_check": "funds available" if aid else "not needed",
            "booked_for": "self", "patient_full_name": "", "patient_age": "",
            "reminder_48h_sent": "", "reminder_2h_sent": "", "notes_flag": "",
        })
print(f"Wrote {rows} fake rows to sheets/appointments.demo.csv")
