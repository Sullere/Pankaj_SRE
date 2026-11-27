import json
import os

DATA_FILE = "hospital_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"doctors": [], "patients": [], "appointments": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_doctor(data, name, specialization):
    doc_id = f"D{len(data['doctors']) + 1:03d}"
    doctor = {"id": doc_id, "name": name.strip(), "specialization": specialization.strip()}
    data["doctors"].append(doctor)
    save_data(data)
    return doctor


def add_patient(data, name, age, phone):
    pat_id = f"P{len(data['patients']) + 1:03d}"
    patient = {
        "id": pat_id,
        "name": name.strip(),
        "age": int(age),
        "phone": phone.strip(),
    }
    data["patients"].append(patient)
    save_data(data)
    return patient


def book_appointment(data, patient_id, doctor_id, date_str, time_str):
    patient_exists = any(p["id"] == patient_id for p in data["patients"])
    doctor_exists = any(d["id"] == doctor_id for d in data["doctors"])

    if not patient_exists:
        return None, f"Patient ID '{patient_id}' nahi mila."
    if not doctor_exists:
        return None, f"Doctor ID '{doctor_id}' nahi mila."

    for appt in data["appointments"]:
        if (
            appt["doctor_id"] == doctor_id
            and appt["date"] == date_str
            and appt["time"] == time_str
            and appt["status"] == "Booked"
        ):
            return None, "Is doctor ka yeh time slot already booked hai."

    appt_id = f"A{len(data['appointments']) + 1:03d}"
    appt = {
        "id": appt_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": date_str.strip(),
        "time": time_str.strip(),
        "status": "Booked",
    }
    data["appointments"].append(appt)
    save_data(data)
    return appt, "Appointment book ho gaya."


def list_appointments(data):
    if not data["appointments"]:
        print("\nKoi appointment nahi mila.")
        return

    print("\n--- Appointments ---")
    for appt in data["appointments"]:
        print(
            f"{appt['id']} | Patient: {appt['patient_id']} | Doctor: {appt['doctor_id']} "
            f"| {appt['date']} {appt['time']} | Status: {appt['status']}"
        )


def cancel_appointment(data, appt_id):
    for appt in data["appointments"]:
        if appt["id"] == appt_id:
            appt["status"] = "Cancelled"
            save_data(data)
            return True, f"Appointment {appt_id} cancel ho gaya."
    return False, f"Appointment ID '{appt_id}' nahi mila."


def main():
    data = load_data()

    while True:
        print("\n=== Hospital Management Menu ===")
        print("1. Add Doctor")
        print("2. Add Patient")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Cancel Appointment")
        print("6. Exit")

        choice = input("Choice enter karein (1-6): ").strip()

        if choice == "1":
            name = input("Doctor ka naam: ")
            spec = input("Specialization: ")
            doc = add_doctor(data, name, spec)
            print(f"Added: {doc['id']} - {doc['name']} ({doc['specialization']})")

        elif choice == "2":
            name = input("Patient ka naam: ")
            age = input("Age: ")
            phone = input("Phone: ")
            try:
                pat = add_patient(data, name, age, phone)
                print(f"Added: {pat['id']} - {pat['name']} (Age: {pat['age']})")
            except ValueError:
                print("Age number mein daalein.")

        elif choice == "3":
            pat_id = input("Patient ID (e.g. P001): ").strip().upper()
            doc_id = input("Doctor ID (e.g. D001): ").strip().upper()
            date_str = input("Date (YYYY-MM-DD): ")
            time_str = input("Time (e.g. 10:30 AM): ")
            appt, msg = book_appointment(data, pat_id, doc_id, date_str, time_str)
            print(msg)
            if appt:
                print(f"Booked ID: {appt['id']}")

        elif choice == "4":
            list_appointments(data)

        elif choice == "5":
            appt_id = input("Appointment ID to cancel (e.g. A001): ").strip().upper()
            _, msg = cancel_appointment(data, appt_id)
            print(msg)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice, 1 se 6 ke beech select karein.")

            from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    main()