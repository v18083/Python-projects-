import json
import os

class StudentSystem:
    def __init__(self):
        self.students = {}
        self.filename = "students.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.students = json.load(file)
                print(f"Loaded {len(self.students)} students")
            except:
                print("Error loading data, starting fresh")
                self.students = {}
        else:
            print("No existing data found, starting fresh")
    
    def save_data(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.students, file, indent=2)
            return True
        except:
            print("Error saving data")
            return False
    
    def get_grade(self, average):
        if average >= 75:
            return "A"
        elif average >= 65:
            return "B"
        elif average >= 50:
            return "C"
        elif average >= 40:
            return "D"
        else:
            return "F"
    
    def calculate_average(self, subjects):
        if not subjects:
            return 0
        total = sum(subjects.values())
        return total / len(subjects)
    
    def validate_mark(self, mark):
        try:
            mark = float(mark)
            if 0 <= mark <= 100:
                return True, mark
            else:
                return False, "Marks must be 0-100"
        except:
            return False, "Please enter a number"
    
    def add_student(self):
        print("\n--- ADD NEW STUDENT ---")
        
        while True:
            student_id = input("Enter Student ID: ").strip().upper()
            if student_id == "":
                print("ID cannot be empty")
                continue
            if student_id in self.students:
                print("This ID already exists!")
                continue
            break
        
        while True:
            name = input("Enter Full Name: ").strip().title()
            if name == "":
                print("Name cannot be empty")
                continue
            break
        
        program = input("Enter Program/Class: ").strip().upper()
        
        subjects = {}
        print("\nEnter at least 3 subjects")
        
        count = 0
        while count < 3:
            subject = input(f"Subject {count + 1} name: ").strip().capitalize()
            if subject == "":
                print("Subject name cannot be empty")
                continue
            
            while True:
                mark_input = input(f"Mark for {subject} (0-100): ")
                valid, result = self.validate_mark(mark_input)
                if valid:
                    subjects[subject] = result
                    count += 1
                    break
                else:
                    print(result)
        
        while True:
            more = input("\nAdd more subjects? (y/n): ").lower()
            if more == 'y':
                subject = input("Subject name: ").strip().capitalize()
                while True:
                    mark_input = input(f"Mark for {subject}: ")
                    valid, result = self.validate_mark(mark_input)
                    if valid:
                        subjects[subject] = result
                        break
                    else:
                        print(result)
            elif more == 'n':
                break
            else:
                print("Please enter y or n")
        
        self.students[student_id] = {
            'id': student_id,
            'name': name,
            'program': program,
            'subjects': subjects
        }
        
        if self.save_data():
            print(f"\n✓ Student {name} added successfully!")
        else:
            print("\n✗ Failed to save student!")
    
    def view_all_students(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        print("\n--- ALL STUDENTS ---")
        for student_id, student in self.students.items():
            avg = self.calculate_average(student['subjects'])
            grade = self.get_grade(avg)
            print(f"\nID: {student_id}")
            print(f"Name: {student['name']}")
            print(f"Program: {student['program']}")
            print(f"Subjects: {len(student['subjects'])}")
            print(f"Average: {avg:.1f} | Grade: {grade}")
            print("-" * 30)
        
        print(f"\nTotal: {len(self.students)} students")
    
    def view_student_report(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        student_id = input("Enter Student ID: ").strip().upper()
        
        if student_id not in self.students:
            print("Student not found!")
            return
        
        student = self.students[student_id]
        
        print(f"\n--- STUDENT REPORT ---")
        print(f"Name: {student['name']}")
        print(f"ID: {student['id']}")
        print(f"Program: {student['program']}")
        print("\nSubjects and Marks:")
        print("-" * 25)
        
        total = 0
        for subject, mark in student['subjects'].items():
            print(f"{subject}: {mark}")
            total += mark
        
        avg = total / len(student['subjects'])
        grade = self.get_grade(avg)
        
        print("-" * 25)
        print(f"Total Marks: {total}")
        print(f"Average: {avg:.1f}")
        print(f"Grade: {grade}")
    
    def update_student(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        student_id = input("Enter Student ID: ").strip().upper()
        
        if student_id not in self.students:
            print("Student not found!")
            return
        
        student = self.students[student_id]
        
        print(f"\n--- UPDATE {student['name']} ---")
        print("1. Update marks")
        print("2. Add new subject")
        print("3. Remove subject")
        print("4. Update name")
        print("5. Update program")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == '1':
            print("\nCurrent subjects:")
            for subject in student['subjects']:
                print(f"- {subject}")
            
            subject = input("\nSubject to update: ").strip().capitalize()
            if subject in student['subjects']:
                while True:
                    mark = input(f"New mark for {subject}: ")
                    valid, result = self.validate_mark(mark)
                    if valid:
                        student['subjects'][subject] = result
                        print(f"✓ {subject} updated to {result}")
                        break
                    else:
                        print(result)
            else:
                print("Subject not found!")
        
        elif choice == '2':
            subject = input("New subject name: ").strip().capitalize()
            if subject in student['subjects']:
                print("Subject already exists!")
            else:
                while True:
                    mark = input(f"Mark for {subject}: ")
                    valid, result = self.validate_mark(mark)
                    if valid:
                        student['subjects'][subject] = result
                        print(f"✓ Added {subject} with mark {result}")
                        break
                    else:
                        print(result)
        
        elif choice == '3':
            print("\nCurrent subjects:")
            for subject in student['subjects']:
                print(f"- {subject}")
            
            subject = input("\nSubject to remove: ").strip().capitalize()
            if subject in student['subjects']:
                if len(student['subjects']) <= 1:
                    print("Cannot remove - student needs at least 1 subject!")
                else:
                    confirm = input(f"Remove {subject}? (y/n): ").lower()
                    if confirm == 'y':
                        del student['subjects'][subject]
                        print(f"✓ Removed {subject}")
            else:
                print("Subject not found!")
        
        elif choice == '4':
            new_name = input("New name: ").strip().title()
            if new_name:
                student['name'] = new_name
                print(f"✓ Name updated to {new_name}")
        
        elif choice == '5':
            new_program = input("New program: ").strip().upper()
            if new_program:
                student['program'] = new_program
                print(f"✓ Program updated to {new_program}")
        
        else:
            print("Invalid choice!")
            return
        
        self.save_data()
    
    def delete_student(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        student_id = input("Enter Student ID to delete: ").strip().upper()
        
        if student_id not in self.students:
            print("Student not found!")
            return
        
        student_name = self.students[student_id]['name']
        confirm = input(f"Delete {student_name}? (y/n): ").lower()
        
        if confirm == 'y':
            del self.students[student_id]
            self.save_data()
            print(f"✓ {student_name} deleted successfully!")
        else:
            print("Deletion cancelled")
    
    def search_student(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        print("\n--- SEARCH STUDENT ---")
        print("1. Search by ID")
        print("2. Search by Name")
        
        choice = input("\nChoose option (1-2): ").strip()
        
        if choice == '1':
            student_id = input("Enter Student ID: ").strip().upper()
            if student_id in self.students:
                student = self.students[student_id]
                print(f"\nFound: {student['name']} ({student['id']})")
                print(f"Program: {student['program']}")
            else:
                print("Student not found!")
        
        elif choice == '2':
            name_search = input("Enter name to search: ").strip().lower()
            found = []
            
            for student in self.students.values():
                if name_search in student['name'].lower():
                    found.append(student)
            
            if found:
                print(f"\nFound {len(found)} student(s):")
                for student in found:
                    print(f"- {student['name']} (ID: {student['id']})")
            else:
                print("No students found!")
        
        else:
            print("Invalid choice!")
    
    def rank_students(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        rankings = []
        for student in self.students.values():
            avg = self.calculate_average(student['subjects'])
            rankings.append((student['name'], student['id'], avg))
        
        rankings.sort(key=lambda x: x[2], reverse=True)
        
        print("\n--- STUDENT RANKINGS ---")
        print(f"{'Rank':<6} {'Name':<25} {'Average':<10} {'Grade'}")
        print("-" * 50)
        
        for i, (name, sid, avg) in enumerate(rankings, 1):
            grade = self.get_grade(avg)
            print(f"{i:<6} {name:<25} {avg:<10.1f} {grade}")
        
        if rankings:
            print("\n" + "=" * 50)
            print(f"🏆 TOP STUDENT: {rankings[0][0]} (ID: {rankings[0][1]})")
            print(f"   Average: {rankings[0][2]:.1f}")
            print(f"   Grade: {self.get_grade(rankings[0][2])}")
    
    def class_statistics(self):
        if not self.students:
            print("\nNo students found!")
            return
        
        averages = []
        for student in self.students.values():
            avg = self.calculate_average(student['subjects'])
            averages.append(avg)
        
        if not averages:
            print("No data available!")
            return
        
        print("\n--- CLASS STATISTICS ---")
        print(f"Total Students: {len(self.students)}")
        print(f"Class Average: {sum(averages)/len(averages):.1f}")
        print(f"Highest Average: {max(averages):.1f}")
        print(f"Lowest Average: {min(averages):.1f}")
        
        grades = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for avg in averages:
            grade = self.get_grade(avg)
            grades[grade] += 1
        
        print("\nGrade Distribution:")
        for grade in ['A', 'B', 'C', 'D', 'F']:
            if grades[grade] > 0:
                percent = (grades[grade] / len(averages)) * 100
                print(f"{grade}: {grades[grade]} students ({percent:.1f}%)")
    
    def show_menu(self):
        print("\n" + "=" * 50)
        print("STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student Report")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search Student")
        print("7. Rank Students")
        print("8. Class Statistics")
        print("9. Exit")
        print("=" * 50)
    
    def run(self):
        print("\n" + "=" * 50)
        print("WELCOME TO STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        
        while True:
            self.show_menu()
            choice = input("\nEnter choice (1-9): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.view_student_report()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.search_student()
            elif choice == '7':
                self.rank_students()
            elif choice == '8':
                self.class_statistics()
            elif choice == '9':
                print("\nThank you for using the system!")
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1-9")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    system = StudentSystem()
    system.run()
