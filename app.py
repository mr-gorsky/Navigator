import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Page configuration
st.set_page_config(
    page_title="VisionQuest Navigator",
    page_icon="⚓",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'ishihara_answers' not in st.session_state:
    st.session_state.ishihara_answers = []
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}

# Header
st.image("https://i.postimg.cc/fbcrnNXC/Gemini-Generated-Image-6gukqc6gukqc6guk.png", use_column_width=True)

# Sidebar
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "🎯 Ishihara Test", "🌈 Farnsworth Test", "💡 Lantern Test", "📊 Results"])

st.sidebar.title("👤 Mariner Info")
name = st.sidebar.text_input("Full Name")
rank = st.sidebar.selectbox("Rank", ["Captain", "Officer", "Cadet", "Other"])

# Home Page
if page == "🏠 Home":
    st.title("🚢 VisionQuest Navigator")
    st.subheader("Comprehensive Maritime Vision Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Why This Testing Matters**")
        st.write("""
        Traditional Ishihara tests alone are insufficient for maritime professionals. 
        Modern navigation requires accurate color perception in various conditions:
        - ECDIS displays with specialized color palettes
        - Navigation lights recognition at distance  
        - Radar displays with color-coded targets
        - Buoy identification in different lighting
        """)
        
    with col2:
        st.write("**Testing Protocol**")
        st.write("""
        1. Complete all tests in sequence
        2. Ensure proper lighting conditions
        3. Maintain normal viewing distance
        4. Do not adjust screen colors
        5. Record your results for review
        """)
    
    st.info("⚠️ **Important:** Use a calibrated monitor in controlled lighting for accurate results.")
    
    if st.button("🚀 START TESTING", type="primary", use_container_width=True):
        st.session_state.page = "ishihara"
        st.session_state.ishihara_answers = []
        st.rerun()

# Ishihara Test
elif page == "🎯 Ishihara Test":
    st.title("🎯 Ishihara Color Vision Test")
    st.write("**Instructions:** Identify the numbers you see in each circle. Type the number or '0' if no number visible.")
    
    plates = [
        {"number": "12", "description": "Basic number recognition"},
        {"number": "8", "description": "Red-green detection"}, 
        {"number": "6", "description": "Color contrast"},
        {"number": "29", "description": "Two-digit number"},
        {"number": "5", "description": "Low contrast"},
        {"number": "3", "description": "Pattern recognition"}
    ]
    
    current_plate = len(st.session_state.ishihara_answers)
    
    if current_plate < len(plates):
        st.write(f"**Plate {current_plate + 1} of {len(plates)}** - {plates[current_plate]['description']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create Ishihara plate
            fig, ax = plt.subplots(figsize=(5, 5))
            
            # Background dots
            for i in range(300):
                x, y = random.uniform(0, 10), random.uniform(0, 10)
                color = random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
                size = random.randint(20, 50)
                ax.scatter(x, y, c=color, s=size, alpha=0.7)
            
            # Number pattern
            if plates[current_plate]["number"] == "12":
                ax.scatter([3,4,6,7], [7,7,7,7], c='#2C3E50', s=80, alpha=0.9)
                ax.scatter([3,4,6,7], [6,6,6,6], c='#2C3E50', s=80, alpha=0.9)
            elif plates[current_plate]["number"] == "8":
                ax.scatter([4,5,6,4,6,4,5,6], [7,7,7,6,6,5,5,5], c='#2C3E50', s=80, alpha=0.9)
            elif plates[current_plate]["number"] == "6":
                ax.scatter([4,5,4,4,5,6], [7,7,6,5,5,5], c='#2C3E50', s=80, alpha=0.9)
            elif plates[current_plate]["number"] == "29":
                ax.scatter([2,3,5,6,7], [7,7,7,7,7], c='#2C3E50', s=80, alpha=0.9)
                ax.scatter([2,3,5,6,7], [6,6,6,6,6], c='#2C3E50', s=80, alpha=0.9)
            elif plates[current_plate]["number"] == "5":
                ax.scatter([4,5,6,4,4,5,6], [7,7,7,6,5,5,5], c='#2C3E50', s=80, alpha=0.9)
            elif plates[current_plate]["number"] == "3":
                ax.scatter([4,5,6,5,4,5,6], [7,7,7,6,5,5,5], c='#2C3E50', s=80, alpha=0.9)
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            answer = st.text_input("What number do you see?", key=f"input_{current_plate}")
            
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if answer:
                    st.session_state.ishihara_answers.append(answer)
                    st.rerun()
                else:
                    st.warning("Please enter an answer")
    
    else:
        # Test completed
        st.success("🎉 Ishihara Test Completed!")
        
        # Calculate score
        correct = 0
        for i, (plate, answer) in enumerate(zip(plates, st.session_state.ishihara_answers)):
            if answer == plate["number"]:
                correct += 1
        
        score = (correct / len(plates)) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", f"{score:.1f}%")
        with col2:
            st.metric("Correct Answers", f"{correct}/{len(plates)}")
        
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct,
            'total': len(plates)
        }
        
        if st.button("Continue to Next Test", type="primary", use_container_width=True):
            st.session_state.page = "farnsworth"
            st.rerun()

