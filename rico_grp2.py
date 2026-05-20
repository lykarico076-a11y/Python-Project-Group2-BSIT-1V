#Adrian Pagsuyuin
#Angel Hekari Valencia
#Era Bendejo
#Lyka Sophia Rico
#Marc Christian Jian Yape
#Ruzzel Nueva

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import re
import csv
from tkinter import filedialog

#1. Ang Database
import json

students = {}

current_folder = os.path.dirname(_file_)
DATA_FILE = os.path.join(current_folder, "student_database.json")

def load_data():
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                students = json.load(file)
        except Exception:
            students = {}

def save_data():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(students, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

load_data()

def convert_college_grade(percentage): #Auto convert from percentage grade to college grade format
    p = int(percentage)
    if p >= 97: return "1.00"
    elif p >= 94: return "1.25"
    elif p >= 91: return "1.50"
    elif p >= 88: return "1.75"
    elif p >= 85: return "2.00"
    elif p >= 82: return "2.25"
    elif p >= 79: return "2.50"
    elif p >= 76: return "2.75"
    elif p == 75: return "3.00"
    else: return "5.00"


#2. Dito po ang additional functions


def refresh_table():
    for item in student_table.get_children():
        student_table.delete(item)
    
    current_selected_term = term_combo.get()
    current_selected_section = section_combo.get() # <--- KUKUNIN NA RIN NATIN ANG SECTION
    
    total_students = 0
    total_percentage = 0
    
    for key, data in students.items():
        # --- BABASAHIN NA NIYA PAREHO ANG TERM AT SECTION ---
        if data["term"] == current_selected_term and data["section"] == current_selected_section:
            if data["grade"] == "5.00":
                row_tag = ("failed",) 
            else:
                row_tag = ("passed",) 
                
            student_table.insert('', tk.END, values=(data["name"], data["section"], data["term"], f"{data['percentage']}%", data["grade"]), tags=row_tag)
            
            total_students += 1
            total_percentage += int(data['percentage'])
            
    if total_students > 0:
        average = total_percentage / total_students
        summary_label.config(text=f"📊 Total Students: {total_students}   |   📈 Class Average: {average:.2f}%")
    else:
        summary_label.config(text="📊 Total Students: 0   |   📈 Class Average: 0.00%")
            
    
    if total_students > 0:
        average = total_percentage / total_students
     
        summary_label.config(text=f"📊 Total Students: {total_students}   |   📈 Class Average: {average:.2f}%")
    else:
    
        summary_label.config(text="📊 Total Students: 0   |   📈 Class Average: 0.00%")

def add_student():
    name = name_entry.get().strip()
    perc_str = grade_entry.get().strip()
    section = section_combo.get().strip()
    term = term_combo.get().strip() # <--- Kinuha ang piniling grading period
    
    # Check kung may blanko (isinama ang term)
    if not name or not perc_str or not section or not term:
        messagebox.showwarning("Input Error", "Please fill up all fields.")
        return
        
    if not re.match(r"^[A-Za-z\sñÑ]+$", name):
        messagebox.showerror("Invalid Name", "Student Name must only contain letters and spaces.")
        return
        
    if not perc_str.isdigit() or not (0 <= int(perc_str) <= 100):
        messagebox.showerror("Invalid Grade", "Grade must be a valid whole number from 0 to 100.")
        return

    college_grade = convert_college_grade(perc_str)
    
    # Isinama na ang "term" sa pag-save sa database natin
    unique_key = f"{name}_{term}" # Halimbawa: "Adrian_Midterms"
    students[unique_key] = {"name": name, "section": section, "term": term, "percentage": perc_str, "grade": college_grade}
    
    save_data() # <--- IDAGDAG ITO DITO

    messagebox.showinfo("Success", f"Added {name} for {term}.\nGrade: {perc_str}% -> {college_grade}")
    name_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)
    refresh_table()
    
