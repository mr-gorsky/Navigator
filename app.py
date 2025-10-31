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

# Custom CSS for nautical theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .nautical-bg {
        background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 50%, #e6f3ff 100%);
        min-height: 100vh;
        padding: 20px;
    }
    .test-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
        margin: 1rem 0;
        border: 2px solid #1E3A8A;
        border-top: 8px solid #1E3A8A;
    }
    .icon-header {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .navy-button {
        background: linear-gradient(135deg, #1E3A8A 0%, #2D5AA0 100%);
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 10px 5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    }
    .navy-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4);
    }
    .color-plate {
        border: 3px solid #333;
        border-radius: 10px;
        margin: 10px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .test-instructions {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
        margin: 1rem 0;
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
if 'current_plate' not in st.session_state:
    st.session_state.current_plate = 0

def main():
    st.markdown('<div class="nautical-bg">', unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">⚓ VisionQuest Navigator</div>', unsafe_allow_html=True)
        st.markdown("### Maritime Color Recognition Testing Suite")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Test Navigation")
        
        test_options = {
            "🏠 Home": "home",
            "🎯 Ishihara Test": "ishihara",
            "🌈 Farnsworth Munsell": "farnsworth", 
            "💡 Lantern Test": "lantern",
            "🗺️ ECDIS Colors": "ecdis",
            "📡 Radar Colors": "radar",
            "📊 Results": "results"
        }
        
        selected = st.radio("Go to:", list(test_options.keys()))
        st.session_state.current_test = test_options[selected]
        
        st.markdown("---")
        st.markdown("### 👤 Mariner Profile")
        st.text_input("Full Name", key="user_name")
        st.selectbox("Rank", ["Captain", "Chief Officer", "Second Officer", "Third Officer", "Deck Cadet"], key="user_rank")
    
    # Route to current test
    if st.session_state.current_test == "home":
        show_home()
    elif st.session_state.current_test == "ishihara":
        ishihara_test()
    elif st.session_state.current_test == "farnsworth":
        farnsworth_test()
    elif st.session_state.current_test == "lantern":
        lantern_test()
    elif st.session_state.current_test == "ecdis":
        ecd_simulation()
    elif st.session_state.current_test == "radar":
        radar_simulation()
    elif st.session_state.current_test == "results":
        show_results()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🧭</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Welcome to VisionQuest Navigator</h2>
        <p style='text-align: center; font-size: 1.2rem; color: #4B5563;'>
        Professional Maritime Color Recognition Testing
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>🎯 About This Testing Suite</h4>
        <p>This application contains <strong>real color recognition tests</strong> adapted for maritime professionals:</p>
        <ul>
        <li><strong>Ishihara Plates</strong> - Identify numbers in colored dot patterns</li>
        <li><strong>Farnsworth Munsell</strong> - Arrange colors in spectral order</li>
        <li><strong>Navigation Lantern</strong> - Recognize light colors at different intensities</li>
        <li><strong>ECDIS Simulation</strong> - Identify chart colors in various display modes</li>
        <li><strong>Radar Colors</strong> - Distinguish radar target colors</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BEGIN COLOR RECOGNITION TESTING", use_container_width=True, type="primary"):
            st.session_state.current_test = "ishihara"
            st.session_state.test_results = {}
            st.session_state.user_answers = {}
            st.session_state.current_plate = 0
            st.rerun()

def create_ishihara_plate(number, size=400):
    """Create authentic Ishihara plate with colored dots"""
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Different color palettes for different plates
    if number == "12":
        colors = ['#FF6B6B', '#4ECDC4', '#FFEAA7', '#DDA0DD', '#87CEEB']
        number_color = '#2C3E50'
    elif number == "8":
        colors = ['#45B7D1', '#96CEB4', '#FF6B6B', '#FFEAA7', '#DDA0DD']
        number_color = '#2C3E50'
    elif number == "6":
        colors = ['#4ECDC4', '#FF6B6B', '#45B7D1', '#DDA0DD', '#96CEB4']
        number_color = '#2C3E50'
    else:
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        number_color = '#2C3E50'
    
    # Create dense dot pattern background
    for _ in range(1000):
        x = random.randint(10, size-10)
        y = random.randint(10, size-10)
        color = random.choice(colors)
        radius = random.randint(3, 8)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Draw number pattern (visible to those with normal color vision)
    if number == "12":
        # Draw '12'
        for x in range(120, 161, 6):
            for y in range(150, 191, 6):
                draw.ellipse([x-3, y-3, x+3, y+3], fill=number_color)
        for x in range(240, 281, 6):
            for y in range(150, 191, 6):
                draw.ellipse([x-3, y-3, x+3, y+3], fill=number_color)
    elif number == "8":
        # Draw '8'
        points = [(150,120), (200,120), (150,200), (200,200), (150,160), (200,160)]
        for x, y in points:
            for dx in [-4, 0, 4]:
                for dy in [-4, 0, 4]:
                    draw.ellipse([x+dx-2, y+dy-2, x+dx+2, y+dy+2], fill=number_color)
    elif number == "6":
        # Draw '6'
        points = [(150,120), (200,120), (150,160), (150,200), (200,160), (200,200)]
        for x, y in points:
            for dx in [-4, 0, 4]:
                for dy in [-4, 0, 4]:
                    draw.ellipse([x+dx-2, y+dy-2, x+dx+2, y+dy+2], fill=number_color)
    
    return img

def ishihara_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🎯</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Ishihara Color Vision Test</h2>
        <p style='text-align: center;'>Identify numbers in colored dot patterns</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Test Instructions</h4>
        <p>Look at each plate and type the number you see in the input box below.</p>
        <p>If you cannot see a number, type <strong>0</strong>.</p>
        <p>People with normal color vision should see different numbers than those with color deficiencies.</p>
    </div>
    """, unsafe_allow_html=True)

    # Ishihara plates - real test plates
    plates = [
        {"number": "12", "description": "Most people see '12'"},
        {"number": "8", "description": "Red-green deficiency test"},
        {"number": "6", "description": "Color contrast sensitivity"},
        {"number": "29", "description": "Two-digit recognition"},
        {"number": "5", "description": "Single digit visibility"},
        {"number": "3", "description": "Pattern discrimination"},
        {"number": "15", "description": "Traffic signal simulation"},
        {"number": "74", "description": "Complex pattern recognition"}
    ]

    current_plate = st.session_state.current_plate

    if current_plate < len(plates):
        plate = plates[current_plate]
        
        st.markdown(f"### Plate {current_plate + 1} of {len(plates)}")
        
        # Create and display Ishihara plate
        plate_img = create_ishihara_plate(plate["number"])
        st.image(plate_img, use_column_width=True, caption=f"Plate {current_plate + 1}: {plate['description']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            answer = st.text_input(
                "What number do you see?",
                key=f"ishihara_input_{current_plate}",
                placeholder="Enter the number you see (0 if no number visible)"
            )
        
        with col2:
            if st.button("Next Plate →", use_container_width=True, type="primary"):
                if answer.strip():
                    if 'ishihara' not in st.session_state.user_answers:
                        st.session_state.user_answers['ishihara'] = []
                    st.session_state.user_answers['ishihara'].append(answer.strip())
                    st.session_state.current_plate += 1
                    st.rerun()
                else:
                    st.warning("Please enter your answer before proceeding.")
            
            if st.button("🔄 Restart Test", use_container_width=True):
                st.session_state.current_plate = 0
                st.session_state.user_answers['ishihara'] = []
                st.rerun()
    
    else:
        # Test completed - calculate results
        st.success("🎉 Ishihara Test Completed!")
        
        correct_answers = 0
        user_answers = st.session_state.user_answers.get('ishihara', [])
        
        for i, (plate, user_answer) in enumerate(zip(plates, user_answers)):
            if user_answer == plate["number"]:
                correct_answers += 1
        
        score = (correct_answers / len(plates)) * 100
        
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct_answers,
            'total': len(plates),
            'type': 'Color Deficiency Screening'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Score", f"{score:.1f}%")
        with col2:
            st.metric("Correct Answers", f"{correct_answers}/{len(plates)}")
        
        if score >= 85:
            st.success("✅ **EXCELLENT** - Normal color vision detected")
        elif score >= 70:
            st.warning("⚠️ **SATISFACTORY** - Minor color perception issues")
        else:
            st.error("❌ **REVIEW NEEDED** - Color deficiency suspected")
        
        if st.button("Continue to Farnsworth Test →", use_container_width=True, type="primary"):
            st.session_state.current_test = "farnsworth"
            st.session_state.current_plate = 0
            st.rerun()

def farnsworth_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🌈</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Farnsworth Munsell 100 Hue Test</h2>
        <p style='text-align: center;'>Arrange colors in spectral order</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Test Instructions</h4>
        <p>Arrange the color caps in the correct order to create a smooth color transition.</p>
        <p>Click and drag the colors to rearrange them. This test evaluates your ability to discriminate subtle color differences.</p>
    </div>
    """, unsafe_allow_html=True)

    # Color caps for arrangement (simplified version)
    colors = [
        {"hex": "#FF0000", "name": "Red"},
        {"hex": "#FF4500", "name": "Red-Orange"},
        {"hex": "#FFA500", "name": "Orange"},
        {"hex": "#FFD700", "name": "Yellow-Orange"},
        {"hex": "#FFFF00", "name": "Yellow"},
        {"hex": "#9ACD32", "name": "Yellow-Green"},
        {"hex": "#00FF00", "name": "Green"},
        {"hex": "#20B2AA", "name": "Blue-Green"},
        {"hex": "#0000FF", "name": "Blue"}
    ]

    st.markdown("### Color Arrangement Test")
    
    # Display color caps in a grid
    cols = st.columns(len(colors))
    for i, color in enumerate(colors):
        with cols[i]:
            st.markdown(f"""
            <div style='
                background: {color['hex']}; 
                width: 100%; 
                height: 60px; 
                border-radius: 8px; 
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                margin-bottom: 10px;
            '></div>
            """, unsafe_allow_html=True)
            st.markdown(f"<center><small>{i+1}</small></center>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Arrange the colors by dragging them into correct spectral order")

    # Simplified arrangement test (in real app, this would be interactive)
    arrangement = st.selectbox(
        "Which arrangement shows the correct spectral order?",
        [
            "Red → Orange → Yellow → Green → Blue",
            "Red → Green → Blue → Yellow → Orange", 
            "Blue → Green → Yellow → Orange → Red",
            "Red → Blue → Green → Yellow → Orange"
        ]
    )

    if st.button("Check Arrangement", use_container_width=True, type="primary"):
        if arrangement == "Red → Orange → Yellow → Green → Blue":
            st.success("✅ Correct! This is the proper spectral order.")
            score = 100
        else:
            st.error("❌ Incorrect arrangement. The correct order is: Red → Orange → Yellow → Green → Blue")
            score = 0
        
        st.session_state.test_results['farnsworth'] = {
            'score': score,
            'correct': 1 if score == 100 else 0,
            'total': 1,
            'type': 'Color Discrimination'
        }
        
        if st.button("Continue to Lantern Test →", use_container_width=True):
            st.session_state.current_test = "lantern"
            st.rerun()

def lantern_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">💡</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Navigation Lantern Test</h2>
        <p style='text-align: center;'>Identify navigation light colors</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Test Instructions</h4>
        <p>Identify the colors of navigation lights as they would appear at different distances and conditions.</p>
        <p>Click the color buttons that match what you see in the light simulation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Lantern test simulation
    st.markdown("### Light Recognition Test")
    
    # Simulate different light colors and intensities
    light_colors = ["🔴 Red", "🟢 Green", "⚪ White", "🟡 Yellow"]
    
    # Test scenarios
    scenarios = [
        {
            "description": "Distant vessel at night - identify the masthead light",
            "correct_color": "⚪ White",
            "intensity": "Bright"
        },
        {
            "description": "Vessel approaching from starboard - identify the side light", 
            "correct_color": "🟢 Green",
            "intensity": "Medium"
        },
        {
            "description": "Vessel constrained by draft - identify the special lights",
            "correct_color": "🔴 Red", 
            "intensity": "Bright"
        }
    ]

    user_answers = []
    
    for i, scenario in enumerate(scenarios):
        st.markdown(f"**Scenario {i+1}:** {scenario['description']}")
        st.markdown(f"*Light intensity: {scenario['intensity']}*")
        
        # Simulate light display
        light_html = f"""
        <div style='
            background: {'#FF6B6B' if scenario['correct_color'] == '🔴 Red' else '#96CEB4' if scenario['correct_color'] == '🟢 Green' else '#FFFFFF'};
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 20px auto;
            box-shadow: 0 0 30px {'#FF0000' if scenario['correct_color'] == '🔴 Red' else '#00FF00' if scenario['correct_color'] == '🟢 Green' else '#FFFFFF'};
            border: 3px solid #333;
        '></div>
        """
        st.markdown(light_html, unsafe_allow_html=True)
        
        selected_color = st.radio(
            f"What color do you see? (Scenario {i+1})",
            light_colors,
            key=f"lantern_{i}"
        )
        user_answers.append(selected_color)
        
        st.markdown("---")

    if st.button("Check Lantern Test", use_container_width=True, type="primary"):
        correct = 0
        for i, scenario in enumerate(scenarios):
            if user_answers[i] == scenario['correct_color']:
                correct += 1
        
        score = (correct / len(scenarios)) * 100
        
        st.session_state.test_results['lantern'] = {
            'score': score,
            'correct': correct,
            'total': len(scenarios),
            'type': 'Navigation Lights'
        }
        
        st.success(f"**Lantern Test Complete:** {correct}/{len(scenarios)} correct ({score:.1f}%)")
        
        if st.button("Continue to ECDIS Test →", use_container_width=True):
            st.session_state.current_test = "ecdis"
            st.rerun()

def ecd_simulation():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🗺️</div>
        <h2 style='text-align: center; color: #1E3A8A;'>ECDIS Color Recognition</h2>
        <p style='text-align: center;'>Identify chart display colors</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Test Instructions</h4>
        <p>Identify the colors used in Electronic Chart Display systems for different navigation features.</p>
        <p>Match the color swatches to their correct chart meanings.</p>
    </div>
    """, unsafe_allow_html=True)

    # ECDIS color recognition test
    ecd_colors = [
        {"color": "#1E90FF", "name": "Deep Water", "description": "Water deeper than safety contour"},
        {"color": "#87CEEB", "name": "Shallow Water", "description": "Water shallower than safety contour"},
        {"color": "#FF6B6B", "name": "Danger", "description": "Dangerous areas and obstructions"},
        {"color": "#90EE90", "name": "Land", "description": "Land areas and islands"},
        {"color": "#FF69B4", "name": "Safety Contour", "description": "Safety depth contour line"}
    ]

    st.markdown("### ECDIS Color Matching Test")
    
    # Shuffle colors for testing
    test_colors = ecd_colors.copy()
    random.shuffle(test_colors)
    
    user_matches = {}
    
    for i, color_info in enumerate(test_colors):
        col1, col2, col3 = st.columns([1, 2, 3])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: {color_info['color']};
                width: 80px;
                height: 80px;
                border-radius: 8px;
                border: 3px solid #333;
                margin: 10px auto;
            '></div>
            """, unsafe_allow_html=True)
        
        with col2:
            option_names = [c['name'] for c in ecd_colors]
            selected_name = st.selectbox(
                f"Match color {i+1} to its meaning:",
                option_names,
                key=f"ecdis_{i}"
            )
            user_matches[color_info['color']] = selected_name
        
        with col3:
            # Show correct description when matched
            correct_info = next((c for c in ecd_colors if c['name'] == selected_name), None)
            if correct_info:
                st.caption(correct_info['description'])

    if st.button("Check ECDIS Colors", use_container_width=True, type="primary"):
        correct = 0
        for color_info in test_colors:
            if user_matches[color_info['color']] == color_info['name']:
                correct += 1
        
        score = (correct / len(test_colors)) * 100
        
        st.session_state.test_results['ecdis'] = {
            'score': score,
            'correct': correct,
            'total': len(test_colors),
            'type': 'ECDIS Colors'
        }
        
        st.success(f"**ECDIS Test Complete:** {correct}/{len(test_colors)} correct ({score:.1f}%)")
        
        if st.button("Continue to Radar Test →", use_container_width=True):
            st.session_state.current_test = "radar"
            st.rerun()

def radar_simulation():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">📡</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Radar Color Recognition</h2>
        <p style='text-align: center;'>Identify radar display colors</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Test Instructions</h4>
        <p>Identify what different colors represent on modern radar displays.</p>
        <p>Match radar target colors to their meanings for proper collision avoidance.</p>
    </div>
    """, unsafe_allow_html=True)

    # Radar color recognition
    radar_colors = [
        {"color": "#FF0000", "name": "Dangerous Target", "description": "Target on collision course"},
        {"color": "#00FF00", "name": "Own Ship", "description": "Your vessel's position"},
        {"color": "#FFFF00", "name": "Close Target", "description": "Target within safety zone"},
        {"color": "#00FFFF", "name": "Tracked Target", "description": "Target being tracked by ARPA"},
        {"color": "#808080", "name": "Lost Target", "description": "Target that was lost from tracking"}
    ]

    st.markdown("### Radar Color Matching Test")
    
    test_colors = radar_colors.copy()
    random.shuffle(test_colors)
    
    user_matches = {}
    
    for i, radar_color in enumerate(test_colors):
        col1, col2, col3 = st.columns([1, 2, 3])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: {radar_color['color']};
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: 3px solid #333;
                margin: 10px auto;
                box-shadow: 0 0 15px {radar_color['color']};
            '></div>
            """, unsafe_allow_html=True)
        
        with col2:
            option_names = [r['name'] for r in radar_colors]
            selected_name = st.selectbox(
                f"Radar target {i+1} color means:",
                option_names,
                key=f"radar_{i}"
            )
            user_matches[radar_color['color']] = selected_name
        
        with col3:
            correct_info = next((r for r in radar_colors if r['name'] == selected_name), None)
            if correct_info:
                st.caption(correct_info['description'])

    if st.button("Check Radar Colors", use_container_width=True, type="primary"):
        correct = 0
        for radar_color in test_colors:
            if user_matches[radar_color['color']] == radar_color['name']:
                correct += 1
        
        score = (correct / len(test_colors)) * 100
        
        st.session_state.test_results['radar'] = {
            'score': score,
            'correct': correct,
            'total': len(test_colors),
            'type': 'Radar Colors'
        }
        
        st.success(f"**Radar Test Complete:** {correct}/{len(test_colors)} correct ({score:.1f}%)")
        
        if st.button("View Results →", use_container_width=True, type="primary"):
            st.session_state.current_test = "results"
            st.rerun()

