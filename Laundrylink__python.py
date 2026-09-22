# ============================================================
# LAUNDRYLINK
# Digital Laundry Business Website
# Python Only - Single File
# ============================================================

import os
import json
import random
import threading
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# ------------------------------------------------------------
# VARIABLES
# ------------------------------------------------------------

BUSINESS_NAME = "LaundryLink"
DATA_FILE = "laundry_orders.json"
CURRENCY = "₹"

# ------------------------------------------------------------
# LIST
# ------------------------------------------------------------

SERVICES = [
    "Wash & Fold",
    "Ironing",
    "Dry Cleaning"
]

# ------------------------------------------------------------
# TUPLE
# ------------------------------------------------------------

PICKUP_SLOTS = (
    "9:00 AM - 11:00 AM",
    "11:00 AM - 1:00 PM",
    "2:00 PM - 4:00 PM",
    "5:00 PM - 7:00 PM"
)

# ------------------------------------------------------------
# DICTIONARY
# ------------------------------------------------------------

SERVICE_PRICES = {
    "Wash & Fold": 80,
    "Ironing": 8,
    "Dry Cleaning": 120
}

ORDER_STATUS = {
    "NEW": "Order Placed",
    "PICKUP": "Pickup Scheduled",
    "PROCESSING": "Laundry Processing",
    "READY": "Ready for Delivery",
    "DONE": "Delivered"
}

# ------------------------------------------------------------
# SET
# ------------------------------------------------------------

SERVICE_AREAS = {
    "Mumbai",
    "Thane",
    "Kalyan",
    "Dombivli",
    "Navi Mumbai"
}

# ------------------------------------------------------------
# FILE HANDLING
# ------------------------------------------------------------

def load_orders():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_orders(orders):

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                orders,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        pass


# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------

def clean_name(name):

    name = str(name).strip()

    if name:
        return name.title()

    return "Customer"


def calculate_price(service, quantity):

    if service not in SERVICE_PRICES:
        return 0

    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    return SERVICE_PRICES[service] * quantity


def generate_order_id():

    orders = load_orders()

    existing_ids = {
        order.get("order_id", "")
        for order in orders
    }

    while True:

        number = random.randint(10000, 99999)
        order_id = "LL" + str(number)

        if order_id not in existing_ids:
            return order_id


def create_order(form_data):

    name = clean_name(
        form_data.get("name", [""])[0]
    )

    phone = form_data.get(
        "phone", [""]
    )[0].strip()

    address = form_data.get(
        "address", [""]
    )[0].strip()

    service = form_data.get(
        "service", ["Wash & Fold"]
    )[0]

    quantity_text = form_data.get(
        "quantity", ["1"]
    )[0]

    pickup_date = form_data.get(
        "date", [""]
    )[0]

    pickup_time = form_data.get(
        "time", [PICKUP_SLOTS[0]]
    )[0]

    if service not in SERVICES:
        service = SERVICES[0]

    try:
        quantity = int(quantity_text)
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    total_price = calculate_price(
        service,
        quantity
    )

    order = {
        "order_id": generate_order_id(),
        "name": name,
        "phone": phone,
        "address": address,
        "service": service,
        "quantity": quantity,
        "pickup_date": pickup_date,
        "pickup_time": pickup_time,
        "price": total_price,
        "status": ORDER_STATUS["NEW"],
        "created_at": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )
    }

    return order


def add_order(order):

    orders = load_orders()
    orders.append(order)
    save_orders(orders)


def find_order(order_id):

    search_id = str(order_id).strip().upper()

    orders = load_orders()

    for order in orders:

        saved_id = order.get(
            "order_id",
            ""
        ).upper()

        if saved_id == search_id:
            return order

    return None


# ============================================================
# WEB PAGE
# ============================================================

