from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    make_response,
)
from flask_session import Session

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "yadawdawd"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Booking System Handler
class BookingSystem:
    def __init__(self, x):
        self.booking_type = 0
        self.MRP1 = 0
        self.MRP2 = 0
        self.x = x
        self.refund = 0

        self.transaction_message = ""
        self.overhead_message = ""
        self.total_amount_message = ""
        self.rating_message = ""
        self.notCancelable = False
        self.callAdPage = False

    def collect_MRP1(self):
        self.transaction_message = f"Transaction completed with amount {self.MRP1}"

    def call_ad_page(self):
        print("Ad page called")
        self.callAdPage = True

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
                self.x += 1
                self.rating_message = f"Rating increased to: {self.x}"
                self.collect_MRP1()
        elif self.booking_type == 1:
            if self.x == 10:
                self.x -= 1
                self.rating_message = f"Rating decreased to: {self.x}"
                self.collect_MRP1()
            else:
                if self.x <= 5 and self.x > 0:
                    self.call_ad_page()
                    self.x -= 1
                    self.rating_message = f"Rating decreased to: {self.x}"
                    self.rebooking_overhead()
                elif self.x > 5:
                    self.call_ad_page()
                    self.x -= 1
                    self.rating_message = f"Rating decreased to: {self.x}"
                    self.total_amount_message = f"Total amount to be paid: {self.MRP1}"
        elif self.booking_type == 2:
            if self.x == 10:  # Check if the semaphore count is 0.
                self.x -= 1
                self.rating_message = f"Rating decreased to: {self.x}"
                refund = self.MRP1 - 0.1 * self.MRP1
                self.total_amount_message = f"Amount refunded : {refund}"
            else:
                if self.x < 5 and self.x > 0:  # Check the semaphore count.
                    self.call_ad_page()
                    self.x -= 1
                    self.rating_message = f"Rating decreased to: {self.x}"
                    self.refund = self.MRP1 - 0.3 * self.MRP1
                    self.total_amount_message = f"Amount refunded : {self.refund}"
                elif self.x >= 5:
                    self.call_ad_page()
                    self.x -= 1
                    self.rating_message = f"Rating decreased to: {self.x}"
                    self.refund = self.MRP1 - 0.2 * self.MRP1
                    self.total_amount_message = f"Amount refunded : {self.refund}"
                elif self.x == 0:
                    self.notCancelable = True


# Global Variables
users = {"user1": "pass1", "user2": "pass2"}

flights = {
    "airasia": {
        "dep": "BAN",
        "arr": "BOM",
        "time": "2h 30m",
        "mrp1": 10600,
        "rebook": 0,
        "image": "assets/img/airasia.png",
    },
    "qatarair": {
        "dep": "DEL",
        "arr": "QAT",
        "time": "5h 40m",
        "mrp1": 35000,
        "rebook": 0,
        "image": "assets/img/qatarair.png",
    },
    "singaair": {
        "dep": "SIN",
        "arr": "MAA",
        "time": "4h 20m",
        "mrp1": 20915,
        "rebook": 0,
        "image": "assets/img/singaair.png",
    },
}

bookedFlights = {}

survey_questions = [
    "How likely are you to cancel a booking with our airline?",
    "How likely are you to rebook with our airline?",
    "How satisfied are you with our customer service?",
    "How would you rate the quality of in-flight meals?",
    "How likely are you to recommend our airline to a friend?",
    "How often do you fly with us in a year?",
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/validate", methods=["POST", "GET"])
def validate():
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["passwd"]
        if userName in users:
            if users[userName] == password:
                if "userName" in session:
                    return render_template(
                        "bookingForm.html",
                        flights=flights,
                        userName=userName,
                        rating=session["booking_system"].x,
                    )
                else:
                    session["userName"] = userName
                    session["flights"] = flights
                    session["booking_system"] = BookingSystem(x=10)
                    return render_template(
                        "bookingForm.html",
                        flights=flights,
                        userName=userName,
                        rating=session["booking_system"].x,
                    )
            else:
                return render_template("index.html", info="Incorrect Password")
        else:
            return render_template("index.html", info="Incorrect Username")


@app.route("/bookingForm")
def bookingForm():
    if "userName" in session:
        return render_template(
            "bookingForm.html",
            flights=flights,
            userName=session["userName"],
            rating=session["booking_system"].x,
        )
    else:
        return redirect("/")


@app.route("/bookingConfirm", methods=["GET", "POST"])
def bookingConfirm():
    if request.method == "POST":
        flight = request.json
        if flight not in bookedFlights:
            mrp1 = flights[flight]["mrp1"]

            booking_system = session["booking_system"]
            booking_system.booking_type = 0

            if flights[flight]["rebook"] == 0:
                flights[flight]["rebook"] = 1
            else:
                booking_system.booking_type = 1

            booking_system.MRP1 = mrp1
            booking_system.handle_booking()
            total_amount = booking_system.MRP1 + booking_system.MRP2
            bookedFlights[flight] = flights[flight].copy()
            bookedFlights[flight]["mrp1"] = total_amount
            booking_system.MRP2 = 0

            modalMessage = "<ul>"
            openSurvey = False

            if booking_system.transaction_message != "":
                modalMessage += "<li>" + booking_system.transaction_message + "</li>"
                booking_system.transaction_message = ""
            if booking_system.rating_message != "":
                modalMessage += "<li>" + booking_system.rating_message + "</li>"
                booking_system.rating_message = ""
            if booking_system.overhead_message != "":
                modalMessage += "<li>" + booking_system.overhead_message + "</li>"
                booking_system.overhead_message = ""
            if booking_system.total_amount_message != "":
                modalMessage += "<li>" + booking_system.total_amount_message + "</li>"
                booking_system.total_amount_message = ""
            if booking_system.callAdPage:
                openSurvey = booking_system.callAdPage
                booking_system.callAdPage = False

            modalMessage += "</ul>"
            response = make_response(
                jsonify({"modalMessage": modalMessage, "openSurvey": openSurvey}), 200
            )
            return response
        else:
            response = make_response(
                jsonify({"modalMessage": "Flight already booked"}), 200
            )
            return response


@app.route("/bookedFlights")
def viewBooked():
    print(bookedFlights)
    return render_template(
        "bookedFlights.html",
        flights=bookedFlights,
        userName=session["userName"],
        rating=session["booking_system"].x,
    )


@app.route("/cancelBooking", methods=["GET", "POST"])
def cancelBooking():
    if request.method == "POST":
        flight = request.json
        mrp1 = bookedFlights[flight]["mrp1"]

        booking_system = session["booking_system"]
        booking_system.booking_type = 2

        booking_system.MRP1 = mrp1
        booking_system.handle_booking()
        if booking_system.notCancelable:
            booking_system.notCancelable = False
            response = make_response(
                jsonify({"modalMessage": "Booking cannot be cancelled"}), 200
            )
            return response
        del bookedFlights[flight]

        modalMessage = "<ul>"
        openSurvey = False

        if booking_system.transaction_message != "":
            modalMessage += "<li>" + booking_system.transaction_message + "</li>"
            booking_system.transaction_message = ""
        if booking_system.rating_message != "":
            modalMessage += "<li>" + booking_system.rating_message + "</li>"
            booking_system.rating_message = ""
        if booking_system.overhead_message != "":
            modalMessage += "<li>" + booking_system.overhead_message + "</li>"
            booking_system.overhead_message = ""
        if booking_system.total_amount_message != "":
            modalMessage += "<li>" + booking_system.total_amount_message + "</li>"
            booking_system.total_amount_message = ""
        if booking_system.callAdPage:
            openSurvey = booking_system.callAdPage
            booking_system.callAdPage = False
        modalMessage += "</ul>"

        response = make_response(
            jsonify({"modalMessage": modalMessage, "openSurvey": openSurvey}), 200
        )
        return response


@app.route("/survey")
def survey():
    return render_template("survey.html", questions=survey_questions)


if __name__ == "__main__":
    app.run(debug=True)
