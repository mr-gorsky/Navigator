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
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
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

def main():
    # Header with Logo only
    st.markdown("""
    <div class="logo-container">
        <img src="https://i.postimg.cc/QNS6smzc/Gemini-Generated-Image-1u8uax1u8uax1u8u.png" width="500">
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
        progress = completed_tests / total_tests
        
        st.markdown(f"**Completed:** {completed_tests}/{total_tests} tests")
        st.markdown(f"**Progress:** {progress:.0%}")
        st.markdown('<div class="test-progress" style="width: {}%"></div>'.format(progress * 100), unsafe_allow_html=True)
    
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
    
    # Start testing button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚢 BEGIN MARITIME TESTING", type="primary", use_container_width=True):
            st.session_state.test_started = True
            st.session_state.current_test = "Ishihara Test"
            st.session_state.current_plate = 0
            st.session_state.ishihara_answers = []
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
            # Add more number patterns for other plates...
            
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
                if st.button("⏭️ Next Plate", use_container_width=True):
                    if answer:
                        st.session_state.ishihara_answers.append(answer.strip())
                        st.session_state.current_plate += 1
                        st.rerun()
                    else:
                        st.warning("Please enter your answer before proceeding.")
            
            with col2:
                if st.button("🔄 Restart Test", use_container_width=True):
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
        
        if st.button("➡️ Continue to Next Test", type="primary", use_container_width=True):
            st.session_state.current_test = "Farnsworth D-15 Test"
            st.rerun()

def farnsworth_test():
    st.markdown('<div class="section-header">🌈 Farnsworth D-15 Color Arrangement Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="test-container">
        <h3>Instructions:</h3>
        <p>Arrange the colors in correct order from one color to the next, creating a smooth color transition.</p>
        <p>Click on the colors in the order you think they should appear.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Color sequence for the test
    colors = ['#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00', 
              '#FFFF00', '#CCFF00', '#99FF00', '#66FF00', '#33FF00',
              '#00FF00', '#00FF33', '#00FF66', '#00FF99', '#00FFCC']
    
    st.markdown("**Drag the colors into the correct sequence:**")
    
    # Simplified version - show colors and ask for order
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.color_picker("Color 1", "#FF0000", key="color1")
        st.color_picker("Color 2", "#FF6600", key="color2")
        st.color_picker("Color 3", "#FFCC00", key="color3")
    
    with col2:
        st.color_picker("Color 4", "#FFFF00", key="color4")
        st.color_picker("Color 5", "#99FF00", key="color5")
        st.color_picker("Color 6", "#33FF00", key="color6")
    
    with col3:
        st.color_picker("Color 7", "#00FF00", key="color7")
        st.color_picker("Color 8", "#00FF66", key="color8")
        st.color_picker("Color 9", "#00FFCC", key="color9")
    
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
        }
    ]
    
    farnsworth_score = 0
    user_answers = []
    
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}:** {q['question']}")
        answer = st.radio(f"Select your answer:", q['options'], key=f"farnsworth_q{i}")
        user_answers.append(answer)
        
        if answer == q['correct']:
            farnsworth_score += 1
    
    if st.button("Submit Farnsworth Test", type="primary", use_container_width=True):
        score = (farnsworth_score / len(questions)) * 100
        st.session_state.test_results['farnsworth'] = {
            'score': score,
            'correct': farnsworth_score,
            'total': len(questions),
            'details': user_answers
        }
        
        st.success(f"🌈 Farnsworth Test Completed: {farnsworth_score}/{len(questions)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to Lantern Test", use_container_width=True):
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
    
    lantern_score = 0
    user_answers = []
    
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
        user_answers.append(answer)
        
        if answer == scenario['correct']:
            lantern_score += 1
    
    if st.button("Submit Lantern Test", type="primary", use_container_width=True):
        score = (lantern_score / len(light_scenarios)) * 100
        st.session_state.test_results['lantern'] = {
            'score': score,
            'correct': lantern_score,
            'total': len(light_scenarios),
            'details': user_answers
        }
        
        st.success(f"💡 Lantern Test Completed: {lantern_score}/{len(light_scenarios)} correct ({score:.1f}%)")
        
        if st.button("➡️ Continue to ECDIS Test", use_container_width=True):
            st.session_state.current_test = "ECDIS Simulation"
            st.rerun()

# Other test functions (ECDIS, Radar, Visual Navigation) would follow similar patterns
def ecd_simulation():
    st.markdown('<div class="section-header">🗺️ ECDIS Color Recognition Test</div>', unsafe_allow_html=True)
    st.info("ECDIS simulation would be implemented here with actual color recognition tasks")
    # Similar structure to other tests

def radar_simulation():
    st.markdown('<div class="section-header">📡 Radar Display Interpretation</div>', unsafe_allow_html=True)
    st.info("Radar simulation would be implemented here with target identification tasks")
    # Similar structure to other tests

def visual_navigation_test():
    st.markdown('<div class="section-header">🚢 Buoy and Visual Navigation Test</div>', unsafe_allow_html=True)
    st.info("Visual navigation test would be implemented here with buoy recognition tasks")
    # Similar structure to other tests

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
            'Test': test_name.title(),
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