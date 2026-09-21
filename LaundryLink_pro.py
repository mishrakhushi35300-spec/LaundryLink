from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import os
import random
import json
from urllib.parse import parse_qs

# =========================================================
# LAUNDRYLINK PRO
# Single-file Python Laundry Business Website
# No external Python packages required
# =========================================================

ORDERS = {}


HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>LaundryLink Pro</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: Arial, sans-serif;
    background: #f5f9fc;
    color: #1f2937;
    line-height: 1.6;
}

/* NAVBAR */

.navbar {
    background: #075985;
    color: white;
    padding: 16px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    font-size: 25px;
    font-weight: bold;
}

.logo span {
    color: #7dd3fc;
}

.nav-links {
    display: flex;
    gap: 25px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-size: 15px;
}

.nav-links a:hover {
    color: #bae6fd;
}

/* HERO */

.hero {
    min-height: 570px;
    padding: 90px 8%;
    display: flex;
    align-items: center;
    background:
        linear-gradient(120deg, #e0f2fe, #f8fafc);
}

.hero-content {
    max-width: 650px;
}

.badge {
    display: inline-block;
    background: #bae6fd;
    color: #075985;
    padding: 8px 15px;
    border-radius: 30px;
    font-weight: bold;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 55px;
    line-height: 1.1;
    color: #0c4a6e;
    margin-bottom: 20px;
}

.hero p {
    font-size: 20px;
    color: #475569;
    margin-bottom: 28px;
}

.primary-btn {
    display: inline-block;
    background: #0284c7;
    color: white;
    padding: 14px 25px;
    border-radius: 9px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
}

.primary-btn:hover {
    background: #0369a1;
}

/* SECTIONS */

section {
    padding: 70px 8%;
}

.section-title {
    text-align: center;
    color: #0c4a6e;
    font-size: 34px;
    margin-bottom: 12px;
}

.section-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 40px;
}

/* SERVICES */

.service-grid {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 25px;
}

.service-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    transition: 0.2s;
}

.service-card:hover {
    transform: translateY(-5px);
}

.service-icon {
    font-size: 48px;
    margin-bottom: 12px;
}

.service-card h3 {
    color: #075985;
    margin-bottom: 8px;
}

.price {
    font-size: 22px;
    font-weight: bold;
    color: #0284c7;
}

/* BENEFITS */

