import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import time
from PIL import Image, ImageDraw
import io

# Page configuration
st.set_page_config(
    page_title="VisionQuest Navigator",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for maritime styling
st.markdown("""
<style>
    .main-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #60A5FA 100%);
        min-height: 100vh;
    }
    .banner-container {
        width: 100%;
        margin-bottom: 2rem;
    }
    .banner-image {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .section-header {
        font-size: 2rem;
        color: #1E40AF;
        border-bottom: 3px solid #1E3A8A;
        padding-bottom: 0.5rem;
        margin-top: 1rem;
        font-weight: bold;
    }
    .test-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 6px solid #1E3A8A;
        border-right: 2px solid #1E3A8A;
    }
    .warning-box {
        background-color: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .navy-button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 10px 5px;
        transition: all 0.3s ease;
    }
    .navy-button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    .compass-rose {
        text-align: center;
        font-size: 3rem;
        margin: 1rem 0;
    }
    .test-progress {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .maritime-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 2px solid #E5E7EB;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}
if 'current_test' not in st.session_state:
    st.session_state.current_test = "Home"
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'current_plate' not in st.session_state:
    st.session_state.current_plate = 0
if 'ishihara_answers' not in st.session_state:
    st.session_state.ishihara_answers = []
if 'farnsworth_answers' not in st.session_state:
    st.session_state.farnsworth_answers = []
if 'lantern_answers' not in st.session_state:
    st.session_state.lantern_answers = []

def main():
    # Header with Banner
    st.markdown("""
    <div class="banner-container">
        <img src="https://i.postimg.cc/sxD1zsLs/Gemini-Generated-Image-jegd9ajegd9ajegd.png" class="banner-image">
    </div>
    """, unsafe_allow_html=True)
    
    # User information
    with st.sidebar:
        st.markdown("### 🧭 Mariner Information")
        st.session_state.user_data['name'] = st.text_input("**Full Name**")
        st.session_state.user_data['rank'] = st.selectbox("**Rank/Position**", 
            ["Captain", "Chief Officer", "Second Officer", "Third Officer", "Deck Cadet", "Other"])
        st.session_state.user_data['company'] = st.text_input("**Shipping Company**")
        
        st.markdown("---")
        st.markdown("### 🧪 Test Progress")
        
        # Show test completion status
        completed_tests = len(st.session_state.test_results)
        total_tests = 6
        progress = completed_tests / total_tests if total_tests > 0 else 0
        
        st.markdown(f"**Completed:** {completed_tests}/{total_tests} tests")
        st.markdown(f"**Progress:** {progress:.0%}")
        st.markdown(f'<div class="test-progress" style="width: {progress * 100}%"></div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    
    test_options = [
        "🏠 Home",
        "🎯 Ishihara Test", 
        "🌈 Farnsworth D-15 Test",
        "💡 Lantern Test",
        "🗺️ ECDIS Simulation",
        "📡 Radar Simulation", 
        "🚢 Visual Navigation",
        "📊 Results & Certificate"
    ]
    
    selected_test = st.sidebar.selectbox("**Select Test:**", test_options)
    
    # Map selection to test functions
    test_mapping = {
        "🏠 Home": show_home,
        "🎯 Ishihara Test": ishihara_test,
        "🌈 Farnsworth D-15 Test": farnsworth_test,
        "💡 Lantern Test": lantern_test,
        "🗺️ ECDIS Simulation": ecd_simulation,
        "📡 Radar Simulation": radar_simulation,
        "🚢 Visual Navigation": visual_navigation_test,
        "📊 Results & Certificate": show_results
    }
    
    # Execute selected test
    test_function = test_mapping.get(selected_test, show_home)
    test_function()

def show_home():
    st.markdown("""
    <div class="maritime-card">
        <div class="compass-rose">🧭</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Welcome to VisionQuest Navigator</h2>
        <p style='text-align: center; font-size: 1.2rem; color: #4B5563;'>
        Comprehensive Maritime Vision Testing Suite
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="test-container">
            <h3>🚢 Why This Testing Matters</h3>
            <p>Traditional Ishihara tests alone are insufficient for maritime professionals. 
            Modern navigation requires accurate color perception in various conditions:</p>
            
            <ul>
            <li><strong>ECDIS displays</strong> with specialized color palettes</li>
            <li><strong>Navigation lights</strong> recognition at distance</li>
            <li><strong>Radar displays</strong> with color-coded targets</li>
            <li><strong>Buoy identification</strong> in different lighting conditions</li>
            </ul>
            
            <p>This comprehensive testing suite evaluates your visual capabilities specifically 
            for maritime navigation requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="test-container">
            <h3>📋 Testing Protocol</h3>
            <ol>
            <li><strong>Complete all tests</strong> in sequence</li>
            <li><strong>Ensure proper lighting</strong> - avoid glare and reflections</li>
            <li><strong>Maintain normal viewing distance</strong> from screen (50-70cm)</li>
            <li><strong>Do not adjust screen colors</strong> during testing</li>
            <li><strong>Record your results</strong> for medical review</li>
            </ol>
            <p><strong>Estimated completion time:</strong> 20-30 minutes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="test-container">
            <h3>⚓ Maritime Safety</h3>
            <p>Proper color vision is critical for:</p>
            <ul>
            <li>Collision avoidance</li>
            <li>Safe navigation in restricted waters</li>
            <li>Emergency response procedures</li>
            <li>Port operations and pilotage</li>
            <li>Night navigation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="test-container">
            <h3>🖥️ Required Equipment</h3>
            <ul>
            <li>Computer with color display</li>
            <li>Standard web browser</li>
            <li>Controlled lighting environment</li>
            <li>Standard viewing distance</li>
            <li>Stable internet connection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Warning about display calibration
    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Important Note:</strong> Test results depend on your display calibration. 
    For most accurate results, use a calibrated monitor in controlled lighting conditions.
    Results should be verified by qualified medical personnel.
    </div>
    """, unsafe_allow_html=True)
    
    # Start testing button - FIXED
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚢 BEGIN MARITIME TESTING", type="primary", use_container_width=True, key="start_testing"):
            st.session_state.test_started = True
            st.session_state.current_test = "Ishihara Test"
            st.session_state.current_plate = 0
            st.session_state.ishihara_answers = []
            st.session_state.farnsworth_answers = []
            st.session_state.lantern_answers = []
            st.rerun()

def ishihara_test():
    st.markdown('<div class="section-header">🎯 Ishihara Color Vision Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Identify the numbers you see in each circle. Type the number in the text box below each plate.</p>
        <p>If you cannot see a number, type <strong>0</strong>.</p>
        <p><strong>Plate {}/8</strong></p>
    </div>
    """.format(st.session_state.current_plate + 1), unsafe_allow_html=True)
    
    # Ishihara plates data
    plates = [
        {"answer": "12", "description": "Red-green deficiency detection"},
        {"answer": "8", "description": "Basic number recognition"},
        {"answer": "6", "description": "Color contrast sensitivity"},
        {"answer": "29", "description": "Two-digit number recognition"},
        {"answer": "5", "description": "Single digit with background noise"},
        {"answer": "3", "description": "Low contrast number identification"},
        {"answer": "15", "description": "Traffic light colors simulation"},
        {"answer": "74", "description": "Complex pattern recognition"}
    ]
    
    current_plate = st.session_state.current_plate
    
    if current_plate < len(plates):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Create Ishihara-like plate
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_aspect('equal')
            
            # Background dots
            for _ in range(300):
                x, y = random.uniform(0.5, 9.5), random.uniform(0.5, 9.5)
                color = random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
                size = random.randint(20, 60)
                ax.scatter(x, y, c=color, s=size, alpha=0.8)
            
            # "Number" made of contrasting dots
            number_centers = []
            if current_plate == 0:  # Number 12
                number_centers = [(3, 7), (4, 7), (6, 7), (7, 7)]
            elif current_plate == 1:  # Number 8
                number_centers = [(4, 6), (5, 7), (5, 6), (5, 5), (6, 6)]
            elif current_plate == 2:  # Number 6
                number_centers = [(4, 5), (5, 6), (5, 5), (5, 4), (6, 5)]
            elif current_plate == 3:  # Number 29
                number_centers = [(2, 7), (3, 7), (5, 7), (6, 7), (7, 7)]
            elif current_plate == 4:  # Number 5
                number_centers = [(4, 7), (5, 7), (6, 7), (4, 6), (4, 5)]
            elif current_plate == 5:  # Number 3
                number_centers = [(4, 7), (5, 7), (6, 7), (5, 6), (4, 5)]
            elif current_plate == 6:  # Number 15
                number_centers = [(2, 7), (3, 7), (5, 7), (6, 7)]
            elif current_plate == 7:  # Number 74
                number_centers = [(2, 7), (3, 7), (5, 7), (6, 7), (7, 7)]
            
            for x, y in number_centers:
                ax.scatter(x, y, c='#2C3E50', s=80, alpha=0.9, edgecolors='white', linewidth=1)
            
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
            plt.close()
            
        with col2:
            st.markdown(f"**Plate Description:** {plates[current_plate]['description']}")
            
            answer = st.text_input(
                f"**What number do you see?**",
                key=f"ishihara_input_{current_plate}",
                placeholder="Enter the number you see (0 if no number visible)"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏭️ Next Plate", use_container_width=True, key=f"next_plate_{current_plate}"):
                    if answer:
                        st.session_state.ishihara_answers.append(answer.strip())
                        st.session_state.current_plate += 1
                        st.rerun()
                    else:
                        st.warning("Please enter your answer before proceeding.")
            
            with col2:
                if st.button("🔄 Restart Test", use_container_width=True, key=f"restart_ishihara"):
                    st.session_state.current_plate = 0
                    st.session_state.ishihara_answers = []
                    st.rerun()
    
    else:
        # All plates completed - show results
        st.markdown("""
        <div class="test-container">
            <h3>🎯 Ishihara Test Complete!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        correct = 0
        results_details = []
        
        for i, (plate, answer) in enumerate(zip(plates, st.session_state.ishihara_answers)):
            is_correct = answer == plate['answer']
            if is_correct:
                correct += 1
            results_details.append({
                'plate': i + 1,
                'expected': plate['answer'],
                'answered': answer,
                'correct': is_correct
            })
        
        score = (correct / len(plates)) * 100
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("**Score**", f"{score:.1f}%")
            st.metric("**Correct Answers**", f"{correct}/{len(plates)}")
        
        with col2:
            if score >= 85:
                st.success("✅ **Excellent** - Color vision suitable for maritime duties")
            elif score >= 70:
                st.warning("⚠️ **Satisfactory** - Minor issues detected")
            else:
                st.error("❌ **Needs Review** - Comprehensive evaluation recommended")
        
        # Save results
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct,
            'total': len(plates),
            'details': results_details
        }
        
        if st.button("➡️ Continue to Next Test", type="primary", use_container_width=True, key="continue_from_ishihara"):
            st.session_state.current_test = "Farnsworth D-15 Test"
            st.rerun()

def farnsworth_test():
    st.markdown('<div class="section-header">🌈 Farnsworth D-15 Color Arrangement Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Arrange the colors in correct order from one color to the next, creating a smooth color transition.</p>
        <p>Select the correct answers for the color sequence questions below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Test questions
    st.markdown("### Color Sequence Questions")
    
    questions = [
        {
            "question": "Which color comes between 🔴 Red and 🟡 Yellow in the spectrum?",
            "options": ["🟠 Orange", "🟢 Green", "🔵 Blue", "🟣 Purple"],
            "correct": "🟠 Orange"
        },
        {
            "question": "What is the correct order from 🟢 Green to 🔵 Blue?",
            "options": ["Green → Yellow → Blue", "Green → Blue", "Green → Red → Blue", "Green → Purple → Blue"],
            "correct": "Green → Blue"
        },
        {
            "question": "Which color is missing in this sequence: Red → Orange → ? → Green",
            "options": ["Yellow", "Blue", "Purple", "Pink"],
            "correct": "Yellow"
        }
    ]
    
    farnsworth_answers = []
    
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}:** {q['question']}")
        answer = st.radio(f"Select your answer:", q['options'], key=f"farnsworth_q{i}")
        farnsworth_answers.append(answer)
    
    if st.button("Submit Farnsworth Test", type="primary", use_container_width=True, key="submit_farnsworth"):
        farnsworth_score = 0
        for i, (q, answer) in enumerate(zip(questions, farnsworth_answers)):
            if answer == q['correct']:
                farnsworth_score += 1
        
        score = (farnsworth_score / len(questions)) * 100
        st.session_state.test_results['farnsworth'] = {
            'score': score,
            'correct': farnsworth_score,
            'total': len(questions),
            'details': farnsworth_answers
        }
        
        st.success(f"🌈 Farnsworth Test Completed: {farnsworth_score}/{len(questions)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to Lantern Test", use_container_width=True, key="continue_to_lantern"):
            st.session_state.current_test = "Lantern Test"
            st.rerun()

def lantern_test():
    st.markdown('<div class="section-header">💡 Navigation Lights Recognition Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Identify the colors of navigation lights as they would appear at sea.</p>
        <p>Select the correct light combination for each scenario.</p>
    </div>
    """)
    
    light_scenarios = [
        {
            "scenario": "Vessel approaching from starboard side at night",
            "lights": ["🟢", "⚪"],
            "correct": "Green and White",
            "options": ["Red and White", "Green and White", "Red and Green", "White only"]
        },
        {
            "scenario": "Vessel constrained by draft",
            "lights": ["🔴", "🔴", "🔴"],
            "correct": "Three Red lights",
            "options": ["Three Red lights", "Two Red lights", "Red-White-Red", "Green-Red-Green"]
        },
        {
            "scenario": "Fishing vessel engaged in trawling",
            "lights": ["🟢", "⚪"],
            "correct": "Green over White",
            "options": ["Red over White", "Green over White", "White over Red", "White over Green"]
        }
    ]
    
    lantern_answers = []
    
    for i, scenario in enumerate(light_scenarios):
        st.markdown(f"**Scenario {i+1}: {scenario['scenario']}**")
        
        # Display lights
        light_display = " + ".join(scenario['lights'])
        st.markdown(f"<h3 style='text-align: center;'>{light_display}</h3>", unsafe_allow_html=True)
        
        answer = st.selectbox(
            f"What lights do you see?",
            scenario['options'],
            key=f"lantern_{i}"
        )
        lantern_answers.append(answer)
    
    if st.button("Submit Lantern Test", type="primary", use_container_width=True, key="submit_lantern"):
        lantern_score = 0
        for i, (scenario, answer) in enumerate(zip(light_scenarios, lantern_answers)):
            if answer == scenario['correct']:
                lantern_score += 1
        
        score = (lantern_score / len(light_scenarios)) * 100
        st.session_state.test_results['lantern'] = {
            'score': score,
            'correct': lantern_score,
            'total': len(light_scenarios),
            'details': lantern_answers
        }
        
        st.success(f"💡 Lantern Test Completed: {lantern_score}/{len(light_scenarios)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to ECDIS Test", use_container_width=True, key="continue_to_ecdis"):
            st.session_state.current_test = "ECDIS Simulation"
            st.rerun()

def ecd_simulation():
    st.markdown('<div class="section-header">🗺️ ECDIS Color Recognition Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Identify the correct meaning of colors used in ECDIS displays for different navigation conditions.</p>
    </div>
    """)
    
    ecd_scenarios = [
        {
            "question": "What does DARK BLUE typically represent on ECDIS?",
            "options": ["Deep water (>100m)", "Shallow water (<10m)", "Restricted area", "Traffic separation scheme"],
            "correct": "Deep water (>100m)"
        },
        {
            "question": "What color indicates DANGEROUS AREAS on ECDIS?",
            "options": ["Red", "Yellow", "Green", "Blue"],
            "correct": "Red"
        },
        {
            "question": "Which color is used for SAFETY CONTOURS?",
            "options": ["Magenta", "Green", "Blue", "Yellow"],
            "correct": "Magenta"
        }
    ]
    
    ecd_answers = []
    
    for i, scenario in enumerate(ecd_scenarios):
        answer = st.radio(
            f"**{scenario['question']}**",
            scenario['options'],
            key=f"ecd_{i}"
        )
        ecd_answers.append(answer)
    
    if st.button("Submit ECDIS Test", type="primary", use_container_width=True, key="submit_ecdis"):
        ecd_score = 0
        for i, (scenario, answer) in enumerate(zip(ecd_scenarios, ecd_answers)):
            if answer == scenario['correct']:
                ecd_score += 1
        
        score = (ecd_score / len(ecd_scenarios)) * 100
        st.session_state.test_results['ecdis'] = {
            'score': score,
            'correct': ecd_score,
            'total': len(ecd_scenarios),
            'details': ecd_answers
        }
        
        st.success(f"🗺️ ECDIS Test Completed: {ecd_score}/{len(ecd_scenarios)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to Radar Test", use_container_width=True, key="continue_to_radar"):
            st.session_state.current_test = "Radar Simulation"
            st.rerun()

def radar_simulation():
    st.markdown('<div class="section-header">📡 Radar Display Interpretation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Interpret colors and symbols on radar displays for safe navigation.</p>
    </div>
    """)
    
    radar_scenarios = [
        {
            "question": "What does a RED target typically indicate on radar?",
            "options": ["Closest target", "Dangerous target", "Stationary target", "Lost target"],
            "correct": "Dangerous target"
        },
        {
            "question": "What color usually represents OWN SHIP on radar?",
            "options": ["Green", "Yellow", "White", "Blue"],
            "correct": "Green"
        },
        {
            "question": "What does a FLASHING target indicate?",
            "options": ["New target", "Target on collision course", "Target changing course", "Target lost"],
            "correct": "Target on collision course"
        }
    ]
    
    radar_answers = []
    
    for i, scenario in enumerate(radar_scenarios):
        answer = st.radio(
            f"**{scenario['question']}**",
            scenario['options'],
            key=f"radar_{i}"
        )
        radar_answers.append(answer)
    
    if st.button("Submit Radar Test", type="primary", use_container_width=True, key="submit_radar"):
        radar_score = 0
        for i, (scenario, answer) in enumerate(zip(radar_scenarios, radar_answers)):
            if answer == scenario['correct']:
                radar_score += 1
        
        score = (radar_score / len(radar_scenarios)) * 100
        st.session_state.test_results['radar'] = {
            'score': score,
            'correct': radar_score,
            'total': len(radar_scenarios),
            'details': radar_answers
        }
        
        st.success(f"📡 Radar Test Completed: {radar_score}/{len(radar_scenarios)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to Visual Navigation", use_container_width=True, key="continue_to_visual"):
            st.session_state.current_test = "Visual Navigation"
            st.rerun()

def visual_navigation_test():
    st.markdown('<div class="section-header">🚢 Buoy and Visual Navigation Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Identify buoy colors and navigation marks in different conditions.</p>
    </div>
    """)
    
    visual_scenarios = [
        {
            "question": "What color is a PORT SIDE buoy?",
            "options": ["Red", "Green", "Yellow", "Black"],
            "correct": "Red"
        },
        {
            "question": "What does a RED & WHITE VERTICAL STRIPED buoy indicate?",
            "options": ["Safe water", "Isolated danger", "Special purpose", "Cardinal mark"],
            "correct": "Safe water"
        },
        {
            "question": "What color are SPECIAL MARKS (yellow buoys)?",
            "options": ["Yellow", "Orange", "White", "Blue"],
            "correct": "Yellow"
        }
    ]
    
    visual_answers = []
    
    for i, scenario in enumerate(visual_scenarios):
        answer = st.radio(
            f"**{scenario['question']}**",
            scenario['options'],
            key=f"visual_{i}"
        )
        visual_answers.append(answer)
    
    if st.button("Submit Visual Navigation Test", type="primary", use_container_width=True, key="submit_visual"):
        visual_score = 0
        for i, (scenario, answer) in enumerate(zip(visual_scenarios, visual_answers)):
            if answer == scenario['correct']:
                visual_score += 1
        
        score = (visual_score / len(visual_scenarios)) * 100
        st.session_state.test_results['visual_nav'] = {
            'score': score,
            'correct': visual_score,
            'total': len(visual_scenarios),
            'details': visual_answers
        }
        
        st.success(f"🚢 Visual Navigation Test Completed: {visual_score}/{len(visual_scenarios)} correct ({score:.1f}%)")
        
        if st.button("📊 View All Results", type="primary", use_container_width=True, key="view_results"):
            st.session_state.current_test = "Results & Certificate"
            st.rerun()

def show_results():
    st.markdown('<div class="section-header">📊 Test Results & Certificate</div>', unsafe_allow_html=True)
    
    if not st.session_state.test_results:
        st.warning("No test results available. Please complete at least one test.")
        return
    
    # Calculate overall score
    total_score = 0
    total_tests = len(st.session_state.test_results)
    
    for test_name, results in st.session_state.test_results.items():
        total_score += results['score']
    
    overall_score = total_score / total_tests if total_tests > 0 else 0
    
    # Display comprehensive results
    st.markdown("""
    <div class="test-container">
        <h3>Detailed Test Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
    results_data = []
    for test_name, results in st.session_state.test_results.items():
        results_data.append({
            'Test': test_name.replace('_', ' ').title(),
            'Score': f"{results['score']:.1f}%",
            'Correct': f"{results['correct']}/{results['total']}",
            'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review'
        })
    
    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, use_container_width=True)
    
    # Overall assessment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("**Overall Score**", f"{overall_score:.1f}%")
    
    with col2:
        st.metric("**Tests Completed**", f"{total_tests}/6")
    
    with col3:
        if overall_score >= 85:
            st.success("**FIT FOR DUTY**")
        elif overall_score >= 70:
            st.warning("**CONDITIONAL**")
        else:
            st.error("**REVIEW REQUIRED**")
    
    # Generate certificate
    st.markdown("---")
    st.markdown("### 🎓 Mariner Vision Assessment Certificate")
    
    st.markdown(f"""
    <div style='border: 4px solid #1E3A8A; padding: 2rem; border-radius: 15px; background: white; text-align: center;'>
        <h1 style='color: #1E3A8A;'>⚓ VISIONQUEST NAVIGATOR</h1>
        <h3 style='color: #4B5563;'>Mariner Vision Assessment Certificate</h3>
        <hr>
        <h2>{st.session_state.user_data.get('name', 'Mariner')}</h2>
        <p><strong>Rank:</strong> {st.session_state.user_data.get('rank', 'Not specified')}</p>
        <p><strong>Company:</strong> {st.session_state.user_data.get('company', 'Not specified')}</p>
        <hr>
        <h3 style='color: #1E3A8A;'>Overall Score: {overall_score:.1f}%</h3>
        <p><strong>Tests Completed:</strong> {total_tests}/6</p>
        <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%B %d, %Y')}</p>
        <small>This assessment is for training purposes and should be verified by qualified medical personnel.</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()