def view_students():
    # Bubuo ito ng panibagong maliit na window para sa listahan
    view_window = tk.Toplevel(root)
    view_window.title("Student Records")
    view_window.geometry("300x400")
    view_window.configure(bg="#ECF0F1")
    
    list_text = tk.Text(view_window, font=("Consolas", 11), bg="#ECF0F1", fg="#2C3E50")
    list_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    if not students:
        list_text.insert(tk.END, "No students recorded yet.")
    else:
        list_text.insert(tk.END, "🎓 OFFICIAL STUDENT LIST 🎓\n\n")
        for name, grade in students.items():
            list_text.insert(tk.END, f"Name: {name}\nGrade: {grade}\n----------------------\n")
    
    # Para hindi ma-edit ng user ang listahan
    list_text.config(state=tk.DISABLED)

def search_student():
    query = search_entry.get().strip().lower() 
    if not query:
        refresh_table()
        return
        
    for item in student_table.get_children():
        student_table.delete(item)
        
    found = False
    for key, data in students.items():
        if query in data["name"].lower():
            if data["grade"] == "5.00":
                row_tag = ("failed",) 
            else:
                row_tag = ("passed",)
                
            
            student_table.insert('', tk.END, values=(data["name"], data["section"], data["term"], f"{data['percentage']}%", data["grade"]), tags=row_tag)
            found = True
            
    if not found:
        messagebox.showinfo("Not Found", "No student matches your search.")
        refresh_table()
        search_entry.delete(0, tk.END)

def clear_search():
    search_entry.delete(0, tk.END)
    refresh_table()

def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please click on a student's name in the table first before deleting.")
        return
        
    item_data = student_table.item(selected_item[0])
    student_name = str(item_data['values'][0]).strip() 
    student_term = str(item_data['values'][2]).strip()
    
    unique_key = f"{student_name}_{student_term}" 
    
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}'s {student_term} record?")
    if confirm:
        if unique_key in students: 
            del students[unique_key]
            save_data()
            messagebox.showinfo("Deleted", f"Successfully removed {student_name}'s record.")
            refresh_table()
            name_entry.delete(0, tk.END)
            grade_entry.delete(0, tk.END)

def update_student():
    selected = student_table.selection()
    new_perc_str = grade_entry.get().strip()
    
    if selected: #Kung may iniclick sa table
        item = student_table.item(selected[0])
        name = str(item['values'][0]).strip() 
        term = str(item['values'][2]).strip() 
    else: #Kung nag type lang sa text box
        name = name_entry.get().strip()
        term = term_combo.get().strip()
        
    unique_key = f"{name}_{term}" #Hahanapin natin ang Pangalan at Term nito
        
    if unique_key in students:
        if new_perc_str:
            if not new_perc_str.isdigit() or not (0 <= int(new_perc_str) <= 100):
                messagebox.showerror("Invalid Grade", "Grade must be a valid whole number from 0 to 100.")
                return
                
            new_college_grade = convert_college_grade(new_perc_str)
           
            students[unique_key]["percentage"] = new_perc_str
            students[unique_key]["grade"] = new_college_grade

            save_data()
            
            messagebox.showinfo("Updated", f"Successfully updated {name}'s {term} grade to {new_college_grade}.")
            name_entry.delete(0, tk.END)
            grade_entry.delete(0, tk.END)
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "Please enter the New Grade (Percentage).")
    else:
        messagebox.showwarning("Error", "Student not found in the database for this term.")

def export_to_csv():
    #Ichecheck kung may laman ang table
    if not student_table.get_children():
        messagebox.showwarning("No Data", "There is no data to export right now.")
        return
        
    #Papalabasin ang "Save As" popup para makapili ng folder
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", ".csv"), ("All Files", ".*")],
        title="Export Records to Excel/CSV"
    )
    
    if not filepath: #Kung nacancel ng user
        return
        
    try:
        # Dito nangyayari ang maayos na format to excel
        with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
            
            file.write("sep=,\n") 
            
            writer = csv.writer(file)
            
            # Isulat ang mga Headers
            writer.writerow(["Student Name", "Course & Section", "Grading Period", "Percentage", "Final Grade"])
            
            # I-loop at isulat ang mga estudyante
            for row_id in student_table.get_children():
                row_data = student_table.item(row_id)['values']
                writer.writerow(row_data)
                
        messagebox.showinfo("Export Successful", f"Records successfully exported to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred:\n{e}")


#3. UI Design dito

