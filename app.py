
import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CareCircle | Elderly Care",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION DATA ----------------
if "medicines" not in st.session_state:
    st.session_state.medicines = [
        {"Medicine": "Morning Tablet", "Time": "09:00 AM",
         "Dosage": "1 tablet", "Status": "Pending"},
        {"Medicine": "Vitamin Supplement", "Time": "02:00 PM",
         "Dosage": "1 tablet", "Status": "Pending"},
    ]

if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "checkins" not in st.session_state:
    st.session_state.checkins = []

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "Senior Name": "Grandpa",
        "Age": 75,
        "Family Contact": "+91 98765 43210",
        "City": "Kasganj"
    }

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: #f5f9fc;
}

[data-testid="stSidebar"] {
    background-color: #e8f6f1;
}

.hero {
    background: linear-gradient(120deg, #e2f7ef, #e7f1ff);
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #d4ebe4;
    margin-bottom: 20px;
}

.hero h1 {
    color: #124b46;
    font-size: 34px;
    margin-bottom: 6px;
}

.hero p {
    color: #385e61;
    font-size: 17px;
}

.section-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2ebef;
    margin-bottom: 12px;
}

.metric-card {
    background: white;
    border: 1px solid #e0ecea;
    border-radius: 16px;
    padding: 18px;
}

.small-note {
    color: #637782;
    font-size: 13px;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #b7ddd0;
    background-color: #e4f5ed;
    color: #165a49;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #d2eee2;
    color: #104c3d;
    border-color: #91cbb5;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #e0ecea;
}

h1, h2, h3 {
    color: #153f51;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPER FUNCTIONS ----------------
def heading(title, description=None):
    st.header(title)
    if description:
        st.caption(description)


def show_medicines():
    medicines = st.session_state.medicines

    if not medicines:
        st.info("No medicines added yet.")
        return

    df = pd.DataFrame(medicines)
    st.dataframe(df, use_container_width=True, hide_index=True)

    pending = [
        i for i, medicine in enumerate(medicines)
        if medicine["Status"] == "Pending"
    ]

    if pending:
        choices = {
            f'{medicines[i]["Medicine"]} — {medicines[i]["Time"]}': i
            for i in pending
        }

        selected = st.selectbox(
            "Select medicine to mark as taken",
            list(choices.keys()),
            key="medicine_to_complete"
        )

        if st.button("✓ Mark as Taken", key="mark_taken"):
            index = choices[selected]
            st.session_state.medicines[index]["Status"] = "Taken"
            st.success("Medicine marked as taken in this demo.")
            st.rerun()


def show_appointments():
    if st.session_state.appointments:
        st.dataframe(
            pd.DataFrame(st.session_state.appointments),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No appointments scheduled yet.")


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 💚 CareCircle")
    st.caption("Connect • Care • Keep Them Safe")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home Dashboard",
            "💊 Medicines",
            "📅 Appointments",
            "🆘 Emergency SOS",
            "💚 Daily Check-in",
            "👩‍⚕️ Find Caregiver",
            "👨‍👩‍👧 Family Reports",
            "⚙️ My Profile"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**Your care, connected.**")
    st.caption("A student/startup prototype.")
    st.caption("Demo data is stored in this session.")


# ---------------- HOME DASHBOARD ----------------
if page == "🏠 Home Dashboard":
    profile = st.session_state.profile

    st.markdown(f"""
    <div class="hero">
        <h1>💚 Hello, {profile['Senior Name']}!</h1>
        <p>Your wellbeing matters. Let's make today safe and happy.</p>
        <b>CareCircle — Smart and Affordable Elderly Care</b>
    </div>
    """, unsafe_allow_html=True)

    total_meds = len(st.session_state.medicines)
    taken_meds = sum(
        m["Status"] == "Taken"
        for m in st.session_state.medicines
    )
    pending_meds = total_meds - taken_meds

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💊 Total Medicines", total_meds)
    c2.metric("✓ Taken", taken_meds)
    c3.metric("⏰ Pending", pending_meds)
    c4.metric("📅 Appointments", len(st.session_state.appointments))

    st.markdown("### Quick Actions")

    a, b, c = st.columns(3)

    with a:
        st.markdown("#### 💊 Medicines")
        st.write("Review today's medication schedule.")
        if st.button("View Medicines", use_container_width=True):
            st.session_state.navigate_to = "💊 Medicines"
            st.rerun()

    with b:
        st.markdown("#### 💚 Daily Check-in")
        st.write("Record your mood and wellbeing.")
        if st.button("Check In Now", use_container_width=True):
            st.session_state.navigate_to = "💚 Daily Check-in"
            st.rerun()

    with c:
        st.markdown("#### 🆘 Emergency")
        st.write("Open the emergency alert demo.")
        if st.button("Open SOS", use_container_width=True):
            st.session_state.navigate_to = "🆘 Emergency SOS"
            st.rerun()

    st.markdown("### Today's Care Overview")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("💊 Medication Progress")
        if total_meds:
            st.progress(taken_meds / total_meds)
            st.write(f"{taken_meds} of {total_meds} medicines marked as taken.")
        else:
            st.write("Add a medicine to start tracking.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📞 Family Connection")
        st.write(f"**Family contact:** {profile['Family Contact']}")
        st.write(f"**Location:** {profile['City']}")
        st.caption("Contact details are for demonstration only.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Recent Wellbeing Check-ins")
    if st.session_state.checkins:
        st.dataframe(
            pd.DataFrame(st.session_state.checkins[-5:][::-1]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No check-ins yet. Visit Daily Check-in to add one.")


# ---------------- MEDICINES ----------------
elif page == "💊 Medicines":
    heading("💊 Medicine Reminders", "Keep track of your medication schedule.")

    with st.expander("➕ Add a Medicine", expanded=False):
        with st.form("medicine_form", clear_on_submit=True):
            medicine_name = st.text_input("Medicine name")
            dosage = st.text_input("Dosage", placeholder="e.g. 1 tablet")
            medicine_time = st.time_input(
                "Reminder time",
                value=time(9, 0)
            )
            add_medicine = st.form_submit_button("Add Medicine")

            if add_medicine:
                if medicine_name.strip() and dosage.strip():
                    st.session_state.medicines.append({
                        "Medicine": medicine_name.strip(),
                        "Time": medicine_time.strftime("%I:%M %p"),
                        "Dosage": dosage.strip(),
                        "Status": "Pending"
                    })
                    st.success("Medicine added successfully.")
                    st.rerun()
                else:
                    st.error("Please enter both medicine name and dosage.")

    show_medicines()

    st.warning(
        "This is a tracking prototype, not an automatic alarm or medical "
        "recommendation system. Follow your clinician's instructions."
    )


# ---------------- APPOINTMENTS ----------------
elif page == "📅 Appointments":
    heading("📅 Appointments", "Organize medical visits and follow-ups.")

    with st.form("appointment_form", clear_on_submit=True):
        doctor = st.text_input("Doctor / Hospital name")
        appointment_date = st.date_input(
            "Appointment date",
            value=date.today()
        )
        appointment_time = st.time_input(
            "Appointment time",
            value=time(10, 0)
        )
        reason = st.text_input("Purpose of visit")
        submit_appointment = st.form_submit_button("Save Appointment")

        if submit_appointment:
            if doctor.strip() and reason.strip():
                st.session_state.appointments.append({
                    "Doctor / Hospital": doctor.strip(),
                    "Date": str(appointment_date),
                    "Time": appointment_time.strftime("%I:%M %p"),
                    "Purpose": reason.strip()
                })
                st.success("Appointment saved.")
                st.rerun()
            else:
                st.error("Please enter the doctor and appointment purpose.")

    st.markdown("### Your Appointments")
    show_appointments()


# ---------------- EMERGENCY SOS ----------------
elif page == "🆘 Emergency SOS":
    heading(
        "🆘 Emergency Assistance",
        "Demonstration of an emergency alert workflow."
    )

    profile = st.session_state.profile

    st.markdown(
        '<div class="section-card">'
        '<h3>Emergency Contact</h3>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(f"**Name:** {profile['Senior Name']}")
    st.write(f"**Family contact:** {profile['Family Contact']}")
    st.write(f"**City:** {profile['City']}")

    st.error(
        "Only use the demo alert for testing. This prototype does not "
        "automatically contact emergency services or send SMS messages."
    )

    reason = st.selectbox(
        "What kind of help is needed?",
        [
            "Medical assistance",
            "Fall or mobility assistance",
            "Feeling unwell",
            "Other emergency"
        ]
    )

    confirm = st.checkbox(
        "I understand this creates a demo alert only."
    )

    if st.button("🆘 Create Emergency Demo Alert", use_container_width=True):
        if confirm:
            st.session_state.alerts.append({
                "Time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
                "Reason": reason,
                "Status": "Demo alert created — not sent"
            })
            st.warning(
                "Demo alert recorded inside the app. "
                "No message was sent to your family."
            )
            st.rerun()
        else:
            st.info("Please confirm that you understand the demo limitations.")

    if st.session_state.alerts:
        st.markdown("### Alert History")
        st.dataframe(
            pd.DataFrame(st.session_state.alerts[::-1]),
            use_container_width=True,
            hide_index=True
        )


# ---------------- DAILY CHECK-IN ----------------
elif page == "💚 Daily Check-in":
    heading(
        "💚 Daily Wellbeing Check-in",
        "A simple way to record how you are feeling."
    )

    with st.form("checkin_form", clear_on_submit=True):
        mood = st.select_slider(
            "How are you feeling today?",
            options=["Very Sad", "Sad", "Okay", "Good", "Very Happy"],
            value="Good"
        )

        wellbeing = st.radio(
            "How is your overall wellbeing?",
            ["Feeling well", "Need some assistance", "Feeling unwell"]
        )

        notes = st.text_area(
            "Anything you would like your family to know?",
            placeholder="Write a short note (optional)."
        )

        save_checkin = st.form_submit_button("Save Daily Check-in")

        if save_checkin:
            st.session_state.checkins.append({
                "Date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "Mood": mood,
                "Wellbeing": wellbeing,
                "Notes": notes.strip()
            })
            st.success("Your check-in has been recorded in this session.")
            st.rerun()

    if st.session_state.checkins:
        st.markdown("### Previous Check-ins")
        st.dataframe(
            pd.DataFrame(st.session_state.checkins[::-1]),
            use_container_width=True,
            hide_index=True
        )


# ---------------- CAREGIVER BOOKING ----------------
elif page == "👩‍⚕️ Find Caregiver":
    heading(
        "👩‍⚕️ Find a Caregiver",
        "Explore sample local care services."
    )

    caregivers = [
        {
            "name": "Anita Sharma",
            "service": "Daily Home Assistance",
            "experience": "5 years",
            "price": "₹400 / visit"
        },
        {
            "name": "Rahul Verma",
            "service": "Companionship & Errands",
            "experience": "3 years",
            "price": "₹300 / visit"
        },
        {
            "name": "Sunita Singh",
            "service": "Senior Support",
            "experience": "7 years",
            "price": "₹500 / visit"
        }
    ]

    for caregiver in caregivers:
        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.subheader(f"👤 {caregiver['name']}")
                st.write(f"**Service:** {caregiver['service']}")
                st.write(f"**Experience:** {caregiver['experience']}")
                st.write(f"**Indicative price:** {caregiver['price']}")

            with right:
                st.caption("Sample profile")
                if st.button(
                    "Request Booking",
                    key="book_" + caregiver["name"].replace(" ", "_")
                ):
                    st.session_state.selected_caregiver = caregiver["name"]
                    st.rerun()

    selected_caregiver = st.session_state.get("selected_caregiver")

    if selected_caregiver:
        st.markdown("---")
        st.subheader(f"Booking Request: {selected_caregiver}")

        with st.form("booking_form", clear_on_submit=True):
            service_date = st.date_input(
                "Preferred date",
                value=date.today(),
                key="service_date"
            )
            service_time = st.time_input(
                "Preferred time",
                value=time(10, 0),
                key="service_time"
            )
            service_type = st.selectbox(
                "Type of assistance",
                [
                    "Daily Home Assistance",
                    "Companionship & Errands",
                    "Senior Support"
                ]
            )
            customer_phone = st.text_input("Your contact number")
            submit_booking = st.form_submit_button("Submit Booking Request")

            if submit_booking:
                if customer_phone.strip():
                    st.session_state.bookings.append({
                        "Caregiver": selected_caregiver,
                        "Service": service_type,
                        "Date": str(service_date),
                        "Time": service_time.strftime("%I:%M %p"),
                        "Contact": customer_phone.strip(),
                        "Status": "Demo request received"
                    })
                    st.session_state.pop("selected_caregiver", None)
                    st.success("Demo booking request saved.")
                    st.rerun()
                else:
                    st.error("Please enter a contact number.")

    st.info(
        "These caregiver profiles and prices are fictional examples. "
        "No real caregiver has been verified or booked."
    )


# ---------------- FAMILY REPORTS ----------------
elif page == "👨‍👩‍👧 Family Reports":
    heading(
        "👨‍👩‍👧 Family Wellbeing Reports",
        "Review the information recorded during this demo session."
    )

    checkins = st.session_state.checkins
    medicines = st.session_state.medicines

    c1, c2, c3 = st.columns(3)

    c1.metric("Check-ins Recorded", len(checkins))
    c2.metric("Medicines Taken", sum(
        m["Status"] == "Taken" for m in medicines
    ))
    c3.metric("Booking Requests", len(st.session_state.bookings))

    st.markdown("### Wellbeing History")
    if checkins:
        df = pd.DataFrame(checkins)
        st.dataframe(df, use_container_width=True, hide_index=True)

        mood_counts = df["Mood"].value_counts()
        st.markdown("#### Mood Summary")
        st.bar_chart(mood_counts)
    else:
        st.info("No wellbeing records are available yet.")

    st.markdown("### Caregiver Requests")
    if st.session_state.bookings:
        st.dataframe(
            pd.DataFrame(st.session_state.bookings),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No caregiver requests have been recorded.")

    st.markdown("### Export Demo Data")
    if checkins:
        csv_data = pd.DataFrame(checkins).to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Wellbeing Report (CSV)",
            data=csv_data,
            file_name="carecircle_wellbeing_report.csv",
            mime="text/csv"
        )

    if medicines:
        med_csv = pd.DataFrame(medicines).to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Medicine Report (CSV)",
            data=med_csv,
            file_name="carecircle_medicine_report.csv",
            mime="text/csv"
        )


# ---------------- PROFILE ----------------
elif page == "⚙️ My Profile":
    heading(
        "⚙️ My Profile",
        "Manage the basic details shown in your prototype."
    )

    profile = st.session_state.profile

    with st.form("profile_form"):
        name = st.text_input("Senior citizen's name", profile["Senior Name"])
        age = st.number_input(
            "Age", min_value=60, max_value=120,
            value=int(profile["Age"])
        )
        phone = st.text_input(
            "Family contact number", profile["Family Contact"]
        )
        city = st.text_input("City", profile["City"])

        save_profile = st.form_submit_button("Save Profile")

        if save_profile:
            if name.strip() and phone.strip() and city.strip():
                st.session_state.profile = {
                    "Senior Name": name.strip(),
                    "Age": int(age),
                    "Family Contact": phone.strip(),
                    "City": city.strip()
                }
                st.success("Profile updated for this demo session.")
                st.rerun()
            else:
                st.error("Please fill in all profile fields.")

    st.caption(
        "Use fictional contact information while demonstrating this prototype."
    )


# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<div style='text-align:center;color:#52706f;padding:10px'>"
    "💚 <b>CareCircle</b> | Small Steps Today, A Safer Tomorrow"
    "</div>",
    unsafe_allow_html=True
)
