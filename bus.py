import streamlit as st
import pandas as pd
import os
import uuid
from datetime import date, time, datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bus Booking Management System",
    page_icon="🚌",
    layout="wide"
)

# ============================================================
# FILE CONFIGURATION
# ============================================================

FILE_NAME = "bus_bookings.csv"

# ============================================================
# ALL COLUMNS
# ============================================================

COLUMNS = [
    "booking_id",
    "customer_id",
    "customer_name",
    "phone_number",
    "customer_email",
    "rating",
    "customer_age",
    "gender",
    "customer_type",
    "booking_date",
    "journey_date",
    "days_before_journey",
    "source_city",
    "destination_city",
    "route",
    "bus_operator",
    "bus_type",
    "departure_time",
    "arrival_time",
    "travel_duration_hours",
    "total_seats",
    "available_seats",
    "ticket_price",
    "number_of_passengers",
    "total_amount",
    "payment_method",
    "booking_status",
    "cancellation_reason",
    "day_of_week",
    "month",
    "is_weekend",
    "is_holiday",
    "season",
    "peak_hour",
    "historical_bookings",
    "historical_avg_price",
    "historical_cancellation_rate",
    "occupancy_rate"
]

# ============================================================
# DATA TYPE GROUPS
# ============================================================

NUMERIC_COLUMNS = [
    "rating",
    "customer_age",
    "days_before_journey",
    "travel_duration_hours",
    "total_seats",
    "available_seats",
    "ticket_price",
    "number_of_passengers",
    "total_amount",
    "historical_bookings",
    "historical_avg_price",
    "historical_cancellation_rate",
    "occupancy_rate"
]

BOOLEAN_COLUMNS = [
    "is_weekend",
    "is_holiday",
    "peak_hour"
]

TEXT_COLUMNS = [
    "booking_id",
    "customer_id",
    "customer_name",
    "phone_number",
    "customer_email",
    "gender",
    "customer_type",
    "booking_date",
    "journey_date",
    "source_city",
    "destination_city",
    "route",
    "bus_operator",
    "bus_type",
    "departure_time",
    "arrival_time",
    "payment_method",
    "booking_status",
    "cancellation_reason",
    "day_of_week",
    "month",
    "season"
]

# ============================================================
# CREATE EMPTY DATAFRAME
# ============================================================

def empty_dataframe():

    data = pd.DataFrame(columns=COLUMNS)

    for col in NUMERIC_COLUMNS:
        data[col] = pd.Series(dtype="float64")

    for col in TEXT_COLUMNS:
        data[col] = pd.Series(dtype="object")

    for col in BOOLEAN_COLUMNS:
        data[col] = pd.Series(dtype="bool")

    return data[COLUMNS]


# ============================================================
# CLEAN DATAFRAME
# ============================================================

def clean_dataframe(data):

    data = data.copy()

    # Add missing columns
    for col in COLUMNS:

        if col not in data.columns:
            data[col] = None

    # Keep required columns only
    data = data[COLUMNS].copy()

    # -------------------------------
    # Numeric columns
    # -------------------------------

    for col in NUMERIC_COLUMNS:

        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

        data[col] = data[col].fillna(0)

    # -------------------------------
    # Text columns
    # -------------------------------

    for col in TEXT_COLUMNS:

        data[col] = (
            data[col]
            .fillna("")
            .astype(str)
        )

    # -------------------------------
    # Boolean columns
    # -------------------------------

    for col in BOOLEAN_COLUMNS:

        if data[col].dtype == "object":

            data[col] = (
                data[col]
                .astype(str)
                .str.lower()
                .map({
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False,
                    "yes": True,
                    "no": False
                })
            )

        data[col] = data[col].fillna(False).astype(bool)

    return data[COLUMNS]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not os.path.exists(FILE_NAME):

        return empty_dataframe()

    try:

        data = pd.read_csv(
            FILE_NAME,
            low_memory=False
        )

        return clean_dataframe(data)

    except Exception as e:

        st.error(
            f"Unable to read {FILE_NAME}: {e}"
        )

        return empty_dataframe()


# ============================================================
# SAVE DATA
# ============================================================

def save_data(data):

    data = clean_dataframe(data)

    data.to_csv(
        FILE_NAME,
        index=False
    )