# Farnsworth Test
elif page == "🌈 Farnsworth Test":
    st.title("🌈 Farnsworth Color Arrangement Test")
    st.write("**Instructions:** Answer questions about color sequences and relationships.")
    
    questions = [
        {
            "question": "Which color comes between RED and YELLOW?",
            "options": ["Orange", "Green", "Blue", "Purple"],
            "correct": "Orange"
        },
        {
            "question": "What is the correct order from GREEN to BLUE?",
            "options": ["Green → Blue", "Green → Yellow → Blue", "Green → Red → Blue", "Green → Purple → Blue"],
            "correct": "Green → Blue"
        }
    ]

    answers = []
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}:** {q['question']}")
        answer = st.radio(f"Select answer:", q['options'], key=f"farnsworth_{i}")
        answers.append(answer)
    
    if st.button("Submit Farnsworth Test", type="primary", use_container_width=True):
        score = 0
        for i, (q, ans) in enumerate(zip(questions, answers)):
            if ans == q['correct']:
                score += 1
        
        total_score = (score / len(questions)) * 100
        
        st.session_state.test_results['farnsworth'] = {
            'score': total_score,
            'correct': score,
            'total': len(questions)
        }
        
        st.success(f"Farnsworth Test Completed! Score: {total_score:.1f}%")
        
        if st.button("Continue to Lantern Test", use_container_width=True):
            st.session_state.page = "lantern"
            st.rerun()

# Lantern Test
elif page == "💡 Lantern Test":
    st.title("💡 Navigation Lights Test")
    st.write("**Instructions:** Identify navigation light combinations for different vessels.")
    
    scenarios = [
        {
            "scenario": "Vessel approaching from starboard side",
            "lights": "🟢 Green + ⚪ White",
            "correct": "Green and White",
            "options": ["Red and White", "Green and White", "Red and Green", "White only"]
        },
        {
            "scenario": "Vessel constrained by draft", 
            "lights": "🔴 Red + 🔴 Red + 🔴 Red",
            "correct": "Three Red lights",
            "options": ["Three Red lights", "Two Red lights", "Red-White-Red", "Green-Red-Green"]
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.write(f"**Scenario {i+1}:** {scenario['scenario']}")
        st.write(f"Lights: {scenario['lights']}")
        answer = st.selectbox(f"Select identification:", scenario['options'], key=f"lantern_{i}")
        answers.append(answer)
    
    if st.button("Submit Lantern Test", type="primary", use_container_width=True):
        score = 0
        for i, (scenario, ans) in enumerate(zip(scenarios, answers)):
            if ans == scenario['correct']:
                score += 1
        
        total_score = (score / len(scenarios)) * 100
        
        st.session_state.test_results['lantern'] = {
            'score': total_score,
            'correct': score, 
            'total': len(scenarios)
        }
        
        st.success(f"Lantern Test Completed! Score: {total_score:.1f}%")
        
        if st.button("View Results", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

# Results Page
elif page == "📊 Results":
    st.title("📊 Test Results")
    
    if not st.session_state.test_results:
        st.warning("Complete tests to see results")
    else:
        # Display results
        results_data = []
        for test_name, results in st.session_state.test_results.items():
            results_data.append({
                'Test': test_name.title(),
                'Score': f"{results['score']:.1f}%",
                'Correct': f"{results['correct']}/{results['total']}",
                'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review'
            })

        st.dataframe(pd.DataFrame(results_data))

        # Overall score
        total_score = sum(result['score'] for result in st.session_state.test_results.values())
        avg_score = total_score / len(st.session_state.test_results)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{avg_score:.1f}%")
        with col2:
            st.metric("Tests Completed", len(st.session_state.test_results))
        with col3:
            if avg_score >= 85:
                st.success("FIT FOR DUTY")
            elif avg_score >= 70:
                st.warning("CONDITIONAL")
            else:
                st.error("REVIEW REQUIRED")

        # Certificate
        st.markdown("---")
        st.subheader("🎓 Assessment Certificate")
        
        st.markdown(f"""
        <div style='border: 2px solid #1E3A8A; padding: 2rem; border-radius: 10px; background: #f8f9fa;'>
            <h3 style='color: #1E3A8A; text-align: center;'>VisionQuest Navigator</h3>
            <h4 style='text-align: center;'>Maritime Vision Assessment</h4>
            <hr>
            <p><strong>Mariner:</strong> {name if name else "Not provided"}</p>
            <p><strong>Rank:</strong> {rank}</p>
            <p><strong>Overall Score:</strong> {avg_score:.1f}%</p>
            <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)