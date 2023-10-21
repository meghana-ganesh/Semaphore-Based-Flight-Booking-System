from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates', static_folder='static')

class BookingSystem:
    def __init__(self):
        self.booking_type = 0  # Default value for booking_type
        self.MRP1 = 10000  # Default value for MRP1
        self.x = 9  # x:rating
        self.MRP2 = 0
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
        self.MRP2 = 0.1 * self.MRP1  # Fix the calculation here
        self.overhead_message = f"Booking price: {self.MRP1}"
        self.overhead_message += f"\nAdditional rebooking overhead: {self.MRP2}"
        self.total_amount_message = f"Please pay total amount: {self.MRP1 + self.MRP2}"

    def handle_booking(self):
        if self.booking_type == 0:
            if self.x == 10:
                self.collect_MRP1()
            else:
                self.x = self.x + 1
                self.rating_message = f"rating increased to: {self.x}"
                self.collect_MRP1()
        elif self.booking_type == 1:
            if self.x == 10:
                self.x = self.x - 1
                self.rating_message = f"rating decreased to: {self.x}"
                self.collect_MRP1()
            else:
                if self.x < 5 and self.x > 0:
                    self.call_add_page()
                    self.x = self.x - 1
                    self.rating_message = f"rating decreased to: {self.x}"
                    self.rebooking_overhead()
                else:
                    self.call_add_page()
                    self.x = self.x - 1
                    self.rating_message = f"rating decreased to: {self.x}"
                    self.total_amount_message = f"Total amount to be paid: {self.MRP1}"

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
