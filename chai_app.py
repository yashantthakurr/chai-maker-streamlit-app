import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_bill_pdf(order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Chai Maker - Bill Receipt")
    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Tea: {order['Tea']}  (Rs. {order['Tea Price']})")
    y -= 20

    c.drawString(50, y, f"Garnishing: {order['Garnishing']}  (Rs. {order['Garnishing Price']})")
    y -= 20

    c.drawString(50, y, f"Sugar Spoons: {order['Sugar']}")
    y -= 20

    c.drawString(50, y, f"Number of Cups: {order['Cups']}")
    y -= 20

    if order["Instruction"]:
        c.drawString(50, y, f"Special Instructions: {order['Instruction']}")
        y -= 20

    c.drawString(50, y, f"Order Type: {order['Order Type']}")
    y -= 30

    c.line(50, y, width - 50, y)
    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Price per cup: Rs. {order['Price Per Cup']}")
    y -= 20

    c.drawString(50, y, f"Total Price: Rs. {order['Total Price']}")
    y -= 40

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, "Thank you for ordering from Chai Maker")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


if "page" not in st.session_state:
    st.session_state.page = "order"

if "submit_clicked" not in st.session_state:
    st.session_state.submit_clicked = False

if st.session_state.page == "order":

    st.title("Welcome to Chai Maker ☕")
    st.subheader("Made by Yashant")

    teaMenu = {
        "<-- Choose from here -->": 0,
        "Lemon Tea": 40,
        "Ice Tea": 50,
        "Masala Tea": 30,
        "Green Tea": 45,
        "Peach Tea": 60
    }

    teaGarnishing = {
        "<-- Choose from here -->": 0,
        "None": 0,
        "Kesar": 30,
        "Mint Leaves": 5,
        "Honey": 10,
        "Rose Petals": 15
    }

    teaSelected = st.selectbox("Choose Tea:", list(teaMenu.keys()), format_func = lambda x: f"{x} (₹{teaMenu[x]})" if teaMenu[x] else x)
    if teaSelected == "<-- Choose from here -->":
        st.write("Choose a Tea!")

    garnishingSelected = st.selectbox("Choose Tea:", list(teaGarnishing.keys()), format_func = lambda x: f"{x} (₹{teaGarnishing[x]})" if teaGarnishing[x] else x)
    if garnishingSelected == "<-- Choose from here -->":
        st.write("Choose a Garnishing!")

    sugarSpoons = st.slider("Select number of spoons of sugar: ", 0, 5, 1)

    teaCups = st.number_input("How many cups: ", min_value = 1, max_value = 10)

    instruction = st.text_input("Any special instruction regarding the tea: ")

    pickOrOrder = st.radio("Select order type: ",["Dine-In", "Takeaway"])

    isValidOrder = (teaSelected != "<-- Choose from here -->" and garnishingSelected != "<-- Choose from here -->")

    teaPrice = teaMenu[teaSelected]
    garnishPrice = teaGarnishing[garnishingSelected]
    pricePerCup = teaPrice + garnishPrice
    totalPrice = pricePerCup * teaCups


    if st.button("☕ Place Order"):
        st.session_state.submit_clicked = True

        if isValidOrder:
            st.session_state.order = {
                "Tea": teaSelected,
                "Tea Price": teaPrice,
                "Garnishing": garnishingSelected,
                "Garnishing Price": garnishPrice,
                "Sugar": sugarSpoons,
                "Cups": teaCups,
                "Instruction": instruction.strip(),
                "Order Type": pickOrOrder,
                "Price Per Cup": pricePerCup,
                "Total Price": totalPrice
            }
            st.session_state.page = "summary"
            st.rerun()

    if st.session_state.submit_clicked and not isValidOrder:
        st.warning("Please select both Tea and Garnishing to proceed ☕")

elif st.session_state.page == "summary":

    if "order" not in st.session_state:
        st.session_state.page = "order"
        st.rerun()

    st.title("🧾 Order Summary")

    order = st.session_state.order

    st.write(f"**Tea:** {order['Tea']} (₹{order['Tea Price']})")
    st.write(f"**Garnishing:** {order['Garnishing']} (₹{order['Garnishing Price']})")
    st.write(f"**Sugar Spoons:** {order['Sugar']}")
    st.write(f"**Number of Cups:** {order['Cups']}")

    if order["Instruction"]:
        st.write(f"**Special Instructions:** {order['Instruction']}")

    st.write(f"**Order Type:** {order['Order Type']}")

    st.divider()
    st.subheader("💸 Price Breakdown")

    st.write(f"**Tea Price per cup:** ₹{order['Tea Price']}")
    st.write(f"**Garnishing per cup:** ₹{order['Garnishing Price']}")

    st.write("—" * 20)
    st.write(f"**Price per cup:** ₹{order['Price Per Cup']}")

    st.write(f"**Number of cups:** {order['Cups']}")

    st.write("—" * 20)
    st.subheader(f"🧾 Total Price: ₹{order['Total Price']}")

    st.success("Your tea order has been placed successfully ☕✨")

    pdf = generate_bill_pdf(order)

    st.download_button(label="📄 Download Bill as PDF", data = pdf, file_name = "chai_bill.pdf", mime = "application/pdf")

    if st.button("⬅️ Place Another Order"):
        st.session_state.page = "order"
        st.session_state.submit_clicked = False
        st.rerun()

