import csv
import os
from datetime import datetime

class Student:
    def __init__(self, id, name, roll_number, email, grade):
        self.id = id
        self.name = name
        self.roll_number = roll_number
        self.email = email
        self.grade = grade

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Roll: {self.roll_number}, Email: {self.email}, Grade: {self.grade}"

class StudentManagementSystem:
    def __init__(self, file_name="students.csv"):
        self.file_name = file_name
        self.students = []
        self.next_id = 1
        self.load_students()

    def load_students(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student = Student(
                        id=int(row['ID']),
                        name=row['Name'],
                        roll_number=row['Roll Number'],
                        email=row['Email'],
                        grade=row['Grade']
                    )
                    self.students.append(student)
                    if student.id >= self.next_id:
                        self.next_id = student.id + 1

    def save_students(self):
        with open(self.file_name, 'w', newline='') as file:
            fieldnames = ['ID', 'Name', 'Roll Number', 'Email', 'Grade']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in self.students:
                writer.writerow({
                    'ID': student.id,
                    'Name': student.name,
                    'Roll Number': student.roll_number,
                    'Email': student.email,
                    'Grade': student.grade
                })

    def add_student(self, name, roll_number, email, grade):
        new_student = Student(self.next_id, name, roll_number, email, grade)
        self.students.append(new_student)
        self.next_id += 1
        self.save_students()
        print("\nStudent added successfully!")

    def view_all_students(self):
        if not self.students:
            print("\nNo students in the system.")
            return
        print("\nAll Students:")
        for student in self.students:
            print(student)

    def search_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def update_student(self, student_id, **kwargs):
        student = self.search_student(student_id)
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            self.save_students()
            return True
        return False

    def delete_student(self, student_id):
        student = self.search_student(student_id)
        if student:
            self.students.remove(student)
            self.save_students()
            return True
        return False

    def generate_report(self, report_file="student_report.txt"):
        with open(report_file, 'w') as file:
            file.write(f"Student Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("="*50 + "\n")
            file.write(f"Total Students: {len(self.students)}\n\n")
            for student in self.students:
                file.write(f"ID: {student.id}\n")
                file.write(f"Name: {student.name}\n")
                file.write(f"Roll Number: {student.roll_number}\n")
                file.write(f"Email: {student.email}\n")
                file.write(f"Grade: {student.grade}\n")
                file.write("-"*50 + "\n")
        print(f"\nReport generated successfully: {report_file}")

def main():
    sms = StudentManagementSystem()

    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            name = input("Enter student name: ")
            roll_number = input("Enter roll number: ")
            email = input("Enter email: ")
            grade = input("Enter grade: ")
            sms.add_student(name, roll_number, email, grade)

        elif choice == '2':
            sms.view_all_students()

        elif choice == '3':
            student_id = int(input("Enter student ID to search: "))
            student = sms.search_student(student_id)
            if student:
                print("\nStudent Found:")
                print(student)
            else:
                print("\nStudent not found.")

        elif choice == '4':
            student_id = int(input("Enter student ID to update: "))
            student = sms.search_student(student_id)
            if student:
                print("\nLeave blank to keep current value")
                name = input(f"Enter new name ({student.name}): ") or student.name
                roll_number = input(f"Enter new roll number ({student.roll_number}): ") or student.roll_number
                email = input(f"Enter new email ({student.email}): ") or student.email
                grade = input(f"Enter new grade ({student.grade}): ") or student.grade
                sms.update_student(student_id, 
                                 name=name,
                                 roll_number=roll_number,
                                 email=email,
                                 grade=grade)
                print("\nStudent updated successfully!")
            else:
                print("\nStudent not found.")

        elif choice == '5':
            student_id = int(input("Enter student ID to delete: "))
            if sms.delete_student(student_id):
                print("\nStudent deleted successfully!")
            else:
                print("\nStudent not found.")

        elif choice == '6':
            sms.generate_report()

        elif choice == '7':
            print("\nExiting the system. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1-7.")

if __name__ == "__main__":
    main()