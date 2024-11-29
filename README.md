# Adventure Land Ticket Booking System

## Description

The **Adventure Land Ticket Booking System** is a simple Python application using **Tkinter** for the graphical user interface (GUI) and **Pickle** for saving and loading customer data. This system allows users to:

1. Register and login.
2. Select from a variety of ticket types (e.g., Single Day, Two Day, VIP Experience, Group Tickets).
3. Purchase tickets with discounts and special offers.
4. View their past orders.

The application demonstrates object-oriented programming (OOP) concepts and uses inheritance, abstract base classes (ABC), and polymorphism for ticket types. It also includes basic login and user management, along with persistent storage using Pickle.

## Features

- **Ticket Types**: 
  - Single Day Ticket
  - Two Day Ticket (with a 10% discount for online purchases)
  - Annual Membership (with a 15% discount on renewals)
  - Group Ticket (special rates for groups of 10 or more)
  - VIP Experience (expedited access)
  - Family Ticket (10% discount for families)
  - Student Ticket (15% discount for students)

- **User Accounts**: Users can register, login, and manage their orders.
- **Persistent Data**: Customer data and orders are saved using **Pickle** for easy retrieval.
- **GUI**: Built with **Tkinter**, the GUI allows users to interact with the system in a user-friendly way.

## Installation

1. Clone the repository or copy the code into your Python environment.
2. Ensure that Python is installed on your machine.
3. Install Tkinter (usually comes pre-installed with Python, but if not, install it using your package manager).

## Running the Program

Run the Python file using your preferred IDE or command line. For example:

```bash
TicketBooking.py
