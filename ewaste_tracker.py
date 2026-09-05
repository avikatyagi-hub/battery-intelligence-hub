import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- 1. Expanded Data Store ---
USER_REWARDS = {"default_user": 0}

# Database of companies and specific models
DEVICE_DATA = {
    "Apple": {
        "Smartphone": ["iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15 Pro"],
        "Laptop": ["MacBook Air M1", "MacBook Air M2", "MacBook Pro M3"],
        "Tablet": ["iPad Air", "iPad Pro 12.9"]
    },
    "Samsung": {
        "Smartphone": ["Galaxy S21", "Galaxy S22 Ultra", "Galaxy S23", "Galaxy S24"],
        "Tablet": ["Galaxy Tab S8", "Galaxy Tab S9 Ultra"],
        "Wearable": ["Galaxy Watch 5", "Galaxy Watch 6"]
    },
    "Google": {
        "Smartphone": ["Pixel 6", "Pixel 7 Pro", "Pixel 8"],
        "Wearable": ["Pixel Watch 2"]
    },
    "Dell": {
        "Laptop": ["XPS 13", "XPS 15", "Latitude 5420", "Inspiron 16"],
        "Monitor": ["UltraSharp 27", "P-Series 24"]
    },
    "HP": {
        "Laptop": ["Spectre x360", "Envy 13", "Pavilion Gaming", "Omen 16"]
    },
    "Lenovo": {
        "Laptop": ["ThinkPad X1 Carbon", "Yoga 7i", "Legion 5 Pro"]
    },
    "Asus": {
        "Laptop": ["Zenbook 14", "ROG Zephyrus G14", "Vivobook S"]
    }
}

LOCATION_DATABASE = {
    "Chennai": [
        "♻️ Enviro Care India - Ambattur Industrial Estate",
        "♻️ Tritech Systems - Guindy",
        "♻️ Earth Sense Recycle - Sriperumbudur",
        "♻️ Virogreen India - Gummidipoondi",
        "♻️ Ultrust Solutions - Perungudi"
    ],
    "Other": ["♻️ Check CPCB.nic.in for authorized state recyclers."]
}

# --- 2. Advanced Logic Engine ---

def get_diagnostics(purchase_date_str, problem, company, model, location):
    try:
        purchase_date = datetime.strptime(purchase_date_str, "%m/%Y")
        months_old = (datetime.now().year - purchase_date.year) * 12 + (datetime.now().month - purchase_date.month)
        if months_old < 0: raise ValueError
    except ValueError:
        return None, None, "Invalid Date (Use MM/YYYY)", []

    # 1. Base Decay based on Device Type
    # Laptops decay faster due to heat; Wearables have tiny, fragile cells.
    decay_rate = 0.8 # Default
    if "MacBook" in model or "XPS" in model or "ThinkPad" in model:
        decay_rate = 1.2 # Laptops
    elif "Watch" in model:
        decay_rate = 1.5 # Wearables
        
    base_health = 100 - (months_old * decay_rate)

    # 2. Hardware Stress Impact (Internet-based Problem Severity)
    problem_impact = {
        "None (Working fine)": 0,
        "Battery Swelling/Bloating": 65,
        "Rapid Discharge/Overheating": 35,
        "Charging Port Loose": 10,
        "System Lag/Freezing": 20,
        "Unexpected Shutdowns": 45
    }
    
    final_health = max(5, int(base_health - problem_impact.get(problem, 0)))
    
    # 3. Dynamic Advice & Condition
    advice_list = []
    if final_health > 80:
        condition = "Repairable/Good"
        advice_list.append("🔋 MAINTENANCE: Best time to recharge is at 20%. Avoid 0% to keep cycles low.")
    elif 50 <= final_health <= 80:
        condition = "Refurbish Candidate"
        advice_list.append("🔌 SMART USAGE: Avoid 'Pass-through' charging (using heavy apps while plugged in).")
    else:
        condition = "Recycle Only"
        advice_list.append(f"⚠️ AGING CELLS: This {model} is failing. Use for low-power tasks like an offline music player.")

    if "Overheating" in problem:
        advice_list.append("❄️ PRO TIP: Check for background apps; heat is the #1 killer of Lithium-Ion.")

    centers = LOCATION_DATABASE.get(location, LOCATION_DATABASE["Other"]) if final_health < 50 else []

    return final_health, condition, "\n\n".join(advice_list), centers