# ============================================================
# GENERATE BOOKING ID
# ============================================================

def generate_booking_id():

    return (
        "BKG"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + "_"
        + str(uuid.uuid4())[:4].upper()
    )


# ============================================================
# CALCULATE SEASON
# ============================================================

def calculate_season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Summer"

    elif month in [6, 7, 8, 9]:
        return "Monsoon"

    else:
        return "Autumn"


# ============================================================
# CALCULATE OCCUPANCY
# ============================================================

def calculate_occupancy(
    total_seats,
    available_seats
):

    if total_seats <= 0:
        return 0.0

    occupied_seats = (
        total_seats - available_seats
    )

    occupancy = (
        occupied_seats / total_seats
    ) * 100

    return round(
        occupancy,
        2
    )


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚌 Bus Booking System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Booking",
        "✏️ Update Booking",
        "🗑️ Remove Booking",
        "🔍 Search Booking",
        "📋 All Bookings"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Bus Booking Management System\n\n"
    "Python + Pandas + Streamlit"
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    st.title(
        "🚌 Bus Booking Management Dashboard"
    )

    st.write(
        "Manage bookings, customers, routes, payments and bus operations."
    )

    st.markdown("---")

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_bookings = len(df)

    total_revenue = float(
        df["total_amount"].sum()
    )

    total_passengers = int(
        df["number_of_passengers"].sum()
    )

    confirmed_bookings = int(
        (
            df["booking_status"]
            .str.lower()
            == "confirmed"
        ).sum()
    )

    cancelled_bookings = int(
        (
            df["booking_status"]
            .str.lower()
            == "cancelled"
        ).sum()
    )

    pending_bookings = int(
        (
            df["booking_status"]
            .str.lower()
            == "pending"
        ).sum()
    )

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Bookings",
        total_bookings
    )

    col2.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    col3.metric(
        "Passengers",
        total_passengers
    )

    col4.metric(
        "Confirmed",
        confirmed_bookings
    )

    col5.metric(
        "Cancelled",
        cancelled_bookings
    )

    st.markdown("---")

    if df.empty:

        st.info(
            "No bookings available. "
            "Go to Add Booking and create your first booking."
        )

    else:

        # ====================================================
        # STATUS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📊 Booking Status"
            )

            status_data = (
                df["booking_status"]
                .value_counts()
            )

            st.bar_chart(
                status_data
            )

        with col2:

            st.subheader(
                "🚌 Bookings by Operator"
            )

            operator_data = (
                df["bus_operator"]
                .value_counts()
                .head(10)
            )

            st.bar_chart(
                operator_data
            )

        # ====================================================
        # ROUTES + PAYMENT
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "🛣️ Top Routes"
            )

            route_data = (
                df["route"]
                .value_counts()
                .head(10)
            )

            st.bar_chart(
                route_data
            )

        with col2:

            st.subheader(
                "💳 Payment Methods"
            )

            payment_data = (
                df["payment_method"]
                .value_counts()
            )

            st.bar_chart(
                payment_data
            )

        # ====================================================
        # REVENUE
        # ====================================================

        st.subheader(
            "💰 Revenue by Bus Operator"
        )

        revenue_data = (
            df.groupby("bus_operator")[
                "total_amount"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            revenue_data
        )

        # ====================================================
        # MONTHLY BOOKINGS
        # ====================================================

        st.subheader(
            "📅 Bookings by Month"
        )

        month_data = (
            df["month"]
            .value_counts()
        )

        st.bar_chart(
            month_data
        )

        # ====================================================
        # RECENT BOOKINGS
        # ====================================================

        st.subheader(
            "📋 Recent Bookings"
        )

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )


# ============================================================
# ADD BOOKING
# ============================================================

