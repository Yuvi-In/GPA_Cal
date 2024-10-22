import customtkinter as ctk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class GPACal(ctk.CTk):
    def __init__(self):
        super(GPACal, self).__init__()

        self.title("GPA Calculator")
        self.geometry("400x400")

        self.grade_label = ctk.CTkLabel(self, text="Grade:")
        self.grade_label.grid(row=0, column=0, padx=10, pady=10)
        self.grade_entry = ctk.CTkEntry(self)
        self.grade_entry.grid(row=0, column=2, padx=10, pady=10)

        self.credit_label = ctk.CTkLabel(self, text="Credit hours:")
        self.credit_label.grid(row=1, column=0, padx=10, pady=10)
        self.credit_entry = ctk.CTkEntry(self)
        self.credit_entry.grid(row=1, column=2, padx=10, pady=10)

        self.add_button = ctk.CTkButton(self, text="Add Course", command=self.add_course)
        self.add_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.course_list = ctk.CTkTextbox(self, height=70)
        self.course_list.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        self.calculate_button = ctk.CTkButton(self, text="Calculate GPA", command=self.calculate_gpa)
        self.calculate_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
        
        self.result_clear = ctk.CTkButton(self, text="Clear", command=self.clear_data)
        self.result_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.print_result = ctk.CTkButton(self, text="Print GPA result", command=self.print_gpa)
        self.print_result.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

        self.courses = []
        self.gpa_result= ""

    def add_course(self):
        if len(self.courses) < 4:
            try:
                grade = float(self.grade_entry.get())
                credits = float(self.credit_entry.get())
                self.courses.append((grade, credits))
                self.course_list.insert(ctk.END, f"Grade: {grade}, Credits: {credits}\n")
                self.grade_entry.delete(0, ctk.END)
                self.credit_entry.delete(0, ctk.END)
                self.course_list.delete(ctk.END)
            except ValueError:
                self.result_label.configure(text="Please enter valid values for grades and credits.")
        else:
            self.result_label.configure(text="Maximu 4 courses only.")

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for grade, credits in self.courses:
            total_points += grade * credits
            total_credits += credits
        if total_credits > 0:
            gpa = total_points / total_credits
            self.result_label.configure(text=f"Your GPA is {gpa:.2f}")
        else:
            self.result_label.configure(text="No course added yet.")
    
    '''def save_to_file(self, gpa):
        try:
            with open("gpa_result.txt", "w") as file:
                file.write("Course List and GPA Calculation:\n")
                for grade, credits in self.courses:
                    file.write(f"Grade: {grade}, Credits: {credits}\n")
                file.write(f"\nFinal GPA: {gpa:.2f}\n")
            self.result_label.configure(text="GPA result saved to 'gpa_result.txt'.")
        except Exception as e:
            self.result_label.configure(text=f"Error saving to file: {e}") '''
    
    def clear_data(self):
        self.courses = []
        self.credit_entry.delete(0, ctk.END)
        self.grade_entry.delete(0, ctk.END)

        self.course_list.delete(1.0, ctk.END)

        self.result_label.configure(text="Add new course")

    def print_gpa(self):
        # Create a PDF with course list and GPA
        pdf_filename = "GPA_Report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "GPA Report")

        # Course details
        y_position = height - 100
        c.setFont("Helvetica", 12)
        for idx, (grade, credits) in enumerate(self.courses, 1):
            course_text = f"Course {idx}: Grade = {grade}, Credits = {credits}"
            c.drawString(100, y_position, course_text)
            y_position -= 20
        
        # GPA result
        c.drawString(100, y_position - 20, self.gpa_result)
        
        # Save the PDF
        c.save()

        # Command to print the generated PDF (adjust for your OS)
        if os.name == 'nt':  # Windows
            os.startfile(pdf_filename, "print")
    """    elif os.name == 'posix':  # macOS/Linux
            os.system(f"lp {pdf_filename}")
    """


if __name__ == "__main__":
    app = GPACal()
    app.mainloop()
