# Navigator VisionQuest - Color Vision Testing Suite
# Copyright © Toni Mandušić 2025

import streamlit as st

st.set_page_config(
    page_title="Navigator VisionQuest",
    page_icon="🚢",
    layout="wide"
)

def main():
    st.title("🚢 Navigator VisionQuest")
    st.subheader("Professional Color Vision Testing Suite for Maritime Applications")
    
    st.success("✅ Application deployed successfully!")
    
    # Simple test navigation
    st.header("Available Tests")
    
    test_option = st.selectbox(
        "Choose a test to run:",
        ["Select a test", "Lantern Test", "FM15 Hue Test", "ECDIS Test", "Ishihara Test"]
    )
    
    if test_option != "Select a test":
        st.info(f"{test_option} - Implementation coming soon")
        
        if test_option == "Ishihara Test":
            st.write("This will contain the standard Ishihara plates")
        elif test_option == "Lantern Test":
            st.write("This will simulate navigation lights")
        elif test_option == "FM15 Hue Test":
            st.write("This will test color discrimination")
        elif test_option == "ECDIS Test":
            st.write("This will test ECDIS color recognition")
    
    st.divider()
    st.markdown("**Copyright © Toni Mandušić 2025**")

if __name__ == "__main__":
    main()