elif menu == "➕ Add Booking":

    st.title(
        "➕ Add New Booking"
    )

    with st.form(
        "add_booking_form",
        clear_on_submit=True
    ):

        # ====================================================
        # CUSTOMER INFORMATION
        # ====================================================

        st.subheader(
            "👤 Customer Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            customer_id = st.text_input(
                "Customer ID"
            )

        with col2:

            customer_name = st.text_input(
                "Customer Name"
            )

        with col3:

            phone_number = st.text_input(
                "Phone Number",
                max_chars=10
            )

        col1, col2, col3 = st.columns(3)

        with col1:

            customer_email = st.text_input(
                "Gmail"
            )

        with col2:

            rating = st.number_input(
                "Rating",
                min_value=1.0,
                max_value=5.0,
                value=5.0,
                step=0.5
            )

        with col3:

            customer_age = st.number_input(
                "Customer Age",
                min_value=1,
                max_value=100,
                value=25
            )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        customer_type = st.selectbox(
            "Customer Type",
            [
                "New",
                "Returning",
                "Regular",
                "Corporate"
            ]
        )

        st.markdown("---")

        # ====================================================
        # JOURNEY INFORMATION
        # ====================================================

        st.subheader(
            "📅 Journey Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            booking_date = st.date_input(
                "Booking Date",
                value=date.today()
            )

        with col2:

            journey_date = st.date_input(
                "Journey Date",
                value=date.today()
            )

        col1, col2 = st.columns(2)

        with col1:

            source_city = st.text_input(
                "Source City"
            )

        with col2:

            destination_city = st.text_input(
                "Destination City"
            )

        st.markdown("---")

        # ====================================================
        # BUS INFORMATION
        # ====================================================

        st.subheader(
            "🚌 Bus Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            bus_operator = st.selectbox(
                "Bus Operator",
                [
                    "APSRTC",
                    "TSRTC",
                    "Orange Travels",
                    "VRL Travels",
                    "SRS Travels",
                    "Kaveri Travels",
                    "RedBus",
                    "Other"
                ]
            )

        with col2:

            bus_type = st.selectbox(
                "Bus Type",
                [
                    "AC Sleeper",
                    "Non-AC Sleeper",
                    "AC Seater",
                    "Non-AC Seater",
                    "Volvo",
                    "Semi Sleeper"
                ]
            )

        with col3:

            travel_duration_hours = st.number_input(
                "Travel Duration (Hours)",
                min_value=0.5,
                max_value=48.0,
                value=8.0,
                step=0.5
            )

        col1, col2 = st.columns(2)

        with col1:

            departure_time = st.time_input(
                "Departure Time",
                value=time(9, 0)
            )

        with col2:

            arrival_time = st.time_input(
                "Arrival Time",
                value=time(17, 0)
            )

        # ====================================================
        # SEAT INFORMATION
        # ====================================================

        st.subheader(
            "💺 Seat Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            total_seats = st.number_input(
                "Total Seats",
                min_value=1,
                max_value=100,
                value=40
            )

        with col2:

            available_seats = st.number_input(
                "Available Seats",
                min_value=0,
                max_value=100,
                value=40
            )

        with col3:

            number_of_passengers = st.number_input(
                "Number of Passengers",
                min_value=1,
                max_value=10,
                value=1
            )

        ticket_price = st.number_input(
            "Ticket Price",
            min_value=0.0,
            value=500.0,
            step=50.0
        )

        # ====================================================
        # PAYMENT
        # ====================================================

        st.subheader(
            "💳 Payment Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking",
                    "Cash",
                    "Wallet"
                ]
            )

        with col2:

            booking_status = st.selectbox(
                "Booking Status",
                [
                    "Confirmed",
                    "Pending",
                    "Cancelled"
                ]
            )

        cancellation_reason = st.text_input(
            "Cancellation Reason"
        )

        # ====================================================
        # HISTORICAL INFORMATION
        # ====================================================

        st.subheader(
            "📊 Historical Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            historical_bookings = st.number_input(
                "Historical Bookings",
                min_value=0,
                value=100
            )

        with col2:

            historical_avg_price = st.number_input(
                "Historical Average Price",
                min_value=0.0,
                value=500.0
            )

        with col3:

            historical_cancellation_rate = st.number_input(
                "Historical Cancellation Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0
            )

        is_holiday = st.checkbox(
            "Is Holiday?"
        )

        # ====================================================
        # SUBMIT
        # ====================================================

        submit = st.form_submit_button(
            "➕ Add Booking",
            use_container_width=True
        )

    # ========================================================
    # ADD PROCESS
    # ========================================================

    if submit:

        # ---------------- VALIDATION ----------------

        if not customer_id.strip():

            st.error(
                "Please enter Customer ID."
            )

            st.stop()

        if not customer_name.strip():

            st.error(
                "Please enter Customer Name."
            )

            st.stop()

        if not phone_number.isdigit() or len(phone_number) != 10:

            st.error(
                "Please enter a valid 10-digit phone number."
            )

            st.stop()

        if not customer_email.strip().lower().endswith("@gmail.com"):

            st.error(
                "Please enter a valid Gmail address."
            )

            st.stop()

        if not source_city.strip():

            st.error(
                "Please enter Source City."
            )

            st.stop()

        if not destination_city.strip():

            st.error(
                "Please enter Destination City."
            )

            st.stop()

        if journey_date < booking_date:

            st.error(
                "Journey Date cannot be before Booking Date."
            )

            st.stop()

        if available_seats > total_seats:

            st.error(
                "Available Seats cannot be greater than Total Seats."
            )

            st.stop()

        if number_of_passengers > available_seats:

            st.error(
                "Passengers cannot be greater than Available Seats."
            )

            st.stop()

        # ---------------- CALCULATIONS ----------------

        booking_id = generate_booking_id()

        days_before_journey = (
            journey_date - booking_date
        ).days

        route = (
            source_city.strip()
            + " → "
            + destination_city.strip()
        )

        day_of_week = (
            journey_date.strftime("%A")
        )

        month = (
            journey_date.strftime("%B")
        )

        is_weekend = (
            day_of_week
            in ["Saturday", "Sunday"]
        )

        peak_hour = (
            departure_time.hour
            in [
                7,
                8,
                9,
                17,
                18,
                19,
                20
            ]
        )

        season = calculate_season(
            journey_date.month
        )

        total_amount = (
            float(ticket_price)
            * int(number_of_passengers)
        )

        occupancy_rate = calculate_occupancy(
            int(total_seats),
            int(available_seats)
        )

        if booking_status != "Cancelled":

            cancellation_reason = ""

        # ---------------- CREATE RECORD ----------------

        new_record = {
            "booking_id": booking_id,
            "customer_id": customer_id.strip(),
            "customer_name": customer_name.strip(),
            "phone_number": phone_number.strip(),
            "customer_email": customer_email.strip().lower(),
            "rating": float(rating),
            "customer_age": int(customer_age),
            "gender": gender,
            "customer_type": customer_type,
            "booking_date": str(booking_date),
            "journey_date": str(journey_date),
            "days_before_journey": int(
                days_before_journey
            ),
            "source_city": source_city.strip(),
            "destination_city": destination_city.strip(),
            "route": route,
            "bus_operator": bus_operator,
            "bus_type": bus_type,
            "departure_time": departure_time.strftime(
                "%H:%M:%S"
            ),
            "arrival_time": arrival_time.strftime(
                "%H:%M:%S"
            ),
            "travel_duration_hours": float(
                travel_duration_hours
            ),
            "total_seats": int(
                total_seats
            ),
            "available_seats": int(
                available_seats
            ),
            "ticket_price": float(
                ticket_price
            ),
            "number_of_passengers": int(
                number_of_passengers
            ),
            "total_amount": float(
                total_amount
            ),
            "payment_method": payment_method,
            "booking_status": booking_status,
            "cancellation_reason": cancellation_reason,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": bool(
                is_weekend
            ),
            "is_holiday": bool(
                is_holiday
            ),
            "season": season,
            "peak_hour": bool(
                peak_hour
            ),
            "historical_bookings": int(
                historical_bookings
            ),
            "historical_avg_price": float(
                historical_avg_price
            ),
            "historical_cancellation_rate": float(
                historical_cancellation_rate
            ),
            "occupancy_rate": float(
                occupancy_rate
            )
        }

        new_row = pd.DataFrame(
            [new_record],
            columns=COLUMNS
        )

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df = clean_dataframe(df)

        save_data(df)

        st.success(
            f"✅ Booking created successfully!"
        )

        st.info(
            f"Booking ID: **{booking_id}**"
        )

        st.balloons()