def create_web_page(
    message="",
    order=None,
    tracked_order=None
):

    # Service dropdown
    service_options = ""

    for service in SERVICES:

        price = SERVICE_PRICES[service]

        service_options += f"""
        <option value="{service}">
            {service} - {CURRENCY}{price}
        </option>
        """

    # Time dropdown
    time_options = ""

    for slot in PICKUP_SLOTS:

        time_options += f"""
        <option value="{slot}">
            {slot}
        </option>
        """

    # Message
    message_html = ""

    if message:

        message_html = f"""
        <div class="message">
            {message}
        </div>
        """

    # Booking result
    booking_result = ""

    if order:

        booking_result = f"""
        <div class="success">

            <div class="success-icon">✓</div>

            <h2>Booking Successful!</h2>

            <p>
                Thank you, <b>{order["name"]}</b>
            </p>

            <p>
                Your Order ID is
            </p>

            <div class="order-id">
                {order["order_id"]}
            </div>

            <p>
                <b>Service:</b> {order["service"]}<br>
                <b>Quantity:</b> {order["quantity"]}<br>
                <b>Price:</b> {CURRENCY}{order["price"]}<br>
                <b>Pickup:</b> {order["pickup_date"]}
            </p>

            <p>
                Please save your Order ID
                for tracking.
            </p>

        </div>
        """

    # Tracking result
    tracking_result = ""

    if tracked_order:

        tracking_result = f"""
        <div class="tracking-result">

            <div class="tracking-icon">📦</div>

            <h2>Order Found</h2>

            <p>
                <b>Order ID:</b>
                {tracked_order["order_id"]}
            </p>

            <p>
                <b>Customer:</b>
                {tracked_order["name"]}
            </p>

            <p>
                <b>Service:</b>
                {tracked_order["service"]}
            </p>

            <p>
                <b>Quantity:</b>
                {tracked_order["quantity"]}
            </p>

            <p>
                <b>Pickup Date:</b>
                {tracked_order["pickup_date"]}
            </p>

            <p>
                <b>Pickup Time:</b>
                {tracked_order["pickup_time"]}
            </p>

            <div class="status">
                {tracked_order["status"]}
            </div>

            <p>
                Estimated Price:
                <b>{CURRENCY}{tracked_order["price"]}</b>
            </p>

        </div>
        """

    # ========================================================
    # COMPLETE WEBPAGE
    # ========================================================

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
{BUSINESS_NAME} | Digital Laundry
</title>

<style>

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: Arial, sans-serif;
    background: #f7fbfe;
    color: #1e293b;
    line-height: 1.6;
}}

.navbar {{
    background: #075985;
    color: white;
    padding: 17px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
}}

.logo {{
    font-size: 27px;
    font-weight: bold;
}}

.logo span {{
    color: #7dd3fc;
}}

.nav-links {{
    display: flex;
    gap: 25px;
}}

.nav-links a {{
    color: white;
    text-decoration: none;
    font-weight: 500;
}}

.nav-links a:hover {{
    color: #bae6fd;
}}

.hero {{
    min-height: 570px;
    padding: 100px 8%;
    display: flex;
    align-items: center;
    background:
    linear-gradient(
        120deg,
        #e0f2fe,
        #ffffff
    );
}}

.hero-content {{
    max-width: 720px;
}}

.badge {{
    display: inline-block;
    background: #bae6fd;
    color: #075985;
    padding: 8px 16px;
    border-radius: 25px;
    font-weight: bold;
    margin-bottom: 18px;
}}

.hero h1 {{
    font-size: 57px;
    color: #0c4a6e;
    line-height: 1.08;
    margin-bottom: 20px;
}}

.hero p {{
    font-size: 20px;
    color: #475569;
    margin-bottom: 28px;
}}

.btn {{
    display: inline-block;
    background: #0284c7;
    color: white;
    padding: 14px 25px;
    border-radius: 9px;
    border: none;
    text-decoration: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
}}

.btn:hover {{
    background: #0369a1;
}}

section {{
    padding: 75px 8%;
}}

.title {{
    text-align: center;
    color: #0c4a6e;
    font-size: 35px;
    margin-bottom: 10px;
}}

.subtitle {{
    text-align: center;
    color: #64748b;
    margin-bottom: 40px;
}}

.service-grid {{
    display: grid;
    grid-template-columns:
    repeat(
        auto-fit,
        minmax(220px, 1fr)
    );
    gap: 25px;
}}

.service-card {{
    background: white;
    padding: 32px;
    border-radius: 17px;
    text-align: center;
    box-shadow:
    0 5px 22px rgba(0,0,0,0.07);

    transition: 0.2s;
}}

.service-card:hover {{
    transform: translateY(-5px);
}}

.service-icon {{
    font-size: 48px;
    margin-bottom: 12px;
}}

.service-card h3 {{
    color: #075985;
    font-size: 21px;
    margin-bottom: 10px;
}}

.price {{
    color: #0284c7;
    font-size: 23px;
    font-weight: bold;
    margin-top: 12px;
}}

.benefits {{
    background: #ffffff;
}}

.benefit-grid {{
    display: grid;
    grid-template-columns:
    repeat(
        auto-fit,
        minmax(200px, 1fr)
    );
    gap: 20px;
}}

.benefit {{
    background: #f8fafc;
    padding: 28px;
    border-radius: 15px;
    text-align: center;
}}

.benefit-icon {{
    font-size: 40px;
    margin-bottom: 10px;
}}

.benefit h3 {{
    color: #075985;
    margin-bottom: 8px;
}}

.booking {{
    background: #e0f2fe;
}}

.form-box {{
    max-width: 800px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow:
    0 6px 25px rgba(0,0,0,0.08);
}}

.row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}}

label {{
    display: block;
    margin-top: 15px;
    margin-bottom: 6px;
    font-weight: bold;
    color: #334155;
}}

input,
select,
textarea {{
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 15px;
    background: white;
}}

textarea {{
    resize: vertical;
}}

.form-btn {{
    width: 100%;
    margin-top: 22px;
}}

.message {{
    max-width: 800px;
    margin: 0 auto 20px;
    background: #fff7ed;
    color: #9a3412;
    padding: 15px;
    text-align: center;
    border-radius: 9px;
}}

.success {{
    max-width: 800px;
    margin: 25px auto 0;
    background: #dcfce7;
    color: #166534;
    padding: 28px;
    border-radius: 15px;
    text-align: center;
}}

.success-icon {{
    font-size: 43px;
    margin-bottom: 5px;
}}

.order-id {{
    font-size: 32px;
    font-weight: bold;
    color: #075985;
    margin: 10px;
}}

.tracking {{
    background: white;
}}

.track-box {{
    max-width: 600px;
    margin: auto;
    background: #f8fafc;
    padding: 30px;
    border-radius: 15px;
    box-shadow:
    0 4px 18px rgba(0,0,0,0.06);
}}

.tracking-result {{
    max-width: 600px;
    margin: 25px auto;
    background: #eff6ff;
    color: #1e3a8a;
    padding: 28px;
    border-radius: 15px;
    text-align: center;
}}

.tracking-icon {{
    font-size: 42px;
}}

.status {{
    display: inline-block;
    margin: 12px;
    padding: 8px 17px;
    background: #dbeafe;
    color: #1d4ed8;
    border-radius: 25px;
    font-weight: bold;
}}

.plan-section {{
    background: #f8fafc;
}}

.plan {{
    max-width: 500px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    box-shadow:
    0 6px 22px rgba(0,0,0,0.07);
}}

.plan h3 {{
    color: #075985;
    font-size: 25px;
}}

.plan-price {{
    color: #0284c7;
    font-size: 39px;
    font-weight: bold;
    margin: 12px;
}}

.plan ul {{
    list-style: none;
    margin: 20px;
}}

.plan li {{
    margin: 8px;
}}

footer {{
    background: #082f49;
    color: white;
    text-align: center;
    padding: 35px 20px;
}}

footer h2 {{
    margin-bottom: 7px;
}}

@media(max-width:700px) {{

    .nav-links {{
        display: none;
    }}

    .hero {{
        padding: 70px 7%;
    }}

    .hero h1 {{
        font-size: 41px;
    }}

    .hero p {{
        font-size: 17px;
    }}

    .row {{
        grid-template-columns: 1fr;
    }}

    section {{
        padding: 55px 6%;
    }}

}}

</style>

</head>


<body>

<!-- NAVBAR -->

<nav class="navbar">

    <div class="logo">
        🧺 Laundry<span>Link</span>
    </div>

    <div class="nav-links">

        <a href="#home">
            Home
        </a>

        <a href="#services">
            Services
        </a>

        <a href="#benefits">
            Why Us
        </a>

        <a href="#booking">
            Book Pickup
        </a>

        <a href="#tracking">
            Track Order
        </a>

    </div>

