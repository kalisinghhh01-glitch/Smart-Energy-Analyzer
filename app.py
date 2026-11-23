
import streamlit as st
import subprocess
import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
ENGINE = ROOT / "energy_engine.exe"

st.set_page_config(
    page_title="Smart Energy Analyzer",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#081525,#102b3c,#0b1b2a);
    color: white;
}
[data-testid="stSidebar"] {
    background: #0b1b2a;
}
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(110deg,#123f50,#10273b);
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #285064;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 35px;
}
.hero p { color: #b8d0dc; }
.metric {
    background: #102b3c;
    border: 1px solid #285064;
    padding: 20px;
    border-radius: 15px;
}
.metric small { color: #a9c5d2; }
.metric h2 { color: white; margin-top: 8px; }
.stButton button {
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


def run_cpp(*args):
    if not ENGINE.exists():
        st.error("C++ engine missing. Run build.bat first.")
        st.stop()

    result = subprocess.run(
        [str(ENGINE), *map(str, args)],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    try:
        data = json.loads(result.stdout)
    except Exception:
        st.error("C++ engine error")
        st.code(result.stderr or result.stdout)
        st.stop()

    if not data.get("ok"):
        st.error(data.get("error", "Operation failed"))
        return None

    return data


def get_appliances():
    result = run_cpp("list")
    return result["appliances"] if result else []


st.markdown("""
<div class="hero">
<h1>⚡ Smart Energy Analyzer</h1>
<p>Intelligent Electricity Monitoring & Consumption Analytics</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("⚡ ENERGY ANALYZER")
    st.caption("SMART ELECTRICITY MONITORING")

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Appliance",
            "Energy Analysis",
            "Prediction",
            "Reports"
        ]
    )

    st.divider()
    st.caption("C++ Engine | Streamlit UI")
    st.caption("Academic Engineering Project")


appliances = get_appliances()
summary = run_cpp("summary")

if summary is None:
    st.stop()

total = summary["total_units"]
bill = summary["bill"]


# DASHBOARD

if page == "Dashboard":

    st.subheader("Energy Overview")

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (c1, "MONTHLY ENERGY", f"{total:.2f} kWh"),
        (c2, "ESTIMATED BILL", f"₹{bill:.2f}"),
        (c3, "APPLIANCES", str(len(appliances))),
        (c4, "USAGE STATUS", summary["level"])
    ]

    for col, label, value in cards:
        with col:
            st.markdown(
                f"""
                <div class="metric">
                <small>{label}</small>
                <h2>{value}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("Appliance Consumption")

        if appliances:
            df = pd.DataFrame(appliances)

            st.bar_chart(
                df.set_index("name")["energy"],
                color="#20C997"
            )

            st.dataframe(
                df.rename(columns={
                    "name": "Appliance",
                    "quantity": "Quantity",
                    "power": "Power (W)",
                    "hours": "Hours/Day",
                    "energy": "Monthly kWh"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No appliances added yet.")

    with right:
        st.subheader("Energy Insights")

        st.metric(
            "Highest Consuming Appliance",
            summary["highest_name"]
        )

        st.metric(
            "Monthly Consumption",
            f"{summary['highest_energy']:.2f} kWh"
        )

        if summary["level"] == "High":
            st.warning("High energy consumption detected.")
        elif summary["level"] == "Medium":
            st.info("Moderate energy consumption.")
        else:
            st.success("Energy consumption is low.")

        st.caption(
            "Sample thresholds: Low <100, "
            "Medium 100–300, High >300 kWh."
        )


# ADD APPLIANCE

elif page == "Add Appliance":

    st.subheader("➕ Appliance Management")
    st.write("Add an electrical appliance to your energy profile.")

    with st.form("appliance_form", clear_on_submit=True):

        name = st.text_input(
            "Appliance Name",
            placeholder="Example: Ceiling Fan"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            quantity = st.number_input(
                "Quantity", 1, 100, 1
            )

        with c2:
            power = st.number_input(
                "Power Rating (Watts)",
                1.0, 20000.0, 75.0
            )

        with c3:
            hours = st.number_input(
                "Daily Usage (Hours)",
                0.1, 24.0, 8.0
            )

        submitted = st.form_submit_button(
            "Save Appliance",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Enter an appliance name.")
            else:
                result = run_cpp(
                    "add",
                    name.strip(),
                    int(quantity),
                    power,
                    hours
                )

                if result:
                    st.success(result["message"])
                    st.rerun()

    if appliances:

        st.divider()
        st.subheader("Saved Appliances")

        df = pd.DataFrame(appliances)

        st.dataframe(
            df[["name", "quantity", "power", "hours"]],
            use_container_width=True,
            hide_index=True
        )

        options = {
            f"{a['name']} - {a['quantity']} unit(s)": i
            for i, a in enumerate(appliances)
        }

        selected = st.selectbox(
            "Select appliance to delete",
            list(options.keys())
        )

        if st.button("Delete Appliance"):
            result = run_cpp("delete", options[selected])

            if result:
                st.success(result["message"])
                st.rerun()


# ENERGY ANALYSIS

elif page == "Energy Analysis":

    st.subheader("📊 Consumption Analysis")

    c1, c2, c3 = st.columns(3)

    c1.metric("Monthly Units", f"{total:.2f} kWh")
    c2.metric("Estimated Bill", f"₹{bill:.2f}")
    c3.metric("Usage Level", summary["level"])

    st.divider()

    st.subheader("💡 Energy Saving Recommendations")

    tips = [
        "Switch off appliances when not in use.",
        "Replace traditional bulbs with LED lights.",
        "Reduce unnecessary appliance operating hours.",
        "Avoid leaving electronic devices on standby.",
        "Prefer energy-efficient appliances."
    ]

    for tip in tips:
        st.markdown(f"✓ {tip}")

    st.caption(
        "Bill is based on illustrative academic tariff slabs, "
        "not actual electricity-board rates."
    )


# PREDICTION

elif page == "Prediction":

    st.subheader("🔮 Next Month Consumption Prediction")

    st.write(
        "Enter previous and current monthly electricity readings."
    )

    with st.form("prediction_form"):

        c1, c2 = st.columns(2)

        previous = c1.number_input(
            "Previous Month (kWh)",
            min_value=0.0,
            value=100.0
        )

        current = c2.number_input(
            "Current Month (kWh)",
            min_value=0.0,
            value=float(total)
        )

        submitted = st.form_submit_button(
            "Predict Next Month",
            type="primary"
        )

        if submitted:

            result = run_cpp(
                "predict",
                previous,
                current
            )

            if result:
                st.success(
                    f"Predicted Usage: "
                    f"{result['prediction']:.2f} kWh"
                )

                st.caption(
                    "Uses a two-month average. "
                    "This is a basic statistical estimate, "
                    "not a trained AI/ML model."
                )


# REPORTS

elif page == "Reports":

    st.subheader("📄 Generate Energy Report")

    st.write(
        "Generate a detailed report of all registered appliances."
    )

    if st.button(
        "Generate Final Report",
        type="primary",
        use_container_width=True
    ):

        result = run_cpp("report")

        if result:

            report_path = ROOT / "Energy_Report.txt"

            content = report_path.read_text(
                encoding="utf-8"
            )

            st.success("Report generated successfully!")

            st.code(content, language="text")

            st.download_button(
                "Download Report",
                content,
                file_name="Energy_Report.txt",
                mime="text/plain"
            )


st.divider()

st.caption(
    "Smart Electrical Consumption Analyzer | "
    "C++ Core Engine + Python Streamlit Interface | "
    "Academic Project"
)
