import csv 
import tkinter as ttk
import tkinter as tk

class Person:
    def __init__(self, name, gender, age,email):
        self.name = name
        self.gender = gender
        self.age = age
        self.email = email

class PersonDetailsUI:
    def __init__(self):
        self.root = ttk.Tk()
        self.root.title(" Enter Your Details")
        self.root.geometry("400x200")
        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_entry = ttk.Entry(self.root)
        self.gender_var = tk.StringVar(value=" ")
        self.gender_label = ttk.Label(self.root, text="Gender:")
        self.Female_b = ttk.Radiobutton(self.root,text ="Female",variable=self.gender_var,value ='F')
        self.Male_b = ttk.Radiobutton(self.root,text ="Male",variable=self.gender_var,value ='M')
        self.age_label = ttk.Label(self.root, text="Age:")
        self.age_entry = ttk.Scale(self.root, from_= 10, to_=100 ,orient= 'horizontal')
        self.email_label = ttk.Label(self.root,text="Email")
        self.email_entry = ttk.Entry(self.root)

        self.submit_button = ttk.Button(self.root, text="Submit", command= self.submit_details)

        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.gender_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.Male_b.grid(row=1, column=1, columnspan=2, padx=5, pady=5,sticky=tk.W)
        self.Female_b.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        self.age_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.age_entry.grid(row=2, column=1,columnspan=2, padx=5, pady=5,sticky=tk.W)
        self.email_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry.grid(row=3, column=1,columnspan=2, padx=5, pady=5)

        self.submit_button.grid(row=4, column=3, columnspan=5, padx=10, pady=10)

    def submit_details(self):
        name = self.name_entry.get()
        gender = self.gender_var.get()
        age = self.age_entry.get()
        email = self.email_entry.get()

        person = Person(name, gender, age,email)
        self.save_person_details(person)

    def save_person_details(self, person):
        columnslist = ['Name','Gender','Age','Email']  # 'Heart_rate','HRV','Stress'
        with open('vitalsReport.csv', 'a+', newline='') as file:
            writer = csv.DictWriter(file, delimiter= ',' ,fieldnames =columnslist)
            writer.writerow({'Name': person.name, 'Gender':person.gender, 'Age':person.age,'Email':person.email})
        self.root.destroy()

def get_person_details():
    details_ui = PersonDetailsUI()
    details_ui.root.mainloop()

# if __name__ == "__main__":

    # get_person_details()