</nav>


<!-- HERO -->

<section
class="hero"
id="home">

    <div class="hero-content">

        <div class="badge">
            Digital Laundry Service
        </div>

        <h1>
            Fresh Clothes.<br>
            Easy Life.
        </h1>

        <p>
            LaundryLink brings professional laundry
            pickup and delivery right to your doorstep.
            Book online and track your order easily.
        </p>

        <a
        href="#booking"
        class="btn">

            Book a Pickup →

        </a>

    </div>

</section>


<!-- SERVICES -->

<section
id="services">

    <h2 class="title">
        Our Services
    </h2>

    <p class="subtitle">
        Professional laundry services at your doorstep.
    </p>


    <div class="service-grid">

        <div class="service-card">

            <div class="service-icon">
                🧺
            </div>

            <h3>
                Wash & Fold
            </h3>

            <p>
                Professional washing and neat folding
                for everyday clothes.
            </p>

            <div class="price">
                ₹80 / kg
            </div>

        </div>


        <div class="service-card">

            <div class="service-icon">
                👕
            </div>

            <h3>
                Ironing
            </h3>

            <p>
                Neatly ironed clothes ready to wear.
            </p>

            <div class="price">
                ₹8 / item
            </div>

        </div>


        <div class="service-card">

            <div class="service-icon">
                ✨
            </div>

            <h3>
                Dry Cleaning
            </h3>

            <p>
                Special care for delicate and premium clothes.
            </p>

            <div class="price">
                ₹120 / item
            </div>

        </div>

    </div>

</section>


<!-- BENEFITS -->

<section
class="benefits"
id="benefits">

    <h2 class="title">
        Why Choose LaundryLink?
    </h2>

    <p class="subtitle">
        Traditional laundry made simple through technology.
    </p>


    <div class="benefit-grid">

        <div class="benefit">

            <div class="benefit-icon">
                🚚
            </div>

            <h3>
                Doorstep Pickup
            </h3>

            <p>
                We collect clothes from your home.
            </p>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                📱
            </div>

            <h3>
                Easy Booking
            </h3>

            <p>
                Book your service online in minutes.
            </p>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                🔍
            </div>

            <h3>
                Order Tracking
            </h3>

            <p>
                Track your laundry order easily.
            </p>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                💳
            </div>

            <h3>
                Digital Payment
            </h3>

            <p>
                Convenient digital payment options.
            </p>

        </div>

    </div>

</section>


<!-- BOOKING -->

<section
class="booking"
id="booking">

    <h2 class="title">
        Book a Laundry Pickup
    </h2>

    <p class="subtitle">
        Enter your details and schedule your pickup.
    </p>


    {message_html}


    <div class="form-box">

        <form
        method="POST"
        action="/book">


            <div class="row">

                <div>

                    <label>
                        Your Name
                    </label>

                    <input
                    type="text"
                    name="name"
                    placeholder="Enter your name"
                    required>

                </div>


                <div>

                    <label>
                        Phone Number
                    </label>

                    <input
                    type="tel"
                    name="phone"
                    placeholder="Enter phone number"
                    required>

                </div>

            </div>


            <label>
                Pickup Address
            </label>

            <textarea
            name="address"
            rows="3"
            placeholder="Enter your complete address"
            required></textarea>


            <div class="row">

                <div>

                    <label>
                        Select Service
                    </label>

                    <select
                    name="service">

                        {service_options}

                    </select>

                </div>


                <div>

                    <label>
                        Quantity
                    </label>

                    <input
                    type="number"
                    name="quantity"
                    min="1"
                    value="1"
                    required>

                </div>

            </div>


            <div class="row">

                <div>

                    <label>
                        Pickup Date
                    </label>

                    <input
                    type="date"
                    name="date"
                    required>

                </div>


                <div>

                    <label>
                        Pickup Time
                    </label>

                    <select
                    name="time">

                        {time_options}

                    </select>

                </div>

            </div>


            <button
            type="submit"
            class="btn form-btn">

                Confirm Pickup

            </button>

        </form>

    </div>


    {booking_result}

