# Navigator VisionQuest - Color Vision Testing Suite
# Copyright © Toni Mandušić 2025

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Navigator VisionQuest",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚢 Navigator VisionQuest")
    st.subheader("Professional Color Vision Testing Suite for Maritime Applications")
    
    st.success("✅ Application is now running!")
    
    # Test selection
    st.header("🎯 Available Tests")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png", width=100)
        if st.button("Lantern Test", use_container_width=True):
            st.session_state.current_test = "lantern"
            st.rerun()
    
    with col2:
        st.image("https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png", width=100)
        if st.button("FM15 Hue Test", use_container_width=True):
            st.session_state.current_test = "fm15"
            st.rerun()
    
    with col3:
        st.image("https://i.postimg.cc/hvSkxQ0B/Gemini-Generated-Image-2mye5e2mye5e2mye.png", width=100)
        if st.button("ECDIS Test", use_container_width=True):
            st.session_state.current_test = "ecdis"
            st.rerun()
    
    with col4:
        st.image("https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png", width=100)
        if st.button("Ishihara Test", use_container_width=True):
            st.session_state.current_test = "ishihara"
            st.rerun()
    
    # Test content
    if 'current_test' in st.session_state:
        st.divider()
        
        if st.session_state.current_test == "lantern":
            st.header("🎯 Lantern Test")
            st.info("Navigation light recognition simulation - Coming Soon")
            
        elif st.session_state.current_test == "fm15":
            st.header("🌈 FM15 Hue Test") 
            st.info("Color discrimination test - Coming Soon")
            
        elif st.session_state.current_test == "ecdis":
            st.header("🗺️ ECDIS Test")
            st.info("Electronic chart display test - Coming Soon")
            
        elif st.session_state.current_test == "ishihara":
            st.header("👁️ Ishihara Test")
            st.info("Color deficiency screening - Coming Soon")
        
        if st.button("← Back to Main Menu"):
            del st.session_state.current_test
            st.rerun()
    
    st.divider()
    st.markdown("**Copyright © Toni Mandušić 2025**")

if __name__ == "__main__":
    main()