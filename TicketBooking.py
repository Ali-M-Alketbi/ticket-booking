import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
from abc import ABC, abstractmethod

# 1. Base Ticket Class
class Ticket(ABC):
    def __init__(self, price, validity, description):
        self.price = price
        self.validity = validity
        self.description = description

    @abstractmethod
    def get_final_price(self):
        pass

    def __str__(self):
        return f"{self.description} - Price: {self.get_final_price()} DHS"

# 2. Specific Ticket Types
class SingleDayTicket(Ticket):
    def __init__(self, price=275):
        super().__init__(price, '1 Day', 'Access to the park for one day')
    
    def get_final_price(self):
        return self.price

class TwoDayTicket(Ticket):
    def __init__(self, price=450):
        super().__init__(price, '2 Days', 'Access for two consecutive days')

    def get_final_price(self):
        return self.price * 0.9  # 10% discount for online purchase

class AnnualMembership(Ticket):
    def __init__(self, price=1840):
        super().__init__(price, '1 Year', 'Unlimited access for one year')

    def get_final_price(self):
        return self.price * 0.85  # 15% discount on renewal

class GroupTicket(Ticket):
    def __init__(self, price=220, group_size=10):
        super().__init__(price, '1 Day', 'Special rate for groups of 10 or more')
        self.group_size = group_size

    def get_final_price(self):
        if self.group_size >= 20:
            return self.price * 0.8  # 20% discount for groups of 20 or more
        return self.price

class VIPExperience(Ticket):
    def __init__(self, price=480):
        super().__init__(price, '1 Day', 'Expedited access and reserved seating for shows')

    def get_final_price(self):
        return self.price

# 3. Adding more ticket types for further expansion
class FamilyTicket(Ticket):
    def __init__(self, price=950, num_members=4):
        super().__init__(price, '1 Day', f'Family pass for {num_members} members')
        self.num_members = num_members
    
    def get_final_price(self):
        return self.price * 0.9  # 10% discount for families

class StudentTicket(Ticket):
    def __init__(self, price=180):
        super().__init__(price, '1 Day', 'Discounted ticket for students')
    
    def get_final_price(self):
        return self.price * 0.85  # 15% discount for students

# Define Customer class and database handling
class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        return [order.order_id for order in self.orders]

class Order:
    def __init__(self, order_id, customer_id, tickets):
        self.order_id = order_id
        self.customer_id = customer_id
        self.tickets = tickets

    def total_cost(self):
        return sum(ticket.get_final_price() for ticket in self.tickets)

# Database Class for Pickle
class Database:
    def __init__(self, filename):
        self.filename = filename

    def save_data(self, data):
        with open(self.filename, 'wb') as file:
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

# GUI Class for Ticket Booking System
class TicketBookingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Adventure Land Ticket Booking System")
        self.db = Database("database.pkl")
        self.customers = self.db.load_data()

        self.logged_in_customer = None
        self.create_widgets()

    def create_widgets(self):
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, pady=10)

        self.register_button = tk.Button(self.master, text="Register New Account", command=self.register_account)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Basic login check (using hardcoded credentials)
        for customer in self.customers:
            if customer.name == username:  # Check if username exists
                self.logged_in_customer = customer
                self.show_ticket_menu()
                return

        messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_account(self):
        username = simpledialog.askstring("Input", "Enter username:")
        password = simpledialog.askstring("Input", "Enter password:", show="*")
        email = simpledialog.askstring("Input", "Enter your email:")

        new_customer = Customer(id=str(len(self.customers) + 1), name=username, email=email)
        self.customers.append(new_customer)
        self.db.save_data(self.customers)

        messagebox.showinfo("Registration Successful", "Account created successfully. Please login.")

    def show_ticket_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()  # Clear login screen

        self.ticket_frame = tk.Frame(self.master)
        self.ticket_frame.pack(pady=20)

        tk.Label(self.ticket_frame, text="Select Ticket Type:").grid(row=0, column=0)

        self.ticket_options = ["Single Day", "Two Day", "Annual Membership", "Group Ticket", "VIP Experience", "Family Ticket", "Student Ticket"]
        self.ticket_var = tk.StringVar(self.master)
        self.ticket_var.set(self.ticket_options[0])

        self.ticket_menu = tk.OptionMenu(self.ticket_frame, self.ticket_var, *self.ticket_options)
        self.ticket_menu.grid(row=0, column=1)

        self.purchase_button = tk.Button(self.master, text="Purchase", command=self.purchase_ticket)
        self.purchase_button.pack(pady=20)

    def purchase_ticket(self):
        ticket_type = self.ticket_var.get()
        ticket_class = self.get_ticket_class(ticket_type)
        ticket = ticket_class()  # Instantiate selected ticket

        order = Order(order_id=f"order{len(self.logged_in_customer.orders) + 1}",
                      customer_id=self.logged_in_customer.id,
                      tickets=[ticket])

        self.logged_in_customer.add_order(order)
        self.db.save_data(self.customers)  # Save the updated customer data

        messagebox.showinfo("Purchase Successful", f"You selected {ticket_type} ticket. Total cost: {order.total_cost()} DHS.")

    def get_ticket_class(self, ticket_type):
        ticket_classes = {
            "Single Day": SingleDayTicket,
            "Two Day": TwoDayTicket,
            "Annual Membership": AnnualMembership,
            "Group Ticket": GroupTicket,
            "VIP Experience": VIPExperience,
            "Family Ticket": FamilyTicket,
            "Student Ticket": StudentTicket,
        }
        return ticket_classes.get(ticket_type)

# Run the GUI
def run_gui():
    root = tk.Tk()
    app = TicketBookingGUI(root)
    root.mainloop()

# Run the GUI
run_gui()
