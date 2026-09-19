from http.server import HTTPServer, BaseHTTPRequestHandler
import os

HTML = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>LaundryLink | Digital Laundry Service</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

html {
    scroll-behavior: smooth;
}

body {
    background: #f5f9ff;
    color: #172033;
}

/* NAVBAR */

nav {
    background: white;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 7%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.logo {
    font-size: 25px;
    font-weight: bold;
    color: #1677ff;
}

.logo span {
    color: #172033;
}

nav a {
    text-decoration: none;
    color: #333;
    margin-left: 25px;
    font-size: 15px;
}

nav a:hover {
    color: #1677ff;
}

/* HERO */

.hero {
    min-height: 580px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 70px 8%;
    background: linear-gradient(135deg, #eaf5ff, #ffffff);
}

.hero-text {
    max-width: 570px;
}

.badge {
    display: inline-block;
    background: #dceeff;
    color: #1677ff;
    padding: 9px 16px;
    border-radius: 25px;
    font-size: 14px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 55px;
    line-height: 1.1;
    margin-bottom: 20px;
}

.hero h1 span {
    color: #1677ff;
}

.hero p {
    font-size: 18px;
    color: #596579;
    line-height: 1.7;
    margin-bottom: 30px;
}

.btn {
    background: #1677ff;
    color: white;
    border: none;
    padding: 15px 27px;
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
}

.btn:hover {
    background: #095dcc;
}

.hero-card {
    width: 390px;
    height: 350px;
    background: white;
    border-radius: 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.washing-icon {
    font-size: 110px;
}

.hero-card h2 {
    margin-top: 15px;
    color: #1677ff;
}

/* COMMON */

section {
    padding: 80px 8%;
}

.section-title {
    text-align: center;
    margin-bottom: 50px;
}

.section-title h2 {
    font-size: 36px;
    margin-bottom: 10px;
}

.section-title p {
    color: #697586;
}

/* SERVICES */

.services {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}

.service {
    background: white;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
    transition: 0.3s;
}

.service:hover {
    transform: translateY(-8px);
}

.service-icon {
    font-size: 50px;
    margin-bottom: 18px;
}

.service h3 {
    margin-bottom: 10px;
    font-size: 22px;
}

.price {
    color: #1677ff;
    font-weight: bold;
    font-size: 20px;
    margin-top: 15px;
}

/* HOW IT WORKS */

.steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.step {
    background: white;
    padding: 30px 20px;
    text-align: center;
    border-radius: 18px;
}

.number {
    width: 45px;
    height: 45px;
    background: #1677ff;
    color: white;
    border-radius: 50%;
    margin: auto auto 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* BOOKING */

.booking-section {
    background: #eef6ff;
}

.booking-box {
    max-width: 850px;
    margin: auto;
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.08);
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group.full {
    grid-column: 1 / 3;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

input, select, textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #d8dee8;
    border-radius: 8px;
    font-size: 15px;
}

textarea {
    height: 90px;
    resize: none;
}

.total {
    background: #eef6ff;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 18px;
}

.success {
    display: none;
    margin-top: 20px;
    padding: 18px;
    background: #e5f9ed;
    color: #16834b;
    border-radius: 10px;
    font-weight: bold;
}

/* TRACKING */

.track-box {
    max-width: 650px;
    margin: auto;
    background: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.track-box input {
    margin: 20px 0;
}

.status {
    display: none;
    background: #eef6ff;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}

/* BENEFITS */

.benefits {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}

.benefit {
    background: white;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 7px 20px rgba(0,0,0,0.06);
}

.benefit h3 {
    color: #1677ff;
    margin-bottom: 10px;
}

/* SUBSCRIPTION */

.subscription {
    background: #172033;
    color: white;
    text-align: center;
}

.subscription h2 {
    font-size: 35px;
    margin-bottom: 15px;
}

.subscription p {
    color: #cbd5e1;
    margin-bottom: 25px;
}

.plan {
    background: white;
    color: #172033;
    max-width: 400px;
    margin: auto;
    padding: 30px;
    border-radius: 18px;
}

.plan h3 {
    font-size: 25px;
    color: #1677ff;
}

.big-price {
    font-size: 35px;
    font-weight: bold;
    margin: 15px;
}

/* FOOTER */

footer {
    background: #0e1523;
    color: white;
    text-align: center;
    padding: 30px;
}

footer p {
    color: #aab4c3;
    margin-top: 8px;
}

/* MOBILE */

@media(max-width: 800px) {

    nav {
        padding: 0 5%;
    }

    nav a {
        display: none;
    }

    .hero {
        flex-direction: column;
        text-align: center;
    }

    .hero h1 {
        font-size: 40px;
    }

    .hero-card {
        width: 100%;
        margin-top: 40px;
    }

    .services,
    .steps,
    .benefits {
        grid-template-columns: 1fr;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .form-group.full {
        grid-column: 1;
    }
}

</style>
</head>

<body>

<nav>

<div class="logo">
🧺 Laundry<span>Link</span>
</div>

<div>
<a href="#home">Home</a>
<a href="#services">Services</a>
<a href="#booking">Book Pickup</a>
<a href="#tracking">Track Order</a>
</div>

</nav>


<section class="hero" id="home">

<div class="hero-text">

<div class="badge">
✨ Smart Laundry Service
</div>

<h1>
Laundry made <span>simple.</span>
</h1>

<p>
Book your laundry online, schedule a pickup,
track your order and get clean clothes delivered
to your doorstep.
</p>

<a href="#booking" class="btn">
Book a Pickup
</a>

</div>


<div class="hero-card">

<div>

<div class="washing-icon">
🧺
</div>

<h2>LaundryLink</h2>

<p>
From Local Service<br>
to Digital Convenience
</p>

</div>

</div>

</section>


<section id="services">

<div class="section-title">

<h2>Our Services</h2>

<p>Choose the service you need</p>

</div>


<div class="services">

<div class="service">

<div class="service-icon">👕</div>

<h3>Wash & Fold</h3>

<p>
Professional washing and folding
for your everyday clothes.
</p>

<div class="price">
₹80 / kg
</div>

</div>


<div class="service">

<div class="service-icon">👔</div>

<h3>Ironing</h3>

<p>
Freshly ironed clothes delivered
ready to wear.
</p>

<div class="price">
₹8 / item
</div>

</div>


<div class="service">

<div class="service-icon">✨</div>

<h3>Dry Cleaning</h3>

<p>
Special care for premium and
delicate clothes.
</p>

<div class="price">
₹120 / item
</div>

</div>

</div>

</section>


<section>

<div class="section-title">

<h2>How LaundryLink Works</h2>

<p>Four simple steps</p>

</div>


<div class="steps">

<div class="step">

<div class="number">1</div>

<h3>Book Online</h3>

<p>Select your laundry service.</p>

</div>


<div class="step">

<div class="number">2</div>

<h3>We Pick Up</h3>

<p>Our partner collects your clothes.</p>

</div>


<div class="step">

<div class="number">3</div>

<h3>We Clean</h3>

<p>Your clothes are professionally cleaned.</p>

</div>


<div class="step">

<div class="number">4</div>

<h3>We Deliver</h3>

<p>Clean clothes reach your doorstep.</p>

</div>

</div>

</section>


<section class="booking-section" id="booking">

<div class="section-title">

<h2>Book a Laundry Pickup</h2>

<p>Fill the form to create your demo order</p>

</div>


<div class="booking-box">

<div class="form-grid">

<div class="form-group">

<label>Customer Name</label>

<input id="name" type="text" placeholder="Enter your name">

</div>


<div class="form-group">

<label>Phone Number</label>

<input id="phone" type="text" placeholder="Enter phone number">

</div>


<div class="form-group full">

<label>Pickup Address</label>

<textarea id="address" placeholder="Enter your complete address"></textarea>

</div>


<div class="form-group">

<label>Service</label>

<select id="service" onchange="calculatePrice()">

<option value="80">Wash & Fold - ₹80/kg</option>

<option value="8">Ironing - ₹8/item</option>

<option value="120">Dry Cleaning - ₹120/item</option>

</select>

</div>


<div class="form-group">

<label>Quantity</label>

<input id="quantity" type="number" value="1" min="1"
oninput="calculatePrice()">

</div>

</div>


<div class="total">

Estimated Price:
<strong>₹<span id="total">80</span></strong>

</div>


<button class="btn" onclick="bookOrder()">

Confirm Pickup

</button>


<div class="success" id="success">

✅ Booking successful!

<br><br>

Your Order ID is:
<strong id="orderId"></strong>

<br><br>

Our pickup partner will contact you soon.

</div>

</div>

</section>


<section id="tracking">

<div class="section-title">

<h2>Track Your Order</h2>

<p>Check the status of your laundry</p>

</div>


<div class="track-box">

<input id="trackId"
type="text"
placeholder="Enter Order ID e.g. LL12345">

<button class="btn" onclick="trackOrder()">

Track Order

</button>


<div class="status" id="status">

📦 <strong>Order Found!</strong>

<br><br>

Status: <strong>Pickup Scheduled</strong>

<br><br>

Your laundry pickup is scheduled.
You will receive updates soon.

</div>

</div>

</section>


<section>

<div class="section-title">

<h2>Why Choose LaundryLink?</h2>

</div>


<div class="benefits">

<div class="benefit">

<h3>⏰ Saves Time</h3>

<p>
Customers can book laundry service
from anywhere without visiting a shop.
</p>

</div>


<div class="benefit">

<h3>📱 Digital Convenience</h3>

<p>
Online booking, digital payments and
order tracking make the process easier.
</p>

</div>


<div class="benefit">

<h3>🚚 Doorstep Pickup</h3>

<p>
Laundry is collected and delivered
directly to the customer's home.
</p>

</div>


<div class="benefit">

<h3>💳 Digital Payments</h3>

<p>
Customers can pay digitally and
receive online order records.
</p>

</div>

</div>

</section>


<section class="subscription">

<h2>Monthly Laundry Plan</h2>

<p>
Perfect for students, working professionals
and families.
</p>


<div class="plan">

<h3>Smart Laundry Plan</h3>

<div class="big-price">
₹999 / month
</div>

<p>
✔ 12 kg Wash & Fold<br><br>
✔ Free Pickup & Delivery<br><br>
✔ Priority Service
</p>

<br>

<a href="#booking" class="btn">
Choose Plan
</a>

</div>

</section>


<footer>

<h3>🧺 LaundryLink</h3>

<p>
Digital Laundry Business
</p>

<p>
© 2026 LaundryLink | College Project
</p>

</footer>


<script>

function calculatePrice() {

    let service =
        document.getElementById("service").value;

    let quantity =
        document.getElementById("quantity").value;

    let total = service * quantity;

    document.getElementById("total").innerText = total;
}


function bookOrder() {

    let name =
        document.getElementById("name").value;

    let phone =
        document.getElementById("phone").value;

    let address =
        document.getElementById("address").value;

    if(name === "" || phone === "" || address === "") {

        alert("Please fill all the required details.");

        return;
    }

    let orderId =
        "LL" + Math.floor(10000 + Math.random() * 90000);

    document.getElementById("orderId").innerText =
        orderId;

    document.getElementById("success").style.display =
        "block";
}


function trackOrder() {

    let id =
        document.getElementById("trackId").value;

    if(id === "") {

        alert("Please enter your Order ID.");

        return;
    }

    document.getElementById("status").style.display =
        "block";
}

</script>

</body>
</html>
"""


class LaundryWebsite(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            HTML.encode("utf-8")
        )


# PORT FOR LOCAL + RENDER
port = int(os.environ.get("PORT", 8000))

server = HTTPServer(
    ("0.0.0.0", port),
    LaundryWebsite
)

print("--------------------------------------")
print("        LAUNDRYLINK WEBSITE")
print("--------------------------------------")
print("Server running on port:", port)
print("--------------------------------------")

server.serve_forever()
