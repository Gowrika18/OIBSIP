import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

def save_to_csv(name, weight, height, bmi, category):
    with open('bmi_records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def calculate_bmi():
    try:
        name = entry_name.get()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal weight"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"BMI: {bmi} - {category}")
        save_to_csv(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        
def show_stats():
    try:
        df = pd.read_csv("bmi_records.csv", header=None)
        df.columns = ["Name", "Weight", "Height", "BMI", "Category", "Date"]

        avg_bmi = round(df["BMI"].mean(), 2)
        max_bmi = df["BMI"].max()
        min_bmi = df["BMI"].min()

        messagebox.showinfo("BMI Stats", f"Average BMI: {avg_bmi}\nMax BMI: {max_bmi}\nMin BMI: {min_bmi}")

    except Exception as e:
        messagebox.showerror("Error", f"Couldn't read data.\n{e}")

def plot_bmi_trend():
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.read_csv("bmi_records.csv", header=None)
        df.columns = ["Name", "Weight", "Height", "BMI", "Category", "Date"]
        df["Date"] = pd.to_datetime(df["Date"])

        name = entry_name.get().strip()
        if name == "":
            messagebox.showerror("Input Error", "Please enter your name to view trend.")
            return

        user_df = df[df["Name"].str.lower() == name.lower()]
        if user_df.empty:
            messagebox.showinfo("No Data", "No records found for this name.")
            return

        plt.figure(figsize=(8, 4))
        plt.plot(user_df["Date"], user_df["BMI"], marker='o', linestyle='-', color='purple')
        plt.title(f"BMI Trend for {name}")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Couldn't plot data.\n{e}")


# GUI Setup
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("300x400")

tk.Label(window, text="Name:").pack()
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="Weight (kg):").pack()
entry_weight = tk.Entry(window)
entry_weight.pack()

tk.Label(window, text="Height (m):").pack()
entry_height = tk.Entry(window)
entry_height.pack()

tk.Button(window, text="Calculate BMI", command=calculate_bmi).pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()
tk.Button(window, text="Show Stats", command=show_stats).pack(pady=5)
tk.Button(window, text="Show Trend Graph", command=plot_bmi_trend).pack(pady=5)


window.mainloop()