root = tk.Tk()
root.title("PTC Student Management System")
root.geometry("1200x700")
root.state('zoomed')
root.configure(bg="#ECF0F1")
root.withdraw()
root.title("PTC Student Management System")
root.geometry("1200x700") 

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", foreground="black", background="white", fieldbackground="white", rowheight=35, font=('Arial', 11))
style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))

THEME_COLOR = "#52D053" 
TEXT_COLOR = "#1A252C" 

left_frame = tk.Frame(root, bg=THEME_COLOR, width=380)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#PTC LOGO
current_folder = os.path.dirname(_file_)
image_path = os.path.join(current_folder, "logo-ptc.png")

try:
    large_logo_image = tk.PhotoImage(file=image_path)
    logo_subsampled = large_logo_image.subsample(4, 4) 
    
    logo_label = tk.Label(left_frame, image=logo_subsampled, bg=THEME_COLOR)
    logo_label.image = logo_subsampled 
    logo_label.pack(pady=(30, 5))
    
    root.iconphoto(False, large_logo_image) 
    
except Exception as e:
    print(f"Logo not found: {e}")

tk.Label(left_frame, text="Student Name:", font=("Arial", 12, "bold"), bg=THEME_COLOR, fg=TEXT_COLOR).pack()
name_entry = tk.Entry(left_frame, width=30, font=("Arial", 13))
name_entry.pack(pady=(5, 15), padx=20)

tk.Label(left_frame, text="Section:", font=("Arial", 12, "bold"), bg=THEME_COLOR, fg=TEXT_COLOR).pack()
section_combo = ttk.Combobox(left_frame, values=["BSIT 1V", "BSIT 1B", "BSOA 1C", "BSOA 1E", "CCS 1A", "CCS 1O"], font=("Arial", 12), state="readonly", width=31)
section_combo.pack(pady=(5, 15), padx=20)
section_combo.current(0)
section_combo.bind("<<ComboboxSelected>>", lambda event: refresh_table())
tk.Label(left_frame, text="Grading Period:", font=("Arial", 12, "bold"), bg=THEME_COLOR, fg=TEXT_COLOR).pack()
term_combo = ttk.Combobox(left_frame, values=["Midterms", "Finals"], font=("Arial", 12), state="readonly", width=31)
term_combo.pack(pady=(5, 15), padx=20)
term_combo.current(0)
term_combo.bind("<<ComboboxSelected>>", lambda event: refresh_table())

tk.Label(left_frame, text="Grade (Percentage 0-100):", font=("Arial", 12, "bold"), bg=THEME_COLOR, fg=TEXT_COLOR).pack()
grade_entry = tk.Entry(left_frame, width=30, font=("Arial", 13))
grade_entry.pack(pady=(5, 15), padx=20)

tk.Label(left_frame, text="", bg=THEME_COLOR).pack() 
#Mga Buttons
tk.Button(left_frame, text="➕ Add Record", command=add_student, width=22, bg="#27AE60", fg="white", font=("Arial", 12, "bold"), borderwidth=3).pack(pady=8)
tk.Button(left_frame, text="✏️ Update Grade", command=update_student, width=22, bg="#8E44AD", fg="white", font=("Arial", 12, "bold"), borderwidth=3).pack(pady=8)
tk.Button(left_frame, text="🗑️ Delete Selected", command=delete_student, width=22, bg="#E74C3C", fg="white", font=("Arial", 12, "bold"), borderwidth=3).pack(pady=8)
tk.Button(left_frame, text="💾 Export to Excel (CSV)", command=export_to_csv, width=22, bg="#2980B9", fg="white", font=("Arial", 12, "bold"), borderwidth=3).pack(pady=15)


tk.Label(left_frame, text="", bg=THEME_COLOR).pack(fill=tk.Y, expand=True)

tk.Button(left_frame, text="Exit Portal", command=root.quit, width=15, font=("Arial", 11), bg="#7F8C8D", fg="white", borderwidth=3).pack(pady=10)
tk.Label(left_frame, text="Developed by: Group 2 - BSIT 1V", font=("Arial", 10, "italic"), bg=THEME_COLOR, fg=TEXT_COLOR).pack(pady=20)

