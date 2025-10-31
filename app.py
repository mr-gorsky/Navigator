# Navigator VisionQuest - Color Vision Testing Suite
# Copyright © Toni Mandušić 2025

import streamlit as st
import os
from modules.lantern_test import lantern_test
from modules.farnsworth_test import farnsworth_test
from modules.ecdis_test import ecdis_test
from modules.ishihara_test import ishihara_test
from utils.evaluation import generate_final_report

# Page configuration
st.set_page_config(
    page_title="Navigator VisionQuest",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    if 'test_results' not in st.session_state:
        st.session_state.test_results = {}
    
    # Display main banner based on current page
    banner_path = f"assets/banners/{st.session_state.current_page}_banner.png"
    if os.path.exists(banner_path):
        st.image(banner_path, use_column_width=True)
    else:
        st.image("assets/banners/main_banner.png", use_column_width=True)
    
    # Sidebar navigation with icons
    with st.sidebar:
        st.header("🧭 Navigation")
        
        # Home button
        if st.button("🏠 **Home Dashboard**", use_container_width=True, 
                    type="primary" if st.session_state.current_page == "home" else "secondary"):
            st.session_state.current_page = "home"
            st.rerun()
        
        st.divider()
        st.subheader("🎯 Color Vision Tests")
        
        # Test buttons with icons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("", key="lantern_btn"):
                st.session_state.current_page = "lantern"
                st.rerun()
            st.image("assets/test_icons/lantern_icon.png", use_column_width=True)
            st.caption("Lantern Test")
            
            if st.button("", key="fm15_btn"):
                st.session_state.current_page = "fm15"
                st.rerun()
            st.image("assets/test_icons/fm15_icon.png", use_column_width=True)
            st.caption("FM15 Hue Test")
        
        with col2:
            if st.button("", key="ecdis_btn"):
                st.session_state.current_page = "ecdis"
                st.rerun()
            st.image("assets/test_icons/ecdis_icon.png", use_column_width=True)
            st.caption("ECDIS Test")
            
            if st.button("", key="ishihara_btn"):
                st.session_state.current_page = "ishihara"
                st.rerun()
            st.image("assets/test_icons/ishihara_icon.png", use_column_width=True)
            st.caption("Ishihara Test")
        
        st.divider()
        
        # Results dashboard
        if st.button("📊 **Results Dashboard**", use_container_width=True,
                    type="primary" if st.session_state.current_page == "results" else "secondary"):
            st.session_state.current_page = "results"
            st.rerun()
    
    # Main content area
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "lantern":
        lantern_test()
    elif st.session_state.current_page == "fm15":
        farnsworth_test()
    elif st.session_state.current_page == "ecdis":
        ecdis_test()
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    elif st.session_state.current_page == "results":
        show_results_dashboard()

def show_home_page():
    st.markdown("""
    ## 🚢 Welcome to Navigator VisionQuest
    
    **Professional Color Vision Testing Suite for Maritime Applications**
    
    ### Available Tests:
    
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png" width="80">
            <h3>🎯 Lantern Test</h3>
            <p>Simulates navigation light recognition under low-light conditions</p>
        </div>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png" width="80">
            <h3>🌈 FM15 Hue Test</h3>
            <p>Measures color discrimination ability with 15 hue variations</p>
        </div>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://i.postimg.cc/hvSkxQ0B/Gemini-Generated-Image-2mye5e2mye5e2mye.png" width="80">
            <h3>🗺️ ECDIS Test</h3>
            <p>Tests color recognition in electronic chart display systems</p>
        </div>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png" width="80">
            <h3>👁️ Ishihara Test</h3>
            <p>Standard red-green color deficiency screening test</p>
        </div>
    </div>
    
    ### Instructions:
    1. Complete all tests for comprehensive assessment
    2. Follow on-screen instructions carefully
    3. Ensure proper lighting conditions
    4. View results in the Dashboard after completion
    
    **Copyright © Toni Mandušić 2025 - For professional maritime use**
    """, unsafe_allow_html=True)

def show_results_dashboard():
    st.header("📊 Comprehensive Results Dashboard")
    
    if not st.session_state.test_results:
        st.warning("No test results available. Please complete at least one test.")
        return
    
    generate_final_report()

if __name__ == "__main__":
    main()