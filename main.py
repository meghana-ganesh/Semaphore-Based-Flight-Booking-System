from flask import Flask, render_template, request, redirect
import threading


app = Flask(__name__, template_folder='templates', static_folder='static')

class BookingSystem:
    def __init__(self):
        self.booking_type = 0  # Default value for booking_type
        self.MRP1 = 10000  # Default value for MRP1
        self.MRP2 = 0
        self.x_semaphore = threading.Semaphore(10)
        self.refund = 0

        self.transaction_message = ""
        self.add_page_message = ""
        self.overhead_message = ""
        self.total_amount_message = ""
        self.rating_message = ""

    def collect_MRP1(self):
        self.transaction_message = f"Transaction completed with amount {self.MRP1}"

    def call_add_page(self):
        self.add_page_message = "THIS IS AN ADVERTISMENT/SURVEY"

    def rebooking_overhead(self):
        self.MRP2 = 0.1 * self.MRP1  # Fix_semaphore the calculation here
        self.overhead_message = f"Booking price: {self.MRP1}"
        self.overhead_message += f"\nAdditional rebooking overhead: {self.MRP2}"
        self.total_amount_message = f"Please pay total amount: {self.MRP1 + self.MRP2}"

    def handle_booking(self):
        if self.booking_type == 0:
            if self.x_semaphore._value == 10:
                self.collect_MRP1()
            else:
                self.x_semaphore.release()
                self.rating_message = f"rating increased to: {self.x_semaphore._value}"
                self.collect_MRP1()
        elif self.booking_type == 1:
            if self.x_semaphore._value == 10:
                self.x_semaphore.acquire()
                self.rating_message = f"rating decreased to: {self.x_semaphore._value}"
                self.collect_MRP1()
            else:
                if self.x_semaphore._value < 5 and self.x_semaphore._value > 0:
                    self.call_add_page()
                    self.x_semaphore = self.x_semaphore - 1
                    self.rating_message = f"rating decreased to: {self.x_semaphore}"
                    self.rebooking_overhead()
                else:
                    self.call_add_page()
                    self.x_semaphore.acquire()
                    self.rating_message = f"rating decreased to: {self.x_semaphore._value}"
                    self.total_amount_message = f"Total amount to be paid: {self.MRP1}"
        else:
            if self.x_semaphore._value == 10:  # Check if the semaphore count is 0.
                self.x_semaphore.acquire()
                print(f"rating decreased to: {self.x_semaphore._value}")
                refund = self.MRP1 - 0.1 * self.MRP1
                self.total_amount_message = f"Amount refunded : {refund}"        
            else:
                if self.x_semaphore._value < 5 and self.x_semaphore._value > 0:  # Check the semaphore count.
                    self.call_add_page()
                    self.x_semaphore.acquire()
                    self.rating_message = f"rating decreased to: {self.x_semaphore._value}"
                    refund = self.MRP1 - 0.2 * self.MRP1
                    self.total_amount_message = f"Amount refunded : {refund}"     
                else:
                    self.call_add_page()
                    self.x_semaphore.acquire()
                    self.rating_message = f"rating decreased to: {self.x_semaphore._value}"
                    refund = self.MRP1 - 0.3 * self.MRP1
                    self.total_amount_message = f"Amount refunded : {refund}"     

booking_system = BookingSystem()  # Initialize the booking_system object



@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/initialize_form', methods=['GET', 'POST'])
def initialize_form():
    if request.method == 'POST':
        # Get the form data
        booking_type = int(request.form['booking_type'])
        MRP1 = int(request.form['MRP1'])

        print(f'booking_type: {booking_type}')
        print(f'MRP1: {MRP1}')

        # Update the booking_system object with form values
        booking_system.booking_type = booking_type
        booking_system.MRP1 = MRP1
        return redirect('/ResultPage')

    return render_template('Booking_Form.html')

@app.route('/ResultPage', methods=['GET','POST'])
def result_page():
    booking_system.handle_booking()  # Call the handle_booking method to handle booking logic
    return render_template('Result.html',
                           transaction_message=booking_system.transaction_message,
                           rating_message=booking_system.rating_message,
                           add_page_message=booking_system.add_page_message,
                           overhead_message=booking_system.overhead_message,
                           total_amount_message=booking_system.total_amount_message)

@app.route('/Survey')
def survey():
    booking_system.handle_booking()  # Call the handle_booking method to handle survey logic
    return render_template('Survey.html',
                           transaction_message=booking_system.transaction_message,
                           rating_message=booking_system.rating_message,
                           add_page_message=booking_system.add_page_message,
                           overhead_message=booking_system.overhead_message,
                           total_amount_message=booking_system.total_amount_message)

if __name__ == '__main__':
    app.run(debug=True)