#Dito nakapwesto search bar at table ruzzel
tk.Label(right_frame, text="Class Record Database", font=("Helvetica", 20, "bold"), bg="white", fg="#2C3E50").pack(pady=(25, 10))
summary_label = tk.Label(right_frame, text="📊 Total Students: 0   |   📈 Class Average: 0.00%", font=("Arial", 12, "bold"), bg="#E8F8F5", fg="#117A65", padx=15, pady=5, relief="solid", borderwidth=1)
summary_label.pack(pady=(0, 10))

#search bar ito
search_frame = tk.Frame(right_frame, bg="white")
search_frame.pack(fill=tk.X, padx=30, pady=10)

tk.Label(search_frame, text="🔍 Search:", font=("Arial", 13, "bold"), bg="white", fg="#2C3E50").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, font=("Arial", 13), width=40)
search_entry.pack(side=tk.LEFT, padx=10)
tk.Button(search_frame, text="Search", command=search_student, bg="#F39C12", fg="white", font=("Arial", 11, "bold"), borderwidth=3).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Clear", command=clear_search, bg="#7F8C8D", fg="white", font=("Arial", 11), borderwidth=3).pack(side=tk.LEFT)

#Table dito este class records
columns = ("Name", "Section", "Term", "Percentage", "Grade") # Idinagdag ang "Term"
student_table = ttk.Treeview(right_frame, columns=columns, show="headings")

student_table.heading("Name", text="Student Name")
student_table.heading("Section", text="COURSE & SECTION")
student_table.heading("Term", text="GRADING PERIOD") # Bagong header
student_table.heading("Percentage", text="PERCENTAGE")
student_table.heading("Grade", text="Final Grade")

#sizes ng mga columns
student_table.column("Name", width=250)
student_table.column("Section", width=140, anchor=tk.CENTER)
student_table.column("Term", width=130, anchor=tk.CENTER) # Bagong column size
student_table.column("Percentage", width=120, anchor=tk.CENTER)
student_table.column("Grade", width=120, anchor=tk.CENTER)

scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=student_table.yview)
student_table.tag_configure("failed", foreground="#E74C3C", font=('Arial', 11, 'bold')) # Kulay Pula at Bold kapag bagsak
student_table.tag_configure("passed", foreground="black") # Normal kapag pasado
student_table.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=(10, 30))

#4. Login screen dito
def show_login():
    login_win = tk.Toplevel()
    login_win.title("PTC Teacher Login")
    login_win.geometry("350x270")
    
    DARK_GREEN = "#145A32" 
    login_win.configure(bg=DARK_GREEN)
    login_win.resizable(False, False)
    login_win.grab_set() 
    
    #Logo Icon
    try:
        login_win.iconphoto(False, large_logo_image)
    except:
        pass

    tk.Label(login_win, text="🔒 SECURITY LOGIN", font=("Helvetica", 14, "bold"), bg=DARK_GREEN, fg="white").pack(pady=(20, 10))
    
    tk.Label(login_win, text="Username:", font=("Arial", 10), bg=DARK_GREEN, fg="white").pack()
    user_entry = tk.Entry(login_win, font=("Arial", 11), width=25)
    user_entry.pack(pady=5)
    
    tk.Label(login_win, text="Password:", font=("Arial", 10), bg=DARK_GREEN, fg="white").pack()
    pass_entry = tk.Entry(login_win, font=("Arial", 11), width=25, show="*")
    pass_entry.pack(pady=5)
    
    def check_credentials():
        if user_entry.get() == "teacher" and pass_entry.get() == "ptc123":
            messagebox.showinfo("Success", "Login Successful! Welcome to PTC Portal.")
            login_win.destroy() 
            root.deiconify()    
            root.state('zoomed') 
        else:
            messagebox.showerror("Access Denied", "Invalid Username or Password.")
            pass_entry.delete(0, tk.END) 
            
    tk.Button(login_win, text="LOGIN", command=check_credentials, bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=15, relief="raised").pack(pady=15)

def main():
    show_login() #Papalabasin ang login bago ang dashboard o portal
    root.mainloop()

if _name_ == "_main_":
    main()
