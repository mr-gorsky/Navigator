# Navigator VisionQuest - Color Vision Testing Suite
# Copyright © Toni Mandušić 2025

import streamlit as st

st.set_page_config(
    page_title="Navigator VisionQuest",
    page_icon="🚢",
    layout="wide"
)

def main():
    # Koristi ONLINE banner umjesto lokalnog
    st.image("https://i.postimg.cc/fbcrnNXC/Gemini-Generated-Image-6gukqc6gukqc6guk.png", use_column_width=True)
    
    st.title("🚢 Navigator VisionQuest")
    st.subheader("Professional Color Vision Testing Suite for Maritime Applications")
    
    st.success("🎉 Application is now running successfully!")
    
    # Test selection with ONLINE icons
    st.header("🎯 Available Tests")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png", width=100)
        st.write("**Lantern Test**")
        st.write("Navigation light recognition")
        
    with col2:
        st.image("https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png", width=100)
        st.write("**FM15 Hue Test**")
        st.write("Color discrimination")
        
    with col3:
        st.image("https://i.postimg.cc/hvSkxQ0B/Gemini-Generated-Image-2mye5e2mye5e2mye.png", width=100)
        st.write("**ECDIS Test**")
        st.write("Chart display colors")
        
    with col4:
        st.image("https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png", width=100)
        st.write("**Ishihara Test**")
        st.write("Color deficiency screening")
    
    st.divider()
    st.markdown("**Copyright © Toni Mandušić 2025**")

if __name__ == "__main__":
    main()