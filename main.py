import json
import csv
import os
from datetime import datetime


# ============================================================
# RUN 360
# Smart Attendance & Management System
# ============================================================


# ============================================================
# FILE NAMES
# ============================================================

STUDENT_FILE = "students.json"
EMPLOYEE_FILE = "employees.json"
TASK_FILE = "tasks.json"
EVENT_FILE = "events.json"
MARK_FILE = "marks.json"
TIMETABLE_FILE = "timetable.json"
ATTENDANCE_FILE = "attendance.csv"


# ============================================================
# GENERAL FILE FUNCTIONS
# ============================================================

def load_json(filename, default_data):

    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data

    try:
        with open(filename, "r") as file:
            return json.load(file)

    except:
        return default_data


def save_json(filename, data):

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# ============================================================
# LOAD ALL DATA
# ============================================================

students = load_json(STUDENT_FILE, {})
employees = load_json(EMPLOYEE_FILE, {})
tasks = load_json(TASK_FILE, {})
events = load_json(EVENT_FILE, {})
marks = load_json(MARK_FILE, {})
timetable = load_json(TIMETABLE_FILE, {})


# ============================================================
# ATTENDANCE CSV
# ============================================================

def create_attendance_file():

    if not os.path.exists(ATTENDANCE_FILE):

        with open(ATTENDANCE_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Name",
                "Mode",
                "Date",
                "Time",
                "Status"
            ])


def save_attendance(user_id, name, mode, status):

    create_attendance_file()

    now = datetime.now()

    with open(ATTENDANCE_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            user_id,
            name,
            mode,
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S"),
            status
        ])


# ============================================================
# STUDENT REGISTRATION
# ============================================================

def student_login():

    print("\n================================")
    print("       STUDENT LOGIN")
    print("================================")

    student_id = input("Enter Student ID: ").strip()

    # New student
    if student_id not in students:

        print("\nStudent not found.")

        name = input("Enter Student Name: ").strip()

        password = input("Create Password: ").strip()

        students[student_id] = {
            "name": name,
            "password": password
        }

        save_json(STUDENT_FILE, students)

        print("\nNew student added successfully!")

        return student_id

    # Existing student
    password = input("Enter Password: ").strip()

    if students[student_id]["password"] == password:

        print("\nLogin successful!")
        print("Welcome,", students[student_id]["name"])

        return student_id

    print("\nIncorrect password!")

    return None


# ============================================================
# STUDENT ATTENDANCE
# ============================================================

def mark_student_attendance(student_id):

    student = students[student_id]

    print("\n================================")
    print("       MARK ATTENDANCE")
    print("================================")

    print("1. Present")
    print("2. Absent")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":

        status = "Present"

        print("\nAttendance marked as PRESENT.")

    elif choice == "2":

        status = "Absent"

        print("\nAttendance marked as ABSENT.")

    else:

        print("\nInvalid choice.")
        return

    save_attendance(
        student_id,
        student["name"],
        "Student",
        status
    )


# ============================================================
# STUDENT ATTENDANCE REPORT
# ============================================================

