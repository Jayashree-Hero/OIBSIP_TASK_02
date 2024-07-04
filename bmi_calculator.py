import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                date TEXT NOT NULL)''')
conn.commit()

class BMICalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("400x300")
        self.configure(bg="#D8BFD8") 
        self.create_widgets()

    def create_widgets(self):
        label_style = {'bg': "#D8BFD8", 'font': ("Helvetica", 12, "bold")}  

        tk.Label(self, text="Name", **label_style).grid(row=0, column=0, pady=5)
        tk.Label(self, text="Weight (kg)", **label_style).grid(row=1, column=0, pady=5)
        tk.Label(self, text="Height (cm)", **label_style).grid(row=2, column=0, pady=5)

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, pady=5)

        self.weight_entry = tk.Entry(self)
        self.weight_entry.grid(row=1, column=1, pady=5)

        self.height_entry = tk.Entry(self)
        self.height_entry.grid(row=2, column=1, pady=5)

        self.result_label = tk.Label(self, text="", bg="#D8BFD8", font=("Helvetica", 12, "bold"))
        self.result_label.grid(row=3, columnspan=2, pady=10)

        button_style = {'bg': "#9370DB", 'fg': "white", 'font': ("Helvetica", 10, "bold"), 'width': 20, 'height': 2}
        tk.Button(self, text="Calculate BMI", command=self.calculate_bmi, **button_style).grid(row=4, columnspan=2, pady=5)
        tk.Button(self, text="View History", command=self.view_history, **button_style).grid(row=5, columnspan=2, pady=5)
        tk.Button(self, text="Analyze Trends", command=self.analyze_trends, **button_style).grid(row=6, columnspan=2, pady=5)

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100

            bmi = weight / (height * height)
            bmi = round(bmi, 2)

            self.result_label.config(text=f"Your BMI: {bmi}")

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute('INSERT INTO bmi_records (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)', 
                         (name, weight, height, bmi, date))
            conn.commit()

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for weight and height.")

    def view_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("BMI History")
        history_window.configure(bg="#D8BFD8") 

        c.execute('SELECT * FROM bmi_records')
        records = c.fetchall()

        history_list = tk.Listbox(history_window, bg="#E6E6FA", font=("Helvetica", 10))
        for record in records:
            history_list.insert(tk.END, f"Name: {record[1]}, Weight: {record[2]}, Height: {record[3]}, BMI: {record[4]}, Date: {record[5]}")
        history_list.pack(fill=tk.BOTH, expand=True)

    def analyze_trends(self):
        c.execute('SELECT date, bmi FROM bmi_records ORDER BY date')
        records = c.fetchall()

        if records:
            dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in records]
            bmis = [record[1] for record in records]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, bmis, marker='o', linestyle='-', color='purple')
            plt.xlabel('Date')
            plt.ylabel('BMI')
            plt.title('BMI Trend Over Time')
            plt.grid(True)
            plt.show()
        else:
            messagebox.showinfo("No data", "No BMI data available to analyze.")

if __name__ == "__main__":
    app = BMICalculator()
    app.mainloop()
    conn.close()