.benefit-grid {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.benefit {
    background: white;
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.benefit-icon {
    font-size: 38px;
}

/* BOOKING */

.booking-section {
    background: #e0f2fe;
}

.form-box {
    max-width: 750px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.09);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

label {
    display: block;
    margin-top: 15px;
    margin-bottom: 5px;
    font-weight: bold;
    color: #334155;
}

input,
select,
textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 15px;
}

textarea {
    resize: vertical;
}

.total-box {
    background: #f0f9ff;
    padding: 18px;
    margin-top: 20px;
    border-radius: 10px;
    text-align: center;
}

.total-box strong {
    color: #0284c7;
    font-size: 25px;
}

.form-button {
    width: 100%;
    margin-top: 20px;
}

/* TRACKING */

.track-box {
    max-width: 600px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    text-align: center;
}

.track-result {
    margin-top: 25px;
    padding: 20px;
    border-radius: 10px;
    background: #f0f9ff;
}

/* PLAN */

.plan {
    max-width: 500px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 6px 25px rgba(0,0,0,0.09);
}

.plan h3 {
    color: #075985;
    font-size: 25px;
}

.plan-price {
    font-size: 38px;
    color: #0284c7;
    font-weight: bold;
    margin: 15px;
}

.plan ul {
    list-style: none;
    margin: 20px;
}

.plan li {
    margin: 8px;
}

/* SUCCESS */

.success {
    display: none;
    margin-top: 25px;
    padding: 22px;
    background: #dcfce7;
    color: #166534;
    border-radius: 12px;
    text-align: center;
}

.order-number {
    font-size: 25px;
    font-weight: bold;
}

/* FOOTER */

footer {
    background: #082f49;
    color: white;
    text-align: center;
    padding: 35px 20px;
}

footer h3 {
    margin-bottom: 8px;
}

/* MOBILE */

@media(max-width: 700px) {

    .navbar {
        padding: 15px 5%;
    }

    .nav-links {
        display: none;
    }

    .hero {
        padding: 65px 7%;
    }

    .hero h1 {
        font-size: 40px;
    }

    .hero p {
        font-size: 17px;
    }

    section {
        padding: 55px 6%;
    }

    .form-row {
        grid-template-columns: 1fr;
    }
}

</style>
</head>


<body>

<!-- NAVIGATION -->

<nav class="navbar">

    <div class="logo">
        🧺 Laundry<span>Link</span>
    </div>

    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#services">Services</a>
        <a href="#booking">Book Pickup</a>
        <a href="#tracking">Track Order</a>
    </div>

</nav>


<!-- HERO -->

<section class="hero" id="home">

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
        </p>

        <a href="#booking" class="primary-btn">
            Book a Pickup →
        </a>

    </div>

</section>


<!-- SERVICES -->

<section id="services">

    <h2 class="section-title">
        Our Services
    </h2>

    <p class="section-subtitle">
        Choose the service that fits your needs.
    </p>

    <div class="service-grid">

        <div class="service-card">

            <div class="service-icon">🧺</div>

            <h3>Wash & Fold</h3>

            <p>
                Professional washing and folding
                for everyday clothes.
            </p>

            <div class="price">
                ₹80 / kg
            </div>

        </div>


        <div class="service-card">

            <div class="service-icon">👕</div>

            <h3>Ironing</h3>

            <p>
                Neatly ironed clothes ready
                for your day.
            </p>

            <div class="price">
                ₹8 / item
            </div>

        </div>


        <div class="service-card">

            <div class="service-icon">✨</div>

            <h3>Dry Cleaning</h3>

            <p>
                Special care for delicate
                and premium clothes.
            </p>

            <div class="price">
                ₹120 / item
            </div>

        </div>

    </div>

</section>


<!-- BENEFITS -->

<section>

    <h2 class="section-title">
        Why LaundryLink?
    </h2>

    <p class="section-subtitle">
        Traditional laundry made simple through technology.
    </p>

    <div class="benefit-grid">

        <div class="benefit">
            <div class="benefit-icon">🚚</div>
            <h3>Doorstep Pickup</h3>
            <p>We collect your clothes from home.</p>
        </div>

        <div class="benefit">
            <div class="benefit-icon">📱</div>
            <h3>Easy Booking</h3>
            <p>Book your service online in minutes.</p>
        </div>

        <div class="benefit">
            <div class="benefit-icon">🔍</div>
            <h3>Order Tracking</h3>
            <p>Track your laundry order easily.</p>
        </div>

        <div class="benefit">
            <div class="benefit-icon">💳</div>
            <h3>Digital Payment</h3>
            <p>Convenient digital payment options.</p>
        </div>

    </div>

</section>


<!-- BOOKING -->

<section class="booking-section" id="booking">

    <h2 class="section-title">
        Book a Laundry Pickup
    </h2>

    <p class="section-subtitle">
        Enter your details and schedule your pickup.
    </p>


    <div class="form-box">

        <form id="bookingForm"
              onsubmit="submitBooking(event)">

            <div class="form-row">

                <div>
                    <label>Your Name</label>

                    <input
                        type="text"
                        id="name"
                        placeholder="Enter your name"
                        required>
                </div>

                <div>
                    <label>Phone Number</label>

                    <input
                        type="tel"
                        id="phone"
                        placeholder="10-digit mobile number"
                        required>
                </div>

            </div>


            <label>Pickup Address</label>

            <textarea
                id="address"
                rows="3"
                placeholder="Enter your complete address"
                required></textarea>


            <div class="form-row">

                <div>

                    <label>Service</label>

                    <select
                        id="service"
                        onchange="calculatePrice()">

                        <option value="wash">
                            Wash & Fold — ₹80/kg
                        </option>

                        <option value="iron">
                            Ironing — ₹8/item
                        </option>

                        <option value="dry">
                            Dry Cleaning — ₹120/item
                        </option>

                    </select>

                </div>


                <div>

                    <label>Quantity</label>

                    <input
                        type="number"
                        id="quantity"
                        min="1"
                        value="1"
                        onchange="calculatePrice()"
                        required>

                </div>

            </div>


            <div class="form-row">

                <div>

                    <label>Pickup Date</label>

                    <input
                        type="date"
                        id="date"
                        required>

                </div>

                <div>

                    <label>Pickup Time</label>

                    <select id="time">

                        <option>9:00 AM - 11:00 AM</option>
                        <option>11:00 AM - 1:00 PM</option>
                        <option>2:00 PM - 4:00 PM</option>
                        <option>5:00 PM - 7:00 PM</option>

                    </select>

                </div>

            </div>


            <div class="total-box">

                Estimated Price:
                <br>

                ₹<strong id="total">80</strong>

            </div>


            <button
                type="submit"
                class="primary-btn form-button">

                Confirm Pickup

            </button>


            <div
                class="success"
                id="success">

                <div>✅ Booking Successful!</div>

                <p>
                    Thank you for choosing LaundryLink.
                </p>

                <p>
                    Your Order ID:
                </p>

                <div
                    class="order-number"
                    id="orderNumber">
                </div>

                <p>
                    Save this ID to track your order.
                </p>

            </div>

        </form>

    </div>

</section>


<!-- TRACK ORDER -->

<section id="tracking">

    <h2 class="section-title">
        Track Your Order
    </h2>

    <p class="section-subtitle">
        Enter your LaundryLink Order ID.
    </p>


    <div class="track-box">

        <input
            type="text"
            id="trackID"
            placeholder="Example: LL12345">

        <br><br>

        <button
            class="primary-btn"
            onclick="trackOrder()">

            Track Order

        </button>


        <div
            class="track-result"
            id="trackResult">

            Enter your Order ID to check status.

        </div>

    </div>

</section>


<!-- MONTHLY PLAN -->

<section>

    <h2 class="section-title">
        LaundryLink Monthly Plan
    </h2>

    <p class="section-subtitle">
        Convenient laundry for regular customers.
    </p>


    <div class="plan">

        <h3>Smart Laundry Plan</h3>

        <div class="plan-price">
            ₹999 / month
        </div>

        <ul>

            <li>✓ Priority Pickup</li>
            <li>✓ Doorstep Delivery</li>
            <li>✓ Easy Online Booking</li>
            <li>✓ Monthly Convenience</li>

        </ul>

        <button
            class="primary-btn"
            onclick="alert('Plan selected! Our team will contact you.')">

            Choose Plan

        </button>

    </div>

</section>


<!-- FOOTER -->

<footer>

    <h3>🧺 LaundryLink</h3>

    <p>
        From Local Laundry to Digital Business
    </p>

    <p>
        © 2026 LaundryLink. All rights reserved.
    </p>

</footer>


<script>

/* PRICE CALCULATION */

function calculatePrice() {

    let service =
        document.getElementById("service").value;

    let quantity =
        Number(document.getElementById("quantity").value);

    let price = 0;

    if (service === "wash") {
        price = 80;
    }

    else if (service === "iron") {
        price = 8;
    }

    else if (service === "dry") {
        price = 120;
    }

    let total = price * quantity;

    document.getElementById("total").innerText =
        total;

}


/* BOOKING */

function submitBooking(event) {

    event.preventDefault();

    let name =
        document.getElementById("name").value;

    let orderID =
        "LL" +
        Math.floor(
            Math.random() * 90000 + 10000
        );

    document.getElementById("orderNumber").innerText =
        orderID;

    document.getElementById("success").style.display =
        "block";

    document.getElementById("trackID").value =
        orderID;

    document.getElementById("success").scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


/* TRACKING DEMO */

function trackOrder() {

    let id =
        document.getElementById("trackID").value
        .trim();

    let result =
        document.getElementById("trackResult");

    if (id === "") {

        result.innerHTML =
            "⚠️ Please enter an Order ID.";

        return;
    }

    result.innerHTML =
        "<h3>Order Found ✅</h3>" +
        "<p><b>Order ID:</b> " + id + "</p>" +
        "<p>📦 Status: <b>Pickup Scheduled</b></p>" +
        "<p>🚚 Our delivery partner will collect your clothes.</p>";

}


/* INITIAL PRICE */

calculatePrice();

</script>

</body>
</html>
"""


class LaundryHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            HTML.encode("utf-8")
        )

    def log_message(self, format, *args):
        pass


# =========================================================
# SERVER
# =========================================================

port = int(os.environ.get("PORT", 8000))

server = HTTPServer(
    ("0.0.0.0", port),
    LaundryHandler
)

print()
print("===================================")
print("       LAUNDRYLINK PRO")
print("===================================")
print()
print("Website is running...")
print("Local address: http://localhost:8000")
print()

# Open browser only when running locally.
# Render/cloud hosting will not open a browser.
if not os.environ.get("PORT"):
    threading.Timer(
        1,
        lambda: webbrowser.open(
            "http://localhost:8000"
        )
    ).start()

server.serve_forever()