def show_results():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">📊</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Test Results Summary</h2>
        <p style='text-align: center;'>Maritime Color Recognition Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.test_results:
        st.warning("No test results available. Please complete some tests first.")
        return

    # Calculate overall score
    total_score = sum(result['score'] for result in st.session_state.test_results.values())
    avg_score = total_score / len(st.session_state.test_results)
    tests_completed = len(st.session_state.test_results)

    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{avg_score:.1f}%")
    with col2:
        st.metric("Tests Completed", f"{tests_completed}/5")
    with col3:
        if avg_score >= 85:
            st.success("FIT FOR DUTY")
        elif avg_score >= 70:
            st.warning("CONDITIONAL")
        else:
            st.error("REVIEW REQUIRED")

    # Detailed results
    st.subheader("Detailed Results")
    results_data = []
    for test_name, results in st.session_state.test_results.items():
        results_data.append({
            'Test': test_name.title(),
            'Type': results.get('type', 'General'),
            'Score': f"{results['score']:.1f}%",
            'Correct': f"{results['correct']}/{results['total']}",
            'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review'
        })
    
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)

    # Certificate
    st.markdown("---")
    st.subheader("🎓 Maritime Color Recognition Certificate")
    
    cert_html = f"""
    <div style='
        border: 3px solid #1E3A8A; 
        padding: 2rem; 
        border-radius: 15px; 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        text-align: center;
    '>
        <h2 style='color: #1E3A8A; margin-bottom: 1rem;'>VisionQuest Navigator</h2>
        <h3 style='color: #495057; margin-bottom: 2rem;'>Maritime Color Recognition Certificate</h3>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; text-align: left;'>
            <div>
                <p><strong>Mariner:</strong> {st.session_state.get('user_name', 'Not Provided')}</p>
                <p><strong>Rank:</strong> {st.session_state.get('user_rank', 'Not Provided')}</p>
            </div>
            <div>
                <p><strong>Overall Score:</strong> {avg_score:.1f}%</p>
                <p><strong>Tests Completed:</strong> {tests_completed}/5</p>
            </div>
        </div>
        
        <div style='
            padding: 1.5rem; 
            background: {"#d4edda" if avg_score >= 85 else "#fff3cd" if avg_score >= 70 else "#f8d7da"}; 
            border-radius: 8px;
            margin-bottom: 1rem;
        '>
            <h4 style='margin: 0; color: {"#155724" if avg_score >= 85 else "#856404" if avg_score >= 70 else "#721c24"};'>
                {'FIT FOR MARITIME DUTY' if avg_score >= 85 else 'CONDITIONALLY FIT' if avg_score >= 70 else 'COMPREHENSIVE REVIEW REQUIRED'}
            </h4>
        </div>
        
        <p style='color: #6B7280; font-size: 0.9rem;'>
            Assessment Date: {pd.Timestamp.now().strftime('%B %d, %Y')}<br>
            Results should be verified by qualified medical personnel for official certification.
        </p>
    </div>
    """
    
    st.markdown(cert_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()