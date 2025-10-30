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
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #1E40AF;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .maritime-theme {
        background-color: #F0F8FF;
    }
    .test-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #1E3A8A;
    }
    .warning-box {
        background-color: #FFFBEB;
        border: 1px solid #F59E0B;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .nav-button {
        background-color: #1E3A8A;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}
if 'current_test' not in st.session_state:
    st.session_state.current_test = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

def main():
    # Header with Logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://i.postimg.cc/QNS6smzc/Gemini-Generated-Image-1u8uax1u8uax1u8u.png" width="400">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">⚓ VisionQuest Navigator</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Vision Testing for Mariners")
    
    # Warning about display calibration
    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Important Note:</strong> Test results depend on your display calibration. 
    For most accurate results, use a calibrated monitor in controlled lighting conditions.
    </div>
    """, unsafe_allow_html=True)
    
    # User information
    with st.sidebar:
        st.title("Mariner Information")
        st.session_state.user_data['name'] = st.text_input("Full Name")
        st.session_state.user_data['rank'] = st.selectbox("Rank/Position", 
            ["Captain", "Chief Officer", "Second Officer", "Third Officer", "Deck Cadet", "Other"])
        st.session_state.user_data['company'] = st.text_input("Shipping Company")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    test_options = [
        "Home",
        "Ishihara Test", 
        "Farnsworth D-15 Test",
        "Lantern Test (Navigation Lights)",
        "ECDIS Simulation",
        "Radar Simulation", 
        "Visual Navigation (Buoys)",
        "Results & Certificate"
    ]
    selected_test = st.sidebar.selectbox("Select Test:", test_options)
    
    # Test pages
    if selected_test == "Home":
        show_home()
    elif selected_test == "Ishihara Test":
        ishihara_test()
    elif selected_test == "Farnsworth D-15 Test":
        farnsworth_test()
    elif selected_test == "Lantern Test (Navigation Lights)":
        lantern_test()
    elif selected_test == "ECDIS Simulation":
        ecd_simulation()
    elif selected_test == "Radar Simulation":
        radar_simulation()
    elif selected_test == "Visual Navigation (Buoys)":
        visual_navigation_test()
    elif selected_test == "Results & Certificate":
        show_results()

def show_home():
    st.markdown('<div class="section-header">Welcome to VisionQuest Navigator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Why This Testing Matters
        
        Traditional Ishihara tests alone are insufficient for maritime professionals. 
        Modern navigation requires accurate color perception in various conditions:
        
        - **ECDIS displays** with specialized color palettes
        - **Navigation lights** recognition at distance
        - **Radar displays** with color-coded targets
        - **Buoy identification** in different lighting
        
        This comprehensive testing suite evaluates your visual capabilities specifically 
        for maritime navigation requirements.
        """)
        
        st.markdown("""
        ### Testing Protocol
        
        1. **Complete all tests** in sequence
        2. **Ensure proper lighting** - avoid glare and reflections
        3. **Maintain normal viewing distance** from screen
        4. **Do not adjust screen colors** during testing
        5. **Record your results** for medical review
        
        Estimated completion time: 20-30 minutes
        """)
    
    with col2:
        # Maritime-themed information
        st.markdown("""
        ### Maritime Navigation Safety
        
        Proper color vision is critical for:
        - Collision avoidance
        - Safe navigation in restricted waters
        - Emergency response
        - Port operations
        """)
        
        st.markdown("""
        ### Required Equipment
        - Computer with color display
        - Standard web browser
        - Controlled lighting environment
        - Standard viewing distance (50-70cm)
        """)
    
    # Start testing button
    if st.button("🚢 Begin Testing", type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.session_state.current_test = "Ishihara Test"
        st.rerun()

def ishihara_test():
    st.markdown('<div class="section-header">Ishihara Color Vision Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Identify the numbers you see in each circle. If you cannot see a number, type '0'.
    """)
    
    # Simplified Ishihara plates (simulated)
    plates = [
        {"image": "12", "answer": "12", "description": "Red-green deficiency test"},
        {"image": "8", "answer": "8", "description": "Basic number recognition"},
        {"image": "6", "answer": "6", "description": "Color contrast sensitivity"},
        {"image": "29", "answer": "29", "description": "Two-digit number recognition"},
        {"image": "5", "answer": "5", "description": "Single digit with background noise"},
        {"image": "3", "answer": "3", "description": "Low contrast number"},
        {"image": "15", "answer": "15", "description": "Traffic light colors simulation"},
        {"image": "74", "answer": "74", "description": "Complex pattern recognition"}
    ]
    
    user_answers = []
    
    for i, plate in enumerate(plates):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Create a simple circle with colored dots (simulated Ishihara plate)
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_aspect('equal')
            
            # Create dot pattern (simplified)
            for _ in range(200):
                x, y = random.uniform(1, 9), random.uniform(1, 9)
                color = random.choice(['red', 'green', 'orange', 'brown'])
                ax.scatter(x, y, c=color, s=30, alpha=0.7)
            
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
            plt.close()
            
        with col2:
            st.write(f"**Plate {i+1}**: {plate['description']}")
            answer = st.text_input(f"What number do you see? (Plate {i+1})", key=f"ishihara_{i}")
            user_answers.append(answer)
    
    if st.button("Submit Ishihara Test", type="primary"):
        correct = 0
        for i, (plate, answer) in enumerate(zip(plates, user_answers)):
            if answer.strip() == plate['answer']:
                correct += 1
        
        score = (correct / len(plates)) * 100
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct,
            'total': len(plates),
            'details': list(zip([p['answer'] for p in plates], user_answers))
        }
        
        st.success(f"Ishihara Test Completed: {correct}/{len(plates)} correct ({score:.1f}%)")
        
        if score >= 85:
            st.balloons()
            st.success("✅ Color vision within normal parameters for basic recognition")

def farnsworth_test():
    st.markdown('<div class="section-header">Farnsworth D-15 Color Arrangement Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Arrange the colors in correct order from one color to the next, 
    creating a smooth color transition.
    """)
    
    st.info("Drag and drop functionality would be implemented here in a full application")
    
    # Simplified version - multiple choice
    st.subheader("Color Order Recognition")
    
    questions = [
        {
            "question": "Which color comes between these two colors?",
            "colors": ["🔴", "🟡"],
            "options": ["🟠", "🟢", "🔵", "🟣"],
            "correct": 0
        },
        {
            "question": "Identify the correct color sequence:",
            "colors": ["🟢", "🔵"],
            "options": ["🟢→🟡→🔵", "🟢→🟠→🔵", "🟢→🔵", "🟢→🟣→🔵"],
            "correct": 2
        }
    ]
    
    farnsworth_score = 0
    
    for i, q in enumerate(questions):
        st.write(f"**Question {i+1}:** {q['question']}")
        st.write(f"Colors: {q['colors'][0]} → ? → {q['colors'][1]}")
        
        selected = st.radio(f"Select answer:", q['options'], key=f"farnsworth_{i}")
        
        if selected == q['options'][q['correct']]:
            farnsworth_score += 1
    
    if st.button("Submit Farnsworth Test", type="primary"):
        score = (farnsworth_score / len(questions)) * 100
        st.session_state.test_results['farnsworth'] = {
            'score': score,
            'correct': farnsworth_score,
            'total': len(questions)
        }
        
        st.success(f"Farnsworth Test Completed: {farnsworth_score}/{len(questions)} correct ({score:.1f}%)")

def lantern_test():
    st.markdown('<div class="section-header">Navigation Lights Recognition Test</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Identify the colors of navigation lights as they would appear at sea.
    Respond quickly as you would in real navigation situations.
    """)
    
    # Navigation light colors and patterns
    light_combinations = [
        {"colors": ["🔴", "🟢"], "description": "Port and Starboard", "answer": "Red-Green"},
        {"colors": ["⚪", "⚪", "⚪"], "description": "Masthead lights", "answer": "White-White-White"},
        {"colors": ["🔴", "⚪"], "description": "Vessel constrained by draft", "answer": "Red-White"},
        {"colors": ["🟢", "⚪"], "description": "Towing lights", "answer": "Green-White"},
        {"colors": ["🔴", "🔴"], "description": "Vessel not under command", "answer": "Red-Red"}
    ]
    
    lantern_score = 0
    user_responses = []
    
    for i, lights in enumerate(light_combinations):
        st.write(f"**Lights {i+1}:** {lights['description']}")
        
        # Display lights
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            light_display = " ".join(lights['colors'])
            st.markdown(f"<h2 style='text-align: center;'>{light_display}</h2>", unsafe_allow_html=True)
        
        answer = st.selectbox(
            f"What lights do you see? (Set {i+1})",
            ["Red-Green", "White-White-White", "Red-White", "Green-White", "Red-Red", "Cannot determine"],
            key=f"lantern_{i}"
        )
        
        user_responses.append(answer)
        
        if answer == lights['answer']:
            lantern_score += 1
    
    if st.button("Submit Lantern Test", type="primary"):
        score = (lantern_score / len(light_combinations)) * 100
        st.session_state.test_results['lantern'] = {
            'score': score,
            'correct': lantern_score,
            'total': len(light_combinations),
            'details': list(zip([l['answer'] for l in light_combinations], user_responses))
        }
        
        st.success(f"Lantern Test Completed: {lantern_score}/{len(light_combinations)} correct ({score:.1f}%)")

def ecd_simulation():
    st.markdown('<div class="section-header">ECDIS Color Recognition Simulation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Identify colors and symbols as they appear on ECDIS displays 
    in different lighting conditions (Day/Dusk/Night modes).
    """)
    
    # ECDIS color scenarios
    ecd_scenarios = [
        {
            "mode": "🌞 Day Mode",
            "question": "What does this BLUE area represent?",
            "options": ["Deep water (>50m)", "Shallow water (<10m)", "Restricted area", "Traffic separation"],
            "correct": 0,
            "color": "#1E90FF"
        },
        {
            "mode": "🌆 Dusk Mode", 
            "question": "What does this ORANGE symbol indicate?",
            "options": ["Navigation buoy", "Danger area", "Recommended route", "Anchorage area"],
            "correct": 1,
            "color": "#FF8C00"
        },
        {
            "mode": "🌙 Night Mode",
            "question": "What does this GREEN line represent?",
            "options": ["Depth contour", "Safety contour", "Route planning", "Track line"],
            "correct": 1,
            "color": "#32CD32"
        }
    ]
    
    ecd_score = 0
    user_responses = []
    
    for i, scenario in enumerate(ecd_scenarios):
        st.markdown(f"**{scenario['mode']}**")
        
        # Create color patch
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"""
            <div style='background-color: {scenario['color']}; 
                        width: 100px; 
                        height: 100px; 
                        border-radius: 10px;
                        border: 2px solid #333;
                        margin: 10px;'>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(scenario['question'])
            answer = st.radio(
                "Select your answer:",
                scenario['options'],
                key=f"ecd_{i}"
            )
            
            user_responses.append(answer)
            
            if answer == scenario['options'][scenario['correct']]:
                ecd_score += 1
    
    if st.button("Submit ECDIS Test", type="primary"):
        score = (ecd_score / len(ecd_scenarios)) * 100
        st.session_state.test_results['ecdis'] = {
            'score': score,
            'correct': ecd_score,
            'total': len(ecd_scenarios),
            'details': list(zip([s['options'][s['correct']] for s in ecd_scenarios], user_responses))
        }
        
        st.success(f"ECDIS Test Completed: {ecd_score}/{len(ecd_scenarios)} correct ({score:.1f}%)")

def radar_simulation():
    st.markdown('<div class="section-header">Radar Display Interpretation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Interpret colors and symbols on radar displays. 
    Identify targets, tracks, and warning indicators.
    """)
    
    # Radar scenarios
    radar_scenarios = [
        {
            "description": "Target identification",
            "question": "What does a RED target typically indicate?",
            "options": ["Closest target", "Dangerous target", "Stationary target", "Lost target"],
            "correct": 1
        },
        {
            "description": "Track interpretation", 
            "question": "What does a YELLOW track line represent?",
            "options": ["Own ship track", "Target history", "Predicted path", "Danger area"],
            "correct": 2
        },
        {
            "description": "Warning symbols",
            "question": "What action should you take for a FLASHING target?",
            "options": ["Ignore it", "Monitor closely", "Immediate action", "Change scale"],
            "correct": 2
        }
    ]
    
    radar_score = 0
    
    for i, scenario in enumerate(radar_scenarios):
        st.write(f"**Scenario {i+1}:** {scenario['description']}")
        st.write(scenario['question'])
        
        answer = st.radio(
            "Select your answer:",
            scenario['options'],
            key=f"radar_{i}"
        )
        
        if answer == scenario['options'][scenario['correct']]:
            radar_score += 1
    
    if st.button("Submit Radar Test", type="primary"):
        score = (radar_score / len(radar_scenarios)) * 100
        st.session_state.test_results['radar'] = {
            'score': score,
            'correct': radar_score,
            'total': len(radar_scenarios)
        }
        
        st.success(f"Radar Test Completed: {radar_score}/{len(radar_scenarios)} correct ({score:.1f}%)")