# ============================================================
# UPDATE BOOKING
# ============================================================

elif menu == "✏️ Update Booking":

    st.title(
        "✏️ Update Booking"
    )

    if df.empty:

        st.warning(
            "No bookings available."
        )

    else:

        booking_ids = (
            df["booking_id"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        booking_ids = [
            x for x in booking_ids
            if x.strip() != ""
        ]

        if not booking_ids:

            st.warning(
                "No valid Booking IDs available."
            )

        else:

            selected_id = st.selectbox(
                "Select Booking ID",
                booking_ids
            )

            selected_rows = df[
                df["booking_id"]
                .astype(str)
                == selected_id
            ]

            if selected_rows.empty:

                st.error(
                    "Booking not found."
                )

            else:

                index = selected_rows.index[0]

                row = df.loc[index]

                st.subheader(
                    f"Updating: {selected_id}"
                )

                with st.form(
                    "update_booking_form"
                ):

                    # ----------------------------------------
                    # CUSTOMER
                    # ----------------------------------------

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        customer_name = st.text_input(
                            "Customer Name",
                            value=str(row["customer_name"])
                        )

                    with col2:

                        phone_number = st.text_input(
                            "Phone Number",
                            value=str(row["phone_number"]),
                            max_chars=10
                        )

                    with col3:

                        customer_email = st.text_input(
                            "Gmail",
                            value=str(row["customer_email"])
                        )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        rating = st.number_input(
                            "Rating",
                            min_value=1.0,
                            max_value=5.0,
                            value=float(row["rating"]),
                            step=0.5
                        )

                    with col2:

                        customer_age = st.number_input(
                            "Customer Age",
                            min_value=1,
                            max_value=100,
                            value=int(row["customer_age"])
                        )

                    with col3:

                        gender_options = [
                            "Male",
                            "Female",
                            "Other"
                        ]

                        current_gender = str(row["gender"])

                        gender_index = (
                            gender_options.index(current_gender)
                            if current_gender in gender_options
                            else 0
                        )

                        gender = st.selectbox(
                            "Gender",
                            gender_options,
                            index=gender_index
                        )

                    customer_type_options = [
                        "New",
                        "Returning",
                        "Regular",
                        "Corporate"
                    ]

                    current_type = str(row["customer_type"])

                    type_index = (
                        customer_type_options.index(current_type)
                        if current_type in customer_type_options
                        else 0
                    )

                    customer_type = st.selectbox(
                        "Customer Type",
                        customer_type_options,
                        index=type_index
                    )

                    # ----------------------------------------
                    # ROUTE
                    # ----------------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        source_city = st.text_input(
                            "Source City",
                            value=str(
                                row["source_city"]
                            )
                        )

                    with col2:

                        destination_city = st.text_input(
                            "Destination City",
                            value=str(
                                row["destination_city"]
                            )
                        )

                    # ----------------------------------------
                    # PRICE / SEATS
                    # ----------------------------------------

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        ticket_price = st.number_input(
                            "Ticket Price",
                            min_value=0.0,
                            value=float(
                                row["ticket_price"]
                            ),
                            step=50.0
                        )

                    with col2:

                        number_of_passengers = st.number_input(
                            "Number of Passengers",
                            min_value=1,
                            max_value=10,
                            value=max(
                                1,
                                int(
                                    row[
                                        "number_of_passengers"
                                    ]
                                )
                            )
                        )

                    with col3:

                        available_seats = st.number_input(
                            "Available Seats",
                            min_value=0,
                            max_value=100,
                            value=int(
                                row["available_seats"]
                            )
                        )

                    # ----------------------------------------
                    # PAYMENT
                    # ----------------------------------------

                    payment_options = [
                        "UPI",
                        "Credit Card",
                        "Debit Card",
                        "Net Banking",
                        "Cash",
                        "Wallet"
                    ]

                    current_payment = str(
                        row["payment_method"]
                    )

                    payment_index = (
                        payment_options.index(
                            current_payment
                        )
                        if current_payment
                        in payment_options
                        else 0
                    )

                    payment_method = st.selectbox(
                        "Payment Method",
                        payment_options,
                        index=payment_index
                    )

                    # ----------------------------------------
                    # STATUS
                    # ----------------------------------------

                    status_options = [
                        "Confirmed",
                        "Pending",
                        "Cancelled"
                    ]

                    current_status = str(
                        row["booking_status"]
                    )

                    status_index = (
                        status_options.index(
                            current_status
                        )
                        if current_status
                        in status_options
                        else 0
                    )

                    booking_status = st.selectbox(
                        "Booking Status",
                        status_options,
                        index=status_index
                    )

                    cancellation_reason = st.text_input(
                        "Cancellation Reason",
                        value=str(
                            row[
                                "cancellation_reason"
                            ]
                        )
                    )

                    update_button = st.form_submit_button(
                        "💾 Update Booking",
                        use_container_width=True
                    )

                # ============================================
                # PROCESS UPDATE
                # ============================================

                if update_button:

                    total_seats = int(
                        row["total_seats"]
                    )

                    if not customer_name.strip():

                        st.error(
                            "Customer Name is required."
                        )

                        st.stop()

                    if not phone_number.isdigit() or len(phone_number) != 10:

                        st.error(
                            "Please enter a valid 10-digit phone number."
                        )

                        st.stop()

                    if not customer_email.strip().lower().endswith("@gmail.com"):

                        st.error(
                            "Please enter a valid Gmail address."
                        )

                        st.stop()

                    if available_seats > total_seats:

                        st.error(
                            "Available Seats cannot exceed Total Seats."
                        )

                        st.stop()

                    if number_of_passengers > available_seats:

                        st.error(
                            "Passengers cannot exceed Available Seats."
                        )

                        st.stop()

                    if not source_city.strip():

                        st.error(
                            "Source City is required."
                        )

                        st.stop()

                    if not destination_city.strip():

                        st.error(
                            "Destination City is required."
                        )

                        st.stop()

                    if booking_status != "Cancelled":

                        cancellation_reason = ""

                    total_amount = (
                        float(ticket_price)
                        * int(number_of_passengers)
                    )

                    occupancy_rate = calculate_occupancy(
                        total_seats,
                        available_seats
                    )

                    # Create updated row

                    updated_row = row.copy()

                    updated_row[
                        "customer_name"
                    ] = str(
                        customer_name.strip()
                    )

                    updated_row[
                        "phone_number"
                    ] = str(
                        phone_number.strip()
                    )

                    updated_row[
                        "customer_email"
                    ] = str(
                        customer_email.strip().lower()
                    )

                    updated_row[
                        "rating"
                    ] = float(
                        rating
                    )

                    updated_row[
                        "customer_age"
                    ] = int(
                        customer_age
                    )

                    updated_row[
                        "gender"
                    ] = str(
                        gender
                    )

                    updated_row[
                        "customer_type"
                    ] = str(
                        customer_type
                    )

                    updated_row[
                        "source_city"
                    ] = str(
                        source_city.strip()
                    )

                    updated_row[
                        "destination_city"
                    ] = str(
                        destination_city.strip()
                    )

                    updated_row[
                        "route"
                    ] = (
                        source_city.strip()
                        + " → "
                        + destination_city.strip()
                    )

                    updated_row[
                        "ticket_price"
                    ] = float(
                        ticket_price
                    )

                    updated_row[
                        "number_of_passengers"
                    ] = int(
                        number_of_passengers
                    )

                    updated_row[
                        "available_seats"
                    ] = int(
                        available_seats
                    )

                    updated_row[
                        "total_amount"
                    ] = float(
                        total_amount
                    )

                    updated_row[
                        "payment_method"
                    ] = str(
                        payment_method
                    )

                    updated_row[
                        "booking_status"
                    ] = str(
                        booking_status
                    )

                    updated_row[
                        "cancellation_reason"
                    ] = str(
                        cancellation_reason
                    )

                    updated_row[
                        "occupancy_rate"
                    ] = float(
                        occupancy_rate
                    )

                    # Replace complete row

                    df.loc[index] = (
                        updated_row
                    )

                    # Clean dataframe

                    df = clean_dataframe(
                        df
                    )

                    # Save

                    save_data(
                        df
                    )

                    st.success(
                        f"✅ Booking {selected_id} updated successfully!"
                    )

                    st.rerun()


# ============================================================
# REMOVE BOOKING
# ============================================================

elif menu == "🗑️ Remove Booking":

    st.title(
        "🗑️ Remove Booking"
    )

    if df.empty:

        st.warning(
            "No bookings available to delete."
        )

    else:

        # Get valid booking IDs

        booking_ids = (
            df["booking_id"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        booking_ids = [
            x for x in booking_ids
            if x.strip() != ""
        ]

        if not booking_ids:

            st.warning(
                "No valid Booking IDs found."
            )

        else:

            selected_id = st.selectbox(
                "Select Booking ID",
                booking_ids
            )

            # Find selected booking

            selected_rows = df[
                df["booking_id"]
                .fillna("")
                .astype(str)
                == selected_id
            ]

            st.subheader(
                "📋 Booking Details"
            )

            if selected_rows.empty:

                st.error(
                    "Selected booking not found."
                )

            else:

                st.dataframe(
                    selected_rows,
                    use_container_width=True
                )

                st.markdown("---")

                confirm_delete = st.checkbox(
                    "⚠️ I confirm that I want to delete this booking."
                )

                if confirm_delete:

                    delete_button = st.button(
                        "🗑️ Delete Booking",
                        type="primary",
                        use_container_width=True
                    )

                    if delete_button:

                        # Create copy

                        updated_df = df.copy()

                        # Remove selected booking

                        updated_df = updated_df[
                            updated_df[
                                "booking_id"
                            ]
                            .fillna("")
                            .astype(str)
                            != selected_id
                        ].copy()

                        # Reset index

                        updated_df.reset_index(
                            drop=True,
                            inplace=True
                        )

                        # Clean data

                        updated_df = clean_dataframe(
                            updated_df
                        )

                        # Save

                        save_data(
                            updated_df
                        )

                        st.success(
                            f"✅ Booking {selected_id} deleted successfully!"
                        )

                        st.rerun()


# ============================================================
# SEARCH BOOKING
# ============================================================

elif menu == "🔍 Search Booking":

    st.title(
        "🔍 Search Booking"
    )

    search_text = st.text_input(
        "Search by Booking ID, Customer ID, Customer Name, Phone, Gmail, City or Route"
    )

    if search_text.strip():

        search_value = search_text.strip()

        search_mask = (
            df.astype(str)
            .apply(
                lambda column:
                column.str.contains(
                    search_value,
                    case=False,
                    na=False,
                    regex=False
                )
            )
            .any(axis=1)
        )

        results = df[
            search_mask
        ]

        if results.empty:

            st.warning(
                "No matching bookings found."
            )

        else:

            st.success(
                f"Found {len(results)} booking(s)."
            )

            st.dataframe(
                results,
                use_container_width=True
            )

    else:

        st.info(
            "Enter a Booking ID, Customer ID, City or Route."
        )


# ============================================================
# ALL BOOKINGS
# ============================================================

elif menu == "📋 All Bookings":

    st.title(
        "📋 All Bookings"
    )

    if df.empty:

        st.warning(
            "No booking records available."
        )

    else:

        st.write(
            f"Total Records: **{len(df)}**"
        )

        st.markdown("---")

        # ====================================================
        # FILTERS
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            status_values = sorted(
                [
                    x for x in
                    df["booking_status"]
                    .fillna("")
                    .astype(str)
                    .unique()
                    .tolist()
                    if x.strip() != ""
                ]
            )

            status_filter = st.selectbox(
                "Booking Status",
                ["All"] + status_values
            )

        with col2:

            operator_values = sorted(
                [
                    x for x in
                    df["bus_operator"]
                    .fillna("")
                    .astype(str)
                    .unique()
                    .tolist()
                    if x.strip() != ""
                ]
            )

            operator_filter = st.selectbox(
                "Bus Operator",
                ["All"] + operator_values
            )

        with col3:

            bus_values = sorted(
                [
                    x for x in
                    df["bus_type"]
                    .fillna("")
                    .astype(str)
                    .unique()
                    .tolist()
                    if x.strip() != ""
                ]
            )

            bus_filter = st.selectbox(
                "Bus Type",
                ["All"] + bus_values
            )

        # ====================================================
        # APPLY FILTERS
        # ====================================================

        filtered_df = df.copy()

        if status_filter != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "booking_status"
                ]
                == status_filter
            ]

        if operator_filter != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "bus_operator"
                ]
                == operator_filter
            ]

        if bus_filter != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "bus_type"
                ]
                == bus_filter
            ]

        # ====================================================
        # DISPLAY
        # ====================================================

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=550
        )

        # ====================================================
        # DOWNLOAD
        # ====================================================

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="bus_bookings_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )