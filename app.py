import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
import io

# Page configuration
st.set_page_config(
    page_title="VisionQuest Navigator",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .test-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 5px solid #1E3A8A;
    }
    .warning-box {
        background: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .navy-button {
        background: #1E3A8A;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_test' not in st.session_state:
    st.session_state.current_test = "home"
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

def main():
    # Header
    st.image("https://i.postimg.cc/fbcrnNXC/Gemini-Generated-Image-6gukqc6gukqc6guk.png", use_column_width=True)

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    menu_option = st.sidebar.radio("Select Test:", [
        "🏠 Home",
        "🎯 Ishihara Test", 
        "🌈 Farnsworth D-15 Test",
        "💡 Lantern Test",
        "🗺️ ECDIS Simulation", 
        "📡 Radar Simulation",
        "🚢 Visual Navigation",
        "📊 Results"
    ])

    # User info
    st.sidebar.title("👤 Mariner Information")
    st.sidebar.text_input("Full Name", key="user_name")
    st.sidebar.selectbox("Rank", ["Captain", "Chief Officer", "Second Officer", "Deck Cadet"], key="user_rank")

    # Route to selected test
    if "Home" in menu_option:
        show_home()
    elif "Ishihara" in menu_option:
        ishihara_test()
    elif "Farnsworth" in menu_option:
        farnsworth_test()
    elif "Lantern" in menu_option:
        lantern_test()
    elif "ECDIS" in menu_option:
        ecd_simulation()
    elif "Radar" in menu_option:
        radar_simulation()
    elif "Visual Navigation" in menu_option:
        visual_navigation_test()
    elif "Results" in menu_option:
        show_results()

def show_home():
    st.markdown('<div class="main-header">VisionQuest Navigator</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Maritime Vision Testing Suite")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="test-container">
            <h3>🚢 Why Proper Testing Matters</h3>
            <p>Traditional Ishihara tests alone are insufficient for maritime professionals. 
            Modern navigation requires accurate color perception in realistic conditions:</p>
            <ul>
            <li><strong>ECDIS displays</strong> with specialized color palettes for day/dusk/night modes</li>
            <li><strong>Navigation lights</strong> recognition at varying distances and conditions</li>
            <li><strong>Radar displays</strong> with color-coded targets and warning systems</li>
            <li><strong>Buoy identification</strong> in different lighting and weather conditions</li>
            <li><strong>Chart interpretation</strong> with complex color-coded information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="test-container">
            <h3>📋 Testing Protocol</h3>
            <ol>
            <li><strong>Complete all tests</strong> in the recommended sequence</li>
            <li><strong>Ensure proper lighting</strong> - avoid glare and reflections</li>
            <li><strong>Maintain 50-70cm viewing distance</strong> from screen</li>
            <li><strong>Do not adjust screen colors</strong> or brightness during testing</li>
            <li><strong>Use calibrated monitor</strong> for accurate results</li>
            <li><strong>Record results</strong> for professional medical review</li>
            </ol>
            <p><strong>Estimated completion time:</strong> 25-35 minutes</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Important Notice:</strong> This testing suite simulates real maritime navigation scenarios. 
    For certification purposes, results should be verified by qualified medical personnel using standardized equipment.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 BEGIN MARITIME VISION TESTING", use_container_width=True, type="primary"):
        st.session_state.current_test = "ishihara"
        st.session_state.test_results = {}
        st.session_state.user_answers = {}
        st.rerun()

def create_ishihara_plate(number, size=400):
    """Create a proper Ishihara color plate"""
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create dot pattern background
    dot_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for _ in range(800):
        x = random.randint(20, size-20)
        y = random.randint(20, size-20)
        color = random.choice(dot_colors)
        radius = random.randint(8, 20)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Add number pattern (simplified representation)
    if number == "12":
        # Draw '12' pattern
        for x in range(120, 180, 15):
            for y in range(150, 210, 15):
                draw.ellipse([x-8, y-8, x+8, y+8], fill='#2C3E50')
        for x in range(220, 280, 15):
            for y in range(150, 210, 15):
                draw.ellipse([x-8, y-8, x+8, y+8], fill='#2C3E50')
    elif number == "8":
        # Draw '8' pattern
        points = [(150,120), (200,120), (150,200), (200,200), (150,160), (200,160)]
        for x, y in points:
            draw.ellipse([x-10, y-10, x+10, y+10], fill='#2C3E50')
    
    return img

def ishihara_test():
    st.markdown("## 🎯 Ishihara Color Vision Test")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Identify the numbers visible in each color plate. Enter the number you see in the text box below each image.</p>
        <p>If no number is visible, enter <strong>0</strong>. There are 8 plates total.</p>
    </div>
    """, unsafe_allow_html=True)

    # Ishihara plates data
    plates = [
        {"correct": "12", "description": "Red-green deficiency screening"},
        {"correct": "8", "description": "Basic number recognition"},
        {"correct": "6", "description": "Color contrast sensitivity"}, 
        {"correct": "29", "description": "Two-digit number recognition"},
        {"correct": "5", "description": "Low contrast conditions"},
        {"correct": "3", "description": "Complex pattern recognition"},
        {"correct": "15", "description": "Traffic signal simulation"},
        {"correct": "74", "description": "Advanced color discrimination"}
    ]

    # Initialize answers if not exists
    if 'ishihara_answers' not in st.session_state.user_answers:
        st.session_state.user_answers['ishihara'] = [""] * len(plates)

    # Display plates
    for i, plate in enumerate(plates):
        st.markdown(f"**Plate {i+1} of {len(plates)}** - {plate['description']}")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Display Ishihara plate
            plate_img = create_ishihara_plate(plate["correct"])
            st.image(plate_img, use_column_width=True)
            
        with col2:
            answer = st.text_input(
                f"What number do you see?",
                value=st.session_state.user_answers['ishihara'][i],
                key=f"ishihara_{i}",
                placeholder="Enter number or '0' if none visible"
            )
            st.session_state.user_answers['ishihara'][i] = answer

        st.markdown("---")

    if st.button("📊 Calculate Ishihara Results", use_container_width=True, type="primary"):
        correct_count = 0
        for i, plate in enumerate(plates):
            if st.session_state.user_answers['ishihara'][i] == plate["correct"]:
                correct_count += 1
        
        score = (correct_count / len(plates)) * 100
        
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct_count,
            'total': len(plates),
            'type': 'Color Deficiency Screening'
        }
        
        st.success(f"**Ishihara Test Complete:** {correct_count}/{len(plates)} correct ({score:.1f}%)")
        
        if score >= 85:
            st.success("✅ **EXCELLENT** - Normal color vision for maritime duties")
        elif score >= 70:
            st.warning("⚠️ **SATISFACTORY** - Minor color perception issues detected")
        else:
            st.error("❌ **REVIEW REQUIRED** - Significant color vision deficiencies detected")

def farnsworth_test():
    st.markdown("## 🌈 Farnsworth D-15 Color Arrangement Test")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Arrange the colors in correct spectral order. Click the colors in the sequence you believe represents the smoothest color transition.</p>
        <p>This test evaluates your ability to discriminate subtle color differences critical for ECDIS interpretation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Color sequence test
    colors = [
        {"name": "Red", "hex": "#FF0000", "emoji": "🔴"},
        {"name": "Red-Orange", "hex": "#FF4500", "emoji": "🟠"}, 
        {"name": "Orange", "hex": "#FFA500", "emoji": "🟠"},
        {"name": "Yellow-Orange", "hex": "#FFD700", "emoji": "🟡"},
        {"name": "Yellow", "hex": "#FFFF00", "emoji": "🟡"},
        {"name": "Yellow-Green", "hex": "#9ACD32", "emoji": "🟢"},
        {"name": "Green", "hex": "#00FF00", "emoji": "🟢"},
        {"name": "Blue-Green", "hex": "#20B2AA", "emoji": "🔵"},
        {"name": "Blue", "hex": "#0000FF", "emoji": "🔵"}
    ]

    st.subheader("Color Sequence Recognition")
    
    # Question 1
    st.write("**Question 1:** Which color comes between 🔴 Red and 🟡 Yellow in the spectrum?")
    q1_answer = st.radio("Select the correct color:", 
                        ["🟠 Orange", "🟢 Green", "🔵 Blue", "🟣 Purple"],
                        key="farnsworth_q1")
    
    # Question 2  
    st.write("**Question 2:** Identify the correct spectral sequence:")
    q2_answer = st.radio("Select the correct order:",
                        ["Red → Green → Blue", "Red → Orange → Yellow → Green → Blue", 
                         "Red → Blue → Green", "Red → Purple → Blue"],
                        key="farnsworth_q2")
    
    # Question 3
    st.write("**Question 3:** Which color is most difficult to distinguish from its neighbors for color-deficient individuals?")
    q3_answer = st.radio("Select the color:",
                        ["🔴 Red", "🟢 Green", "🔵 Blue", "🟠 Orange"],
                        key="farnsworth_q3")

    if st.button("📊 Calculate Farnsworth Results", use_container_width=True, type="primary"):
        score = 0
        if q1_answer == "🟠 Orange":
            score += 1
        if "Red → Orange → Yellow → Green → Blue" in q2_answer:
            score += 1  
        if q3_answer == "🟢 Green":
            score += 1
            
        total_score = (score / 3) * 100
        
        st.session_state.test_results['farnsworth'] = {
            'score': total_score,
            'correct': score,
            'total': 3,
            'type': 'Color Discrimination'
        }
        
        st.success(f"**Farnsworth Test Complete:** {score}/3 correct ({total_score:.1f}%)")

def lantern_test():
    st.markdown("## 💡 Navigation Lights Recognition Test")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Identify navigation light configurations as they would appear at sea. Select the correct vessel type or situation for each light pattern.</p>
        <p>This test simulates real-world navigation light recognition under various conditions.</p>
    </div>
    """, unsafe_allow_html=True)

    scenarios = [
        {
            "lights": "🔴 Red + 🟢 Green + ⚪ White",
            "description": "Lights visible: Red, Green, and White",
            "question": "What type of vessel is this?",
            "options": ["Power-driven vessel underway", "Vessel at anchor", "Fishing vessel", "Vessel constrained by draft"],
            "correct": "Power-driven vessel underway"
        },
        {
            "lights": "🔴 Red + 🔴 Red + 🔴 Red", 
            "description": "Lights visible: Three all-round red lights",
            "question": "What does this indicate?",
            "options": ["Vessel not under command", "Vessel constrained by draft", "Fishing vessel trawling", "Pilot vessel"],
            "correct": "Vessel constrained by draft"
        },
        {
            "lights": "🟢 Green + ⚪ White + ⚪ White",
            "description": "Lights visible: Green over two white lights", 
            "question": "What vessel situation is this?",
            "options": ["Towing vessel >200m", "Fishing vessel other than trawling", "Vessel engaged in dredging", "Sailing vessel"],
            "correct": "Towing vessel >200m"
        },
        {
            "lights": "🔴 Red + ⚪ White",
            "description": "Lights visible: Red over white",
            "question": "Identify the vessel type:",
            "options": ["Pilot vessel on duty", "Fishing vessel", "Vessel at anchor", "Vessel aground"],
            "correct": "Pilot vessel on duty"
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.markdown(f"**Scenario {i+1}:** {scenario['lights']}")
        st.write(scenario['description'])
        
        answer = st.radio(
            scenario['question'],
            scenario['options'],
            key=f"lantern_{i}"
        )
        answers.append(answer)
        st.markdown("---")

    if st.button("📊 Calculate Lantern Test Results", use_container_width=True, type="primary"):
        score = 0
        for i, scenario in enumerate(scenarios):
            if answers[i] == scenario['correct']:
                score += 1
                
        total_score = (score / len(scenarios)) * 100
        
        st.session_state.test_results['lantern'] = {
            'score': total_score,
            'correct': score, 
            'total': len(scenarios),
            'type': 'Navigation Lights'
        }
        
        st.success(f"**Lantern Test Complete:** {score}/{len(scenarios)} correct ({total_score:.1f}%)")

def ecd_simulation():
    st.markdown("## 🗺️ ECDIS Color Recognition Simulation")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Identify the meaning of colors used in Electronic Chart Display and Information Systems (ECDIS).</p>
        <p>This test evaluates your ability to interpret color-coded navigation information under different display modes.</p>
    </div>
    """, unsafe_allow_html=True)

    # ECDIS color scenarios
    scenarios = [
        {
            "mode": "🌞 Day Mode",
            "question": "What does DARK BLUE typically represent on ECDIS?",
            "options": ["Deep water (>100m)", "Shallow water (<10m)", "Restricted area", "Traffic separation scheme"],
            "correct": "Deep water (>100m)"
        },
        {
            "mode": "🌆 Dusk Mode",
            "question": "Which color indicates DANGEROUS AREAS on ECDIS displays?",
            "options": ["Red", "Yellow", "Green", "Blue"], 
            "correct": "Red"
        },
        {
            "mode": "🌙 Night Mode", 
            "question": "What color is used for SAFETY CONTOURS (isolines)?",
            "options": ["Magenta", "Green", "Blue", "Yellow"],
            "correct": "Magenta"
        },
        {
            "mode": "🌞 Day Mode",
            "question": "Which color represents the SHIP'S TRACK on ECDIS?",
            "options": ["Green line", "Yellow line", "Red line", "Blue line"],
            "correct": "Green line"
        },
        {
            "mode": "🌆 Dusk Mode",
            "question": "What does CYAN/BLUE-GREEN typically indicate?",
            "options": ["Recommended track", "Danger area", "Anchorage area", "Depth information"],
            "correct": "Depth information"
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.markdown(f"**{scenario['mode']}**")
        st.write(scenario['question'])
        
        answer = st.radio(
            "Select your answer:",
            scenario['options'],
            key=f"ecdis_{i}"
        )
        answers.append(answer)
        st.markdown("---")

    if st.button("📊 Calculate ECDIS Test Results", use_container_width=True, type="primary"):
        score = 0
        for i, scenario in enumerate(scenarios):
            if answers[i] == scenario['correct']:
                score += 1
                
        total_score = (score / len(scenarios)) * 100
        
        st.session_state.test_results['ecdis'] = {
            'score': total_score,
            'correct': score,
            'total': len(scenarios),
            'type': 'ECDIS Colors'
        }
        
        st.success(f"**ECDIS Test Complete:** {score}/{len(scenarios)} correct ({total_score:.1f}%)")

def radar_simulation():
    st.markdown("## 📡 Radar Display Interpretation")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Interpret colors and symbols on modern radar displays. Identify what different colors represent in various radar modes.</p>
        <p>This test evaluates your ability to quickly interpret radar information for collision avoidance and navigation.</p>
    </div>
    """, unsafe_allow_html=True)

    scenarios = [
        {
            "mode": "Standard Mode",
            "question": "What does a FLASHING RED target typically indicate?",
            "options": ["New acquisition", "Dangerous target", "Target on collision course", "Lost target"],
            "correct": "Target on collision course"
        },
        {
            "mode": "True Motion",
            "question": "What color usually represents YOUR VESSEL on radar?",
            "options": ["Green", "Yellow", "White", "Blue"],
            "correct": "Green"
        },
        {
            "mode": "Relative Motion", 
            "question": "What does a YELLOW track line represent?",
            "options": ["Own ship history", "Target predicted path", "Danger area", "Navigation line"],
            "correct": "Target predicted path"
        },
        {
            "mode": "ARPA Mode",
            "question": "What color indicates a TARGET LOST situation?",
            "options": ["Gray", "Red", "Yellow", "Magenta"],
            "correct": "Gray"
        },
        {
            "mode": "Navigation Mode",
            "question": "What does a BLUE/GREEN area typically represent?",
            "options": ["Shallow water", "Land mass", "Traffic lane", "Anchorage area"],
            "correct": "Land mass"
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.markdown(f"**{scenario['mode']}**")
        st.write(scenario['question'])
        
        answer = st.radio(
            "Select your answer:",
            scenario['options'],
            key=f"radar_{i}"
        )
        answers.append(answer)
        st.markdown("---")

    if st.button("📊 Calculate Radar Test Results", use_container_width=True, type="primary"):
        score = 0
        for i, scenario in enumerate(scenarios):
            if answers[i] == scenario['correct']:
                score += 1
                
        total_score = (score / len(scenarios)) * 100
        
        st.session_state.test_results['radar'] = {
            'score': total_score,
            'correct': score,
            'total': len(scenarios),
            'type': 'Radar Interpretation'
        }
        
        st.success(f"**Radar Test Complete:** {score}/{len(scenarios)} correct ({total_score:.1f}%)")

def visual_navigation_test():
    st.markdown("## 🚢 Visual Navigation & Buoy Recognition")
    
    st.markdown("""
    <div class="test-container">
        <h3>Test Instructions:</h3>
        <p>Identify buoy colors, shapes, and light characteristics in various conditions.</p>
        <p>This test evaluates your ability to recognize navigation marks under different lighting and weather conditions.</p>
    </div>
    """, unsafe_allow_html=True)

    scenarios = [
        {
            "conditions": "🌅 Sunrise conditions",
            "question": "What color is a PORT SIDE buoy (IALA System A)?",
            "options": ["Red", "Green", "Yellow", "Black"],
            "correct": "Red"
        },
        {
            "conditions": "🌃 Night conditions",
            "question": "What does a RED & WHITE VERTICAL STRIPED buoy indicate?",
            "options": ["Safe water", "Isolated danger", "Special purpose", "Cardinal mark"],
            "correct": "Safe water"
        },
        {
            "conditions": "🌫️ Foggy conditions",
            "question": "What color are SPECIAL MARKS (yellow buoys)?", 
            "options": ["Yellow", "Orange", "White", "Blue"],
            "correct": "Yellow"
        },
        {
            "conditions": "🌆 Dusk conditions",
            "question": "What shape is a STARBOARD HAND buoy?",
            "options": ["Cone (triangle)", "Can (cylinder)", "Sphere", "Pillar"],
            "correct": "Cone (triangle)"
        },
        {
            "conditions": "☀️ Bright daylight",
            "question": "What does a BLACK & YELLOW HORIZONTAL buoy indicate?",
            "options": ["Cardinal mark", "Isolated danger", "Special mark", "Safe water"],
            "correct": "Cardinal mark"
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.markdown(f"**Conditions:** {scenario['conditions']}")
        st.write(scenario['question'])
        
        answer = st.radio(
            "Select your answer:",
            scenario['options'],
            key=f"visual_{i}"
        )
        answers.append(answer)
        st.markdown("---")

    if st.button("📊 Calculate Visual Navigation Results", use_container_width=True, type="primary"):
        score = 0
        for i, scenario in enumerate(scenarios):
            if answers[i] == scenario['correct']:
                score += 1
                
        total_score = (score / len(scenarios)) * 100
        
        st.session_state.test_results['visual_nav'] = {
            'score': total_score,
            'correct': score,
            'total': len(scenarios),
            'type': 'Visual Navigation'
        }
        
        st.success(f"**Visual Navigation Test Complete:** {score}/{len(scenarios)} correct ({total_score:.1f}%)")

def show_results():
    st.markdown("## 📊 Comprehensive Test Results")
    
    if not st.session_state.test_results:
        st.warning("No test results available. Please complete at least one test.")
        return

    # Calculate overall statistics
    total_tests = len(st.session_state.test_results)
    overall_score = sum(result['score'] for result in st.session_state.test_results.values()) / total_tests
    
    # Display overall summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{overall_score:.1f}%")
    with col2:
        st.metric("Tests Completed", total_tests)
    with col3:
        if overall_score >= 85:
            st.success("FIT FOR DUTY")
        elif overall_score >= 70:
            st.warning("CONDITIONAL")
        else:
            st.error("REVIEW REQUIRED")

    # Detailed results table
    st.subheader("Detailed Test Results")
    results_data = []
    for test_name, results in st.session_state.test_results.items():
        results_data.append({
            'Test': test_name.replace('_', ' ').title(),
            'Type': results.get('type', 'General'),
            'Score': f"{results['score']:.1f}%",
            'Correct': f"{results['correct']}/{results['total']}",
            'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review'
        })
    
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)

    # Generate certificate
    st.markdown("---")
    st.subheader("🎓 Maritime Vision Assessment Certificate")
    
    certificate_html = f"""
    <div style='border: 3px solid #1E3A8A; padding: 2rem; border-radius: 10px; background: #f8f9fa;'>
        <h2 style='color: #1E3A8A; text-align: center; margin-bottom: 1rem;'>VisionQuest Navigator</h2>
        <h3 style='text-align: center; color: #4B5563; margin-bottom: 2rem;'>Maritime Vision Assessment Certificate</h3>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;'>
            <div>
                <p><strong>Mariner:</strong> {st.session_state.get('user_name', 'Not Provided')}</p>
                <p><strong>Rank:</strong> {st.session_state.get('user_rank', 'Not Provided')}</p>
            </div>
            <div>
                <p><strong>Overall Score:</strong> {overall_score:.1f}%</p>
                <p><strong>Tests Completed:</strong> {total_tests}/6</p>
            </div>
        </div>
        
        <div style='text-align: center; padding: 1rem; background: {"#D1FAE5" if overall_score >= 85 else "#FEF3C7" if overall_score >= 70 else "#FEE2E2"}; border-radius: 5px;'>
            <h4 style='margin: 0; color: {"#065F46" if overall_score >= 85 else "#92400E" if overall_score >= 70 else "#991B1B"};'>
                {'FIT FOR MARITIME DUTY' if overall_score >= 85 else 'CONDITIONALLY FIT - REVIEW RECOMMENDED' if overall_score >= 70 else 'COMPREHENSIVE REVIEW REQUIRED'}
            </h4>
        </div>
        
        <p style='text-align: center; margin-top: 2rem; font-size: 0.9rem; color: #6B7280;'>
            Assessment Date: {pd.Timestamp.now().strftime('%B %d, %Y')}<br>
            This assessment should be verified by qualified medical personnel for official certification purposes.
        </p>
    </div>
    """
    
    st.markdown(certificate_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()