</section>


<!-- TRACK ORDER -->

<section
class="tracking"
id="tracking">

    <h2 class="title">
        Track Your Order
    </h2>

    <p class="subtitle">
        Enter your LaundryLink Order ID to check status.
    </p>


    <div class="track-box">

        <form
        method="POST"
        action="/track">


            <label>
                Order ID
            </label>

            <input
            type="text"
            name="order_id"
            placeholder="Example: LL12345"
            required>


            <button
            type="submit"
            class="btn form-btn">

                Track Order

            </button>

        </form>

    </div>


    {tracking_result}

</section>


<!-- MONTHLY PLAN -->

<section
class="plan-section">

    <h2 class="title">
        LaundryLink Monthly Plan
    </h2>

    <p class="subtitle">
        Convenient laundry for regular customers.
    </p>


    <div class="plan">

        <h3>
            Smart Laundry Plan
        </h3>

        <div class="plan-price">
            ₹999 / month
        </div>

        <ul>

            <li>
                ✓ Priority Pickup
            </li>

            <li>
                ✓ Doorstep Delivery
            </li>

            <li>
                ✓ Easy Online Booking
            </li>

            <li>
                ✓ Monthly Convenience
            </li>

        </ul>


        <button
        class="btn"
        onclick="alert(
            'Thank you! Our team will contact you.'
        )">

            Choose Plan

        </button>

    </div>

</section>


<!-- FOOTER -->

<footer>

    <h2>
        🧺 LaundryLink
    </h2>

    <p>
        From Traditional Laundry to Digital Business
    </p>

    <p>
        © 2026 LaundryLink. All rights reserved.
    </p>

</footer>


</body>

</html>
"""

    return html


# ============================================================
# WEB SERVER
# ============================================================

class LaundryHandler(BaseHTTPRequestHandler):

    def send_page(self, page):

        data = page.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.end_headers()

        self.wfile.write(data)


    def read_form_data(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        body = self.rfile.read(length)

        body = body.decode("utf-8")

        return parse_qs(body)


    def do_GET(self):

        if self.path == "/":

            page = create_web_page()

            self.send_page(page)

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        # ---------------- BOOK ORDER ----------------

        if self.path == "/book":

            form_data = self.read_form_data()

            name = form_data.get(
                "name",
                [""]
            )[0].strip()

            phone = form_data.get(
                "phone",
                [""]
            )[0].strip()

            address = form_data.get(
                "address",
                [""]
            )[0].strip()


            if not name:

                self.send_page(
                    create_web_page(
                        "Please enter your name."
                    )
                )

                return


            if not phone:

                self.send_page(
                    create_web_page(
                        "Please enter your phone number."
                    )
                )

                return


            if not address:

                self.send_page(
                    create_web_page(
                        "Please enter your address."
                    )
                )

                return


            order = create_order(
                form_data
            )

            add_order(order)

            self.send_page(
                create_web_page(
                    order=order
                )
            )

            return


        # ---------------- TRACK ORDER ----------------

        if self.path == "/track":

            form_data = self.read_form_data()

            order_id = form_data.get(
                "order_id",
                [""]
            )[0]

            order = find_order(order_id)


            if order:

                page = create_web_page(
                    tracked_order=order
                )

            else:

                page = create_web_page(
                    "Order ID not found. Please try again."
                )


            self.send_page(page)

            return


        self.send_response(404)
        self.end_headers()


    def log_message(self, format, *args):
        pass


# ============================================================
# START SERVER
# ============================================================

def start_laundrylink():

    # Render gives PORT automatically.
    port = int(
        os.environ.get(
            "PORT",
            "8000"
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        LaundryHandler
    )

    print()
    print("====================================")
    print("          LAUNDRYLINK")
    print("====================================")
    print()
    print(
        "Website running at:"
    )
    print(
        f"http://localhost:{port}"
    )
    print()

    # Open browser only on local computer.
    if "PORT" not in os.environ:

        threading.Timer(
            1,
            lambda: webbrowser.open(
                f"http://localhost:{port}"
            )
        ).start()

    server.serve_forever()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    start_laundrylink()