def visual_navigation_test():
    st.markdown('<div class="section-header">Buoy and Visual Navigation Recognition</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Instructions:** Identify buoy colors and shapes under different lighting conditions.
    """)
    
    # Buoy recognition scenarios
    buoy_scenarios = [
        {
            "conditions": "🌅 Sunrise conditions",
            "question": "What type of buoy has RED and GREEN horizontal bands?",
            "options": ["Safe water mark", "Isolated danger", "Cardinal mark", "Special mark"],
            "correct": 1
        },
        {
            "conditions": "🌃 Night conditions",
            "question": "What does a QUICK FLASHING WHITE light indicate?",
            "options": ["North cardinal", "West cardinal", "Safe water", "Special purpose"],
            "correct": 0
        },
        {
            "conditions": "🌫️ Foggy conditions", 
            "question": "How would you identify a PORT HAND buoy in reduced visibility?",
            "options": ["Red color, can shape", "Green color, cone shape", "Red and white stripes", "Yellow special mark"],
            "correct": 0
        }
    ]
    
    buoy_score = 0
    
    for i, scenario in enumerate(buoy_scenarios):
        st.write(f"**Conditions:** {scenario['conditions']}")
        st.write(scenario['question'])
        
        answer = st.radio(
            "Select your answer:",
            scenario['options'],
            key=f"buoy_{i}"
        )
        
        if answer == scenario['options'][scenario['correct']]:
            buoy_score += 1
    
    if st.button("Submit Visual Navigation Test", type="primary"):
        score = (buoy_score / len(buoy_scenarios)) * 100
        st.session_state.test_results['visual_nav'] = {
            'score': score,
            'correct': buoy_score,
            'total': len(buoy_scenarios)
        }
        
        st.success(f"Visual Navigation Test Completed: {buoy_score}/{len(buoy_scenarios)} correct ({score:.1f}%)")

def show_results():
    st.markdown('<div class="section-header">Test Results & Certificate</div>', unsafe_allow_html=True)
    
    if not st.session_state.test_results:
        st.warning("No test results available. Please complete at least one test.")
        return
    
    # Calculate overall score
    total_score = 0
    total_tests = 0
    completed_tests = []
    
    for test_name, results in st.session_state.test_results.items():
        total_score += results['score']
        total_tests += 1
        completed_tests.append(test_name)
    
    overall_score = total_score / total_tests if total_tests > 0 else 0
    
    # Display results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Detailed Results")
        
        results_data = []
        for test_name, results in st.session_state.test_results.items():
            results_data.append({
                'Test': test_name.replace('_', ' ').title(),
                'Score': f"{results['score']:.1f}%",
                'Correct': f"{results['correct']}/{results['total']}",
                'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review Needed'
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True)
    
    with col2:
        st.subheader("Overall Assessment")
        
        st.metric("Overall Score", f"{overall_score:.1f}%")
        st.metric("Tests Completed", f"{total_tests}/7")
        
        if overall_score >= 85:
            st.success("🎉 Excellent - Vision suitable for maritime navigation")
            assessment = "FIT FOR DUTY"
            color = "green"
        elif overall_score >= 70:
            st.warning("⚠️ Satisfactory - Some areas need attention")
            assessment = "CONDITIONALLY FIT"
            color = "orange"
        else:
            st.error("❌ Needs Improvement - Comprehensive review recommended")
            assessment = "REVIEW REQUIRED"
            color = "red"
    
    # Generate certificate
    st.markdown("---")
    st.subheader("Mariner Vision Assessment Certificate")
    
    cert_col1, cert_col2, cert_col3 = st.columns([1, 2, 1])
    
    with cert_col2:
        st.markdown(f"""
        <div style='border: 3px solid {color}; 
                    padding: 2rem; 
                    border-radius: 15px;
                    text-align: center;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
            <h1 style='color: #1E3A8A;'>⚓ VISIONQUEST NAVIGATOR</h1>
            <h2 style='color: #1E3A8A;'>Mariner Vision Assessment</h2>
            <hr>
            <h3>MARINER: {st.session_state.user_data.get('name', 'Not Provided')}</h3>
            <h3>RANK: {st.session_state.user_data.get('rank', 'Not Provided')}</h3>
            <h3>COMPANY: {st.session_state.user_data.get('company', 'Not Provided')}</h3>
            <hr>
            <h2 style='color: {color};'>{assessment}</h2>
            <p>Overall Score: <strong>{overall_score:.1f}%</strong></p>
            <p>Tests Completed: {total_tests}/7</p>
            <p>Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
            <small>This assessment is for informational purposes and should be reviewed by qualified medical personnel.</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Download results
    if st.button("📄 Generate Printable Report", type="primary"):
        st.info("Full reporting functionality would be implemented in production version")
        st.success("Report generation complete! This would create a PDF in the full application.")

if __name__ == "__main__":
    main()