# --- 3. Tkinter Application Class ---

class EWasteTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Circular Economy: Battery Intelligence Hub")
        self.geometry("620x880")
        self.resizable(False, False)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="AI Device Diagnostics & E-Waste Hub", font=('Inter', 16, 'bold')).pack(pady=10)
        
        form = ttk.LabelFrame(main_frame, text=" 1. Select Your Device ", padding="15")
        form.pack(fill='x', pady=5)

        # Dropdowns
        ttk.Label(form, text="Company:").grid(row=0, column=0, sticky='w', pady=5)
        self.company_cb = ttk.Combobox(form, values=list(DEVICE_DATA.keys()), state="readonly")
        self.company_cb.grid(row=0, column=1, sticky='ew', pady=5)
        self.company_cb.bind("<<ComboboxSelected>>", self.update_models)

        ttk.Label(form, text="Model:").grid(row=1, column=0, sticky='w', pady=5)
        self.model_cb = ttk.Combobox(form, state="readonly")
        self.model_cb.grid(row=1, column=1, sticky='ew', pady=5)

        ttk.Label(form, text="Problem:").grid(row=2, column=0, sticky='w', pady=5)
        self.prob_cb = ttk.Combobox(form, values=["None (Working fine)", "Battery Swelling/Bloating", "Rapid Discharge/Overheating", "Charging Port Loose", "System Lag/Freezing", "Unexpected Shutdowns"], state="readonly")
        self.prob_cb.current(0)
        self.prob_cb.grid(row=2, column=1, sticky='ew', pady=5)

        ttk.Label(form, text="Purchase (MM/YYYY):").grid(row=3, column=0, sticky='w', pady=5)
        self.date_ent = ttk.Entry(form)
        self.date_ent.insert(0, "01/2023")
        self.date_ent.grid(row=3, column=1, sticky='ew', pady=5)

        ttk.Label(form, text="Location:").grid(row=4, column=0, sticky='w', pady=5)
        self.loc_cb = ttk.Combobox(form, values=["Chennai", "Mumbai", "Delhi", "Bangalore"], state="readonly")
        self.loc_cb.current(0)
        self.loc_cb.grid(row=4, column=1, sticky='ew', pady=5)

        form.columnconfigure(1, weight=1)

        ttk.Button(main_frame, text="Run Analysis", command=self.run_analysis).pack(pady=15)

        # Output Section
        self.res_label = ttk.Label(main_frame, text="Health: --", font=('Inter', 12, 'bold'))
        self.res_label.pack()

        self.advice_box = tk.Text(main_frame, height=6, font=('Inter', 10), bg="#f8f9fa", wrap='word', state='disabled', padx=10, pady=10)
        self.advice_box.pack(fill='x', pady=5)

        self.recycle_frame = ttk.LabelFrame(main_frame, text=" 📍 Nearest Recycling Centers ", padding="10")
        self.recycle_frame.pack(fill='both', expand=True)
        
        self.recycle_list = tk.Text(self.recycle_frame, height=5, font=('Inter', 9), bg="#f1f1f1", state='disabled')
        self.recycle_list.pack(fill='both', expand=True)

    def update_models(self, event):
        brand = self.company_cb.get()
        all_models = []
        for category in DEVICE_DATA[brand]:
            all_models.extend(DEVICE_DATA[brand][category])
        self.model_cb['values'] = all_models
        self.model_cb.set('')

    def run_analysis(self):
        h, c, a, centers = get_diagnostics(self.date_ent.get(), self.prob_cb.get(), self.company_cb.get(), self.model_cb.get(), self.loc_cb.get())
        
        if h is None:
            messagebox.showerror("Error", a)
            return

        # UI Update
        self.res_label.config(text=f"Battery Health: {h}% ({c})", foreground="#D22B2B" if h < 50 else "#00A36C")
        
        self.advice_box.config(state='normal')
        self.advice_box.delete('1.0', tk.END)
        self.advice_box.insert(tk.END, a)
        self.advice_box.config(state='disabled')

        self.recycle_list.config(state='normal')
        self.recycle_list.delete('1.0', tk.END)
        if centers:
            self.recycle_list.insert(tk.END, "\n".join(centers))
        else:
            self.recycle_list.insert(tk.END, "✅ Health is sufficient. Keep using the device following the advice above!")
        self.recycle_list.config(state='disabled')

if __name__ == "__main__":
    app = EWasteTrackerApp()
    app.mainloop()