def student_attendance_report(student_id):

    if not os.path.exists(ATTENDANCE_FILE):

        print("\nNo attendance records found.")
        return

    name = students[student_id]["name"]

    present = 0
    absent = 0

    with open(ATTENDANCE_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["ID"] == student_id and row["Mode"] == "Student":

                if row["Status"] == "Present":
                    present += 1

                elif row["Status"] == "Absent":
                    absent += 1

    total = present + absent

    if total > 0:
        percentage = (present / total) * 100
    else:
        percentage = 0

    print("\n================================")
    print("      ATTENDANCE REPORT")
    print("================================")

    print("Student ID:", student_id)
    print("Name:", name)
    print("Present:", present)
    print("Absent:", absent)
    print("Total Classes:", total)
    print("Attendance:", round(percentage, 2), "%")


# ============================================================
# ADD TASK
# ============================================================

def add_student_task(student_id):

    task = input("\nEnter new task: ").strip()

    if student_id not in tasks:
        tasks[student_id] = []

    tasks[student_id].append({
        "task": task,
        "completed": False
    })

    save_json(TASK_FILE, tasks)

    print("\nTask added successfully!")


# ============================================================
# VIEW TASKS
# ============================================================

def view_student_tasks(student_id):

    print("\n================================")
    print("          YOUR TASKS")
    print("================================")

    if student_id not in tasks or len(tasks[student_id]) == 0:

        print("No tasks available.")
        return

    for i, item in enumerate(tasks[student_id], 1):

        status = "Completed" if item["completed"] else "Pending"

        print(
            i,
            ".",
            item["task"],
            "-",
            status
        )


# ============================================================
# COMPLETE TASK
# ============================================================

def complete_student_task(student_id):

    if student_id not in tasks or len(tasks[student_id]) == 0:

        print("\nNo tasks available.")
        return

    view_student_tasks(student_id)

    try:

        number = int(
            input("\nEnter task number to complete: ")
        )

        if 1 <= number <= len(tasks[student_id]):

            tasks[student_id][number - 1]["completed"] = True

            save_json(TASK_FILE, tasks)

            print("\nTask completed!")

        else:

            print("\nInvalid task number.")

    except ValueError:

        print("\nPlease enter a number.")


# ============================================================
# ADD EVENT
# ============================================================

def add_student_event(student_id):

    event_name = input("\nEnter event name: ").strip()

    event_date = input("Enter event date: ").strip()

    if student_id not in events:
        events[student_id] = []

    events[student_id].append({
        "name": event_name,
        "date": event_date
    })

    save_json(EVENT_FILE, events)

    print("\nEvent added successfully!")


# ============================================================
# VIEW EVENTS
# ============================================================

def view_student_events(student_id):

    print("\n================================")
    print("         YOUR EVENTS")
    print("================================")

    if student_id not in events or len(events[student_id]) == 0:

        print("No events available.")
        return

    for i, event in enumerate(events[student_id], 1):

        print(
            i,
            ".",
            event["name"],
            "| Date:",
            event["date"]
        )


# ============================================================
# ADD MARKS
# ============================================================

def add_student_marks(student_id):

    subject = input("\nEnter subject: ").strip()

    try:

        score = float(input("Enter marks: "))

        if score < 0 or score > 100:

            print("\nMarks must be between 0 and 100.")
            return

    except ValueError:

        print("\nInvalid marks.")
        return

    if student_id not in marks:
        marks[student_id] = {}

    marks[student_id][subject] = score

    save_json(MARK_FILE, marks)

    print("\nMarks saved successfully!")


# ============================================================
# VIEW MARKS
# ============================================================

def view_student_marks(student_id):

    print("\n================================")
    print("      ACADEMIC PERFORMANCE")
    print("================================")

    if student_id not in marks or len(marks[student_id]) == 0:

        print("No marks available.")
        return

    total = 0

    for subject, score in marks[student_id].items():

        print(subject, ":", score)

        total += score

    average = total / len(marks[student_id])

    print("\nAverage Marks:", round(average, 2))


# ============================================================
# ADD TIMETABLE
# ============================================================

def add_timetable(student_id):

    day = input("\nEnter day: ").strip()

    subject = input("Enter subject/class: ").strip()

    if student_id not in timetable:
        timetable[student_id] = {}

    if day not in timetable[student_id]:
        timetable[student_id][day] = []

    timetable[student_id][day].append(subject)

    save_json(TIMETABLE_FILE, timetable)

    print("\nTimetable updated successfully!")


# ============================================================
# VIEW TIMETABLE
# ============================================================

def view_timetable(student_id):

    print("\n================================")
    print("          TIMETABLE")
    print("================================")

    if student_id not in timetable:

        print("No timetable available.")
        return

    for day, subjects in timetable[student_id].items():

        print("\n", day)

        for subject in subjects:

            print(" -", subject)


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_mode():

    student_id = student_login()

    if student_id is None:
        return

    while True:

        print("\n================================")
        print("       STUDENT DASHBOARD")
        print("================================")

        print("1. Mark Attendance")
        print("2. Attendance Report")
        print("3. Add Task")
        print("4. View Tasks")
        print("5. Complete Task")
        print("6. Add Event")
        print("7. View Events")
        print("8. Add Marks")
        print("9. View Marks")
        print("10. Add Timetable")
        print("11. View Timetable")
        print("12. Logout")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            mark_student_attendance(student_id)

        elif choice == "2":

            student_attendance_report(student_id)

        elif choice == "3":

            add_student_task(student_id)

        elif choice == "4":

            view_student_tasks(student_id)

        elif choice == "5":

            complete_student_task(student_id)

        elif choice == "6":

            add_student_event(student_id)

        elif choice == "7":

            view_student_events(student_id)

        elif choice == "8":

            add_student_marks(student_id)

        elif choice == "9":

            view_student_marks(student_id)

        elif choice == "10":

            add_timetable(student_id)

        elif choice == "11":

            view_timetable(student_id)

        elif choice == "12":

            print("\nLogged out successfully.")
            break

        else:

            print("\nInvalid choice!")


# ============================================================
# EMPLOYEE LOGIN / REGISTRATION
# ============================================================

def employee_login():

    print("\n================================")
    print("      INDUSTRIAL LOGIN")
    print("================================")

    employee_id = input("Enter Employee ID: ").strip()

    # New employee
    if employee_id not in employees:

        print("\nEmployee not found.")

        name = input("Enter Employee Name: ").strip()

        password = input("Create Password: ").strip()

        shift = input(
            "Enter Shift (Morning/Evening/Night): "
        ).strip()

        employees[employee_id] = {
            "name": name,
            "password": password,
            "shift": shift,
            "check_in": None
        }

        save_json(EMPLOYEE_FILE, employees)

        print("\nNew employee added successfully!")

        return employee_id

    password = input("Enter Password: ").strip()

    if employees[employee_id]["password"] == password:

        print("\nLogin successful!")
        print("Welcome,", employees[employee_id]["name"])

        return employee_id

    print("\nIncorrect password!")

    return None


# ============================================================
# EMPLOYEE CHECK-IN
# ============================================================

def employee_check_in(employee_id):

    employee = employees[employee_id]

    if employee.get("check_in") is not None:

        print("\nAlready checked in.")
        return

    current_time = datetime.now()

    employee["check_in"] = current_time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    save_json(EMPLOYEE_FILE, employees)

    save_attendance(
        employee_id,
        employee["name"],
        "Industrial",
        "Present"
    )

    print("\nCheck-in successful!")
    print(
        "Time:",
        current_time.strftime("%H:%M:%S")
    )


# ============================================================
# EMPLOYEE CHECK-OUT
# ============================================================

def employee_check_out(employee_id):

    employee = employees[employee_id]

    if employee.get("check_in") is None:

        print("\nPlease check-in first.")
        return

    check_in = datetime.strptime(
        employee["check_in"],
        "%Y-%m-%d %H:%M:%S"
    )

    check_out = datetime.now()

    difference = check_out - check_in

    total_seconds = int(difference.total_seconds())

    hours = total_seconds // 3600

    minutes = (total_seconds % 3600) // 60

    employee["check_in"] = None

    save_json(EMPLOYEE_FILE, employees)

    save_attendance(
        employee_id,
        employee["name"],
        "Industrial",
        "Check-Out"
    )

    print("\nCheck-out successful!")

    print(
        "Working Time:",
        hours,
        "hours",
        minutes,
        "minutes"
    )


# ============================================================
# EMPLOYEE ATTENDANCE REPORT
# ============================================================

def employee_attendance_report(employee_id):

    if not os.path.exists(ATTENDANCE_FILE):

        print("\nNo attendance records.")
        return

    name = employees[employee_id]["name"]

    present = 0

    with open(ATTENDANCE_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["ID"] == employee_id
                and row["Mode"] == "Industrial"
                and row["Status"] == "Present"
            ):

                present += 1

    print("\n================================")
    print("     EMPLOYEE ATTENDANCE")
    print("================================")

    print("Employee ID:", employee_id)
    print("Name:", name)
    print("Present Days:", present)


# ============================================================
# VIEW SHIFT
# ============================================================

def view_shift(employee_id):

    employee = employees[employee_id]

    print("\n================================")
    print("        SHIFT DETAILS")
    print("================================")

    print("Employee:", employee["name"])
    print("Shift:", employee["shift"])


# ============================================================
# EMPLOYEE TASK
# ============================================================

def add_employee_task(employee_id):

    task = input("\nEnter work task: ").strip()

    if employee_id not in tasks:
        tasks[employee_id] = []

    tasks[employee_id].append({
        "task": task,
        "completed": False
    })

    save_json(TASK_FILE, tasks)

    print("\nWork task added!")


def view_employee_tasks(employee_id):

    print("\n================================")
    print("          WORK TASKS")
    print("================================")

    if employee_id not in tasks:

        print("No work tasks.")
        return

    for i, item in enumerate(tasks[employee_id], 1):

        status = "Completed" if item["completed"] else "Pending"

        print(
            i,
            ".",
            item["task"],
            "-",
            status
        )


# ============================================================
# INDUSTRIAL MODE
# ============================================================

def industrial_mode():

    employee_id = employee_login()

    if employee_id is None:
        return

    while True:

        print("\n================================")
        print("       INDUSTRIAL MODE")
        print("================================")

        print("1. Check-In")
        print("2. Check-Out")
        print("3. Attendance Report")
        print("4. View Shift")
        print("5. Add Work Task")
        print("6. View Work Tasks")
        print("7. Logout")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            employee_check_in(employee_id)

        elif choice == "2":

            employee_check_out(employee_id)

        elif choice == "3":

            employee_attendance_report(employee_id)

        elif choice == "4":

            view_shift(employee_id)

        elif choice == "5":

            add_employee_task(employee_id)

        elif choice == "6":

            view_employee_tasks(employee_id)

        elif choice == "7":

            print("\nLogged out successfully.")
            break

        else:

            print("\nInvalid choice!")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    create_attendance_file()

    while True:

        print("\n")
        print("==============================================")
        print("                 RUN 360")
        print("     Smart Attendance & Management System")
        print("==============================================")

        print("\n1. Student Mode")
        print("2. Industrial Mode")
        print("3. Exit")

        choice = input("\nSelect Mode: ").strip()

        if choice == "1":

            student_mode()

        elif choice == "2":

            industrial_mode()

        elif choice == "3":

            print("\nThank you for using RUN 360!")
            break

        else:

            print("\nInvalid choice!")


# ============================================================
# START PROGRAM
# ============================================================

main()
