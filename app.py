import streamlit as st
from streamlit_option_menu import option_menu
from system_overview import get_system_overview
from incident_resolution import resolve_incident, get_alternative_solution
from documentation import document_incident
import json


st.set_page_config(page_title="AI-PHASE Ops Assistant", page_icon="🤖", layout="wide")


st.markdown("""
<style>
    body {
        color: white;
        background-color: black;
    }
    .reportview-container {
        background: black;
        color: white;
    }
    .main {
        background-color: black;
    }
    .stButton>button {
        color: white;
        border-radius: 50px;
        height: 3em;
        width: 100%;
        background-color: #4F8BF9;
        border: none;
        font-size: 1.2em;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a6fd9;
    }
    .stTextInput>div>div>input {
        border-radius: 50px;
        background-color: #1E1E1E;
        color: white;
    }
    .stSelectbox>div>div>input {
        border-radius: 50px;
        background-color: #1E1E1E;
        color: white;
    }
    .stExpander {
        background-color: #1E1E1E;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
    }
    .css-145kmo2 {
        color: white;
    }
    .css-1d391kg {
        background-color: #1E1E1E;
    }
</style>
""", unsafe_allow_html=True)

# Headline
st.markdown("<h1 style='text-align: center; color: #4F8BF9;'>AI-PHASE: Powering the Future of IT Operations</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #fafafa;'>Intelligent Solutions, Seamless Performance</h3>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Incident Resolution"],
        icons=["speedometer2", "tools"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1E1E1E"},
            "icon": {"color": "#4F8BF9", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#2E2E2E"},
            "nav-link-selected": {"background-color": "#2E2E2E"},
        }
    )

if selected == "Dashboard":
    st.title("🎛️ AI Ops Dashboard")

    # System Overview
    st.header("System Overview")
    
    if st.button("Refresh System Overview", key="refresh_overview"):
        with st.spinner("Fetching system overview..."):
            overview = get_system_overview()
        st.session_state.system_overview = overview

    if 'system_overview' in st.session_state:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create a simple table for system status
            st.table(
                {"System": list(st.session_state.system_overview['raw_data'].keys()),
                 "Status": [data['status'] for data in st.session_state.system_overview['raw_data'].values()]}
            )

        with col2:
            st.subheader("System Summary")
            st.info(st.session_state.system_overview['summary'])

elif selected == "Incident Resolution":
    st.title("🛠️ Incident Resolution")

    # Predefined IT issues
    it_issues = [
        "Select an issue",
        "Network connectivity problems",
        "Software installation issues",
        "Hardware malfunction",
        "Email configuration",
        "Data backup and recovery",
        "Security concerns",
        "Other (please describe)"
    ]

    # Use session state to store the selected issue
    if 'selected_issue' not in st.session_state:
        st.session_state.selected_issue = "Select an issue"

    selected_issue = st.selectbox("Select an IT issue:", it_issues, key="issue_selector", index=it_issues.index(st.session_state.selected_issue))

    # Update session state when a new issue is selected
    if selected_issue != st.session_state.selected_issue:
        st.session_state.selected_issue = selected_issue
        st.session_state.issue_description = None  # Reset description when a new issue is selected

    if selected_issue == "Other (please describe)":
        # Use session state to store the issue description
        if 'issue_description' not in st.session_state:
            st.session_state.issue_description = ""
        
        issue_description = st.text_area("Describe the issue:", value=st.session_state.issue_description, key="issue_description")
        
        # Update session state when the description changes
        if issue_description != st.session_state.issue_description:
            st.session_state.issue_description = issue_description
    else:
        issue_description = selected_issue

    if issue_description and issue_description != "Select an issue":
        # Use a form to capture the Enter key press
        with st.form(key='resolve_form'):
            submit_button = st.form_submit_button(label='Resolve Incident')
        
        if submit_button or st.session_state.get('resolve_pressed', False):
            st.session_state.resolve_pressed = True
            with st.spinner("Analyzing and resolving the incident..."):
                system_context = json.dumps(st.session_state.get('system_overview', {}))
                resolution = resolve_incident(issue_description, system_context)
            
            st.success("Resolution Generated")
            with st.expander("View Suggested Resolution", expanded=True):
                st.write(resolution)
            
            # Store the resolution in session state
            st.session_state.last_resolution = resolution
            
            # Ask user if the issue is resolved
            is_resolved = st.radio("Has your issue been resolved?", ("Select an option", "Yes", "No"))
            
            if is_resolved != "Select an option":
                if st.button("Submit Feedback", key="submit_feedback"):
                    if is_resolved == "Yes":
                        result = document_incident(issue_description, resolution, "resolved")
                        st.success("Issue documented as resolved.")
                    else:
                        result = document_incident(issue_description, resolution, "unresolved")
                        st.warning("Issue documented as unresolved.")
                    
                    # Add the current solution to previous solutions
                    if 'previous_solutions' not in st.session_state:
                        st.session_state.previous_solutions = []
                    st.session_state.previous_solutions.append(resolution)
                    
                    # Clear the form for the next issue
                    st.session_state.selected_issue = "Select an issue"
                    st.session_state.issue_description = None
                    st.session_state.resolve_pressed = False
                    st.rerun()
            
            # Alternative solution
            if st.button("Get Alternative Solution"):
                with st.spinner("Generating alternative solution..."):
                    alt_resolution = get_alternative_solution(issue_description, system_context)
                st.info("Alternative Solution Generated")
                with st.expander("View Alternative Solution", expanded=True):
                    st.write(alt_resolution)
                st.session_state.last_alt_resolution = alt_resolution

                # Show previous solutions after generating alternative solution
                if 'previous_solutions' in st.session_state and len(st.session_state.previous_solutions) > 0:
                    st.subheader("Previous Solutions")
                    for i, solution in enumerate(st.session_state.previous_solutions):
                        with st.expander(f"Solution {i+1}", expanded=False):
                            st.write(solution)

    # Previous Solutions
    if 'previous_solutions' in st.session_state and len(st.session_state.previous_solutions) > 0:
        if st.button("View Previous Solutions"):
            for i, solution in enumerate(st.session_state.previous_solutions):
                with st.expander(f"Solution {i+1}", expanded=False):
                    st.write(solution)

