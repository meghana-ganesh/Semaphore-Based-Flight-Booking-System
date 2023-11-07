# Semaphore-Based Flight Booking System

This is a simple Flight Booking System implemented using Python and the Flask web framework. Users can log in, browse available flights, book seats on flights, view booked flights, cancel bookings.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python and Flask installed on your system.

### Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/yourusername/flight-booking-system.git
```

2. Change the directory to the project folder:

```
cd flight-booking-system
```

3. Create a virtual environment (optional but recommended):

```
python -m venv env
```

4. Activate the virtual environment:

- On Windows (For PowerShell):

  ```
  env\Scripts\Activate.ps1
  ```

- On macOS and Linux:

  ```
  source env/bin/activate
  ```

5. Install the required dependencies:

```
pip install -r requirements.txt
```

### Usage

1. Run the application:

```
python app.py
```

2. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the Flight Booking System.

3. You can use the following sample accounts for testing:

- Username: user1, Password: pass1
- Username: user2, Password: pass2

4. Explore the features of the Flight Booking System, such as booking flights, viewing booked flights, and canceling bookings.


## Features

- User authentication.
- Browsing and booking flights from a list of available flights.
- Viewing booked flights.
- Canceling booked flights.
- Seat booking for selected flights.
- Participating in a survey for ad revenue.

## Project Structure

The project is organized as follows:

- `app.py`: The main application file that defines the Flask routes and handles the logic for flight booking and survey participation.
- `templates/`: This directory contains the HTML templates for rendering the web pages.
- `static/`: This directory contains static files like images and stylesheets.
- `requirements.txt`: A list of Python packages required for the project.

## Contributors

1. Meghana Ganesh - [meghana-ganesh](https://github.com/meghana-ganesh)
2. Abel Koshy - [abel-koshy](https://github.com/abel-koshy)
3. Ronit Saini - [VooDooRon](https://github.com/VooDooRon)
4. Jithin Joseph - [jj1104](https://github.com/JJ1104)