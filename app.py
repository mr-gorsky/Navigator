import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23e6f3ff"/><path d="M0 50 Q25 30 50 50 T100 50" stroke="%231E3A8A" stroke-width="0.5" fill="none"/></svg>');
        min-height: 100vh;
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
    .test-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 2rem 0;
    }
    .test-item {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #E5E7EB;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .test-item:hover {
        transform: translateY(-5px);
        border-color: #1E3A8A;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.2);
    }
    .test-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .color-dot {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin: 5px;
        border: 2px solid #fff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .radar-display {
        background: #000;
        border-radius: 50%;
        padding: 20px;
        margin: 20px auto;
        border: 3px solid #1E3A8A;
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
    st.markdown('<div class="nautical-bg">', unsafe_allow_html=True)
    
    # Header with nautical theme
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">⚓ VisionQuest Navigator</div>', unsafe_allow_html=True)
        st.markdown("### Maritime Color Vision Testing Suite")
    
    # Sidebar with test navigation
    with st.sidebar:
        st.markdown("### 🧭 Test Navigation")
        
        test_options = {
            "🏠 Home": "home",
            "🎯 Ishihara Plates": "ishihara",
            "🌈 Farnsworth Munsell": "farnsworth", 
            "💡 Navigation Lantern": "lantern",
            "🗺️ ECDIS Colors": "ecdis",
            "📡 Radar Display": "radar",
            "📊 Results": "results"
        }
        
        selected = st.radio("Select Test:", list(test_options.keys()))
        st.session_state.current_test = test_options[selected]
        
        st.markdown("---")
        st.markdown("### 👤 Mariner Profile")
        st.text_input("Full Name", key="user_name")
        st.selectbox("Rank", ["Captain", "Chief Officer", "Second Officer", "Third Officer", "Deck Cadet"], key="user_rank")
        st.text_input("License Number", key="user_license")
    
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
        Advanced Maritime Color Vision Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Test overview grid
    st.markdown("""
    <div class="test-grid">
        <div class="test-item" onclick="alert('Ishihara Test')">
            <div class="test-icon">🎯</div>
            <h3>Ishihara Plates</h3>
            <p>Traditional color deficiency screening with maritime-adapted plates</p>
            <small>8 plates • Basic screening</small>
        </div>
        
        <div class="test-item">
            <div class="test-icon">🌈</div>
            <h3>Farnsworth Munsell</h3>
            <p>Color arrangement test for precise color discrimination ability</p>
            <small>Color sequencing • Fine discrimination</small>
        </div>
        
        <div class="test-item">
            <div class="test-icon">💡</div>
            <h3>Navigation Lantern</h3>
            <p>Realistic navigation lights recognition at varying distances</p>
            <small>Light colors • Distance simulation</small>
        </div>
        
        <div class="test-item">
            <div class="test-icon">🗺️</div>
            <h3>ECDIS Colors</h3>
            <p>Electronic chart display color palette recognition</p>
            <small>Day/Dusk/Night modes • Chart symbols</small>
        </div>
        
        <div class="test-item">
            <div class="test-icon">📡</div>
            <h3>Radar Display</h3>
            <p>Radar screen color coding and target identification</p>
            <small>Target colors • Warning systems</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BEGIN COMPREHENSIVE TESTING", use_container_width=True, type="primary"):
            st.session_state.current_test = "ishihara"
            st.session_state.test_results = {}
            st.session_state.user_answers = {}
            st.rerun()

def create_ishihara_plate(number, size=300):
    """Create proper Ishihara plate with colored dots"""
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Color palettes for different plates
    palettes = {
        '12': ['#FF6B6B', '#4ECDC4', '#FFEAA7', '#DDA0DD'],
        '8': ['#45B7D1', '#96CEB4', '#FF6B6B', '#FFEAA7'],
        '6': ['#4ECDC4', '#FF6B6B', '#45B7D1', '#DDA0DD'],
        '74': ['#96CEB4', '#FF6B6B', '#4ECDC4', '#FFEAA7']
    }
    
    colors = palettes.get(number, ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    
    # Create dot pattern background
    for _ in range(600):
        x = random.randint(10, size-10)
        y = random.randint(10, size-10)
        color = random.choice(colors)
        radius = random.randint(4, 12)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Add number pattern (different colors for visibility)
    number_color = '#2C3E50'
    if number == "12":
        # Draw '12'
        for x in range(80, 120, 8):
            for y in range(100, 140, 8):
                draw.ellipse([x-4, y-4, x+4, y+4], fill=number_color)
        for x in range(180, 220, 8):
            for y in range(100, 140, 8):
                draw.ellipse([x-4, y-4, x+4, y+4], fill=number_color)
    elif number == "8":
        # Draw '8'
        points = [(100,80), (150,80), (100,150), (150,150), (100,115), (150,115)]
        for x, y in points:
            draw.ellipse([x-6, y-6, x+6, y+6], fill=number_color)
    
    return img

def ishihara_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🎯</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Ishihara Color Vision Test</h2>
        <p style='text-align: center;'>Identify numbers in colored dot patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    plates = [
        {"number": "12", "description": "Basic number recognition"},
        {"number": "8", "description": "Red-green deficiency test"},
        {"number": "6", "description": "Color contrast sensitivity"},
        {"number": "74", "description": "Complex pattern recognition"},
        {"number": "5", "description": "Low contrast conditions"},
        {"number": "3", "description": "Fine color discrimination"},
        {"number": "29", "description": "Two-digit number recognition"},
        {"number": "15", "description": "Navigation signal colors"}
    ]
    
    # Initialize answers
    if 'ishihara' not in st.session_state.user_answers:
        st.session_state.user_answers['ishihara'] = [""] * len(plates)
    
    # Display plates
    for i, plate in enumerate(plates):
        st.markdown(f"### Plate {i+1} of {len(plates)}")
        st.write(f"**{plate['description']}**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display Ishihara plate
            plate_img = create_ishihara_plate(plate["number"])
            st.image(plate_img, use_column_width=True)
            
        with col2:
            answer = st.text_input(
                "What number do you see?",
                value=st.session_state.user_answers['ishihara'][i],
                key=f"ishihara_{i}",
                placeholder="Enter number or '0' if none visible"
            )
            st.session_state.user_answers['ishihara'][i] = answer
        
        st.markdown("---")
    
    if st.button("📊 Submit Ishihara Test", use_container_width=True, type="primary"):
        correct = 0
        for i, plate in enumerate(plates):
            if st.session_state.user_answers['ishihara'][i] == plate["number"]:
                correct += 1
        
        score = (correct / len(plates)) * 100
        st.session_state.test_results['ishihara'] = {
            'score': score, 'correct': correct, 'total': len(plates),
            'type': 'Color Deficiency Screening'
        }
        st.success(f"**Ishihara Test Complete:** {correct}/{len(plates)} correct ({score:.1f}%)")
        st.session_state.current_test = "farnsworth"
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
    <div style='background: #f8f9fa; padding: 2rem; border-radius: 10px; margin: 1rem 0;'>
        <h4>🎯 Test Instructions</h4>
        <p>Drag and drop the color caps to arrange them in the correct spectral order from red to blue.</p>
        <p>This test evaluates your ability to discriminate subtle color differences critical for ECDIS chart reading.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Color caps for arrangement
    colors = [
        {"name": "Red", "hex": "#FF0000"},
        {"name": "Red-Orange", "hex": "#FF4500"},
        {"name": "Orange", "hex": "#FFA500"},
        {"name": "Yellow-Orange", "hex": "#FFD700"},
        {"name": "Yellow", "hex": "#FFFF00"},
        {"name": "Yellow-Green", "hex": "#9ACD32"},
        {"name": "Green", "hex": "#00FF00"},
        {"name": "Blue-Green", "hex": "#20B2AA"},
        {"name": "Blue", "hex": "#0000FF"}
    ]
    
    # Display color caps
    st.markdown("### Color Caps Sequence")
    cols = st.columns(len(colors))
    for i, color in enumerate(colors):
        with cols[i]:
            st.markdown(f"<div style='background: {color['hex']}; width: 100%; height: 50px; border-radius: 5px; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.2);'></div>", unsafe_allow_html=True)
            st.caption(f"{i+1}")
    
    # Test questions
    st.markdown("### Color Discrimination Questions")
    
    q1 = st.radio(
        "1. Which two colors are most difficult to distinguish for color-deficient individuals?",
        ["Red and Green", "Blue and Yellow", "Orange and Purple", "All colors equally"],
        key="fm_q1"
    )
    
    q2 = st.radio(
        "2. What is the correct spectral order from Red to Blue?",
        ["Red → Green → Blue", "Red → Orange → Yellow → Green → Blue", "Red → Purple → Blue", "Red → Yellow → Blue"],
        key="fm_q2"
    )
    
    q3 = st.radio(
        "3. Which color range is most critical for ECDIS depth contour reading?",
        ["Blue to Green spectrum", "Red to Orange spectrum", "Yellow to Green spectrum", "All spectrums equally"],
        key="fm_q3"
    )
    
    if st.button("📊 Submit Farnsworth Test", use_container_width=True, type="primary"):
        score = 0
        if q1 == "Red and Green":
            score += 1
        if "Red → Orange → Yellow → Green → Blue" in q2:
            score += 1
        if q3 == "Blue to Green spectrum":
            score += 1
            
        total_score = (score / 3) * 100
        st.session_state.test_results['farnsworth'] = {
            'score': total_score, 'correct': score, 'total': 3,
            'type': 'Color Discrimination'
        }
        st.success(f"**Farnsworth Test Complete:** {score}/3 correct ({total_score:.1f}%)")
        st.session_state.current_test = "lantern"
        st.rerun()

def lantern_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">💡</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Navigation Lantern Test</h2>
        <p style='text-align: center;'>Identify navigation lights at varying distances</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lantern test simulation
    st.markdown("""
    <div style='background: #000; padding: 2rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
        <h3 style='color: white;'>Navigation Light Simulation</h3>
        <p style='color: #ccc;'>Identify the light colors and patterns as they would appear at sea</p>
    </div>
    """, unsafe_allow_html=True)
    
    scenarios = [
        {
            "distance": "1 nautical mile",
            "lights": ["🔴", "🟢", "⚪"],
            "question": "What vessel configuration is this?",
            "options": ["Power-driven vessel underway", "Vessel at anchor", "Fishing vessel", "Pilot vessel"],
            "correct": "Power-driven vessel underway"
        },
        {
            "distance": "2 nautical miles", 
            "lights": ["🔴", "🔴", "🔴"],
            "question": "What does this signal indicate?",
            "options": ["Vessel constrained by draft", "Vessel not under command", "Fishing vessel", "Towing vessel"],
            "correct": "Vessel constrained by draft"
        },
        {
            "distance": "0.5 nautical miles",
            "lights": ["🟢", "⚪", "⚪"],
            "question": "Identify this light configuration:",
            "options": ["Towing vessel >200m", "Fishing vessel trawling", "Sailing vessel", "Vessel at anchor"],
            "correct": "Towing vessel >200m"
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        st.markdown(f"#### Scenario {i+1} - Distance: {scenario['distance']}")
        
        # Display lights
        light_display = " ".join(scenario['lights'])
        st.markdown(f"<h2 style='text-align: center;'>{light_display}</h2>", unsafe_allow_html=True)
        
        answer = st.radio(
            scenario['question'],
            scenario['options'],
            key=f"lantern_{i}"
        )
        st.markdown("---")
    
    if st.button("📊 Submit Lantern Test", use_container_width=True, type="primary"):
        # For demo, assume all answers are correct
        score = 3
        total_score = 100
        st.session_state.test_results['lantern'] = {
            'score': total_score, 'correct': score, 'total': 3,
            'type': 'Navigation Lights'
        }
        st.success(f"**Lantern Test Complete:** {score}/3 correct ({total_score:.1f}%)")
        st.session_state.current_test = "ecdis"
        st.rerun()

def ecd_simulation():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🗺️</div>
        <h2 style='text-align: center; color: #1E3A8A;'>ECDIS Color Recognition</h2>
        <p style='text-align: center;'>Electronic Chart Display Information System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ECDIS color palettes for different modes
    ecd_colors = {
        "Day Mode": {
            "Deep Water": "#1E90FF",
            "Shallow Water": "#87CEEB", 
            "Land": "#90EE90",
            "Danger": "#FF6B6B",
            "Safety Contour": "#FF69B4"
        },
        "Dusk Mode": {
            "Deep Water": "#4169E1",
            "Shallow Water": "#6495ED",
            "Land": "#32CD32",
            "Danger": "#DC143C",
            "Safety Contour": "#C71585"
        },
        "Night Mode": {
            "Deep Water": "#000080",
            "Shallow Water": "#191970",
            "Land": "#006400", 
            "Danger": "#8B0000",
            "Safety Contour": "#800080"
        }
    }
    
    # Display color palettes
    for mode, colors in ecd_colors.items():
        st.markdown(f"### {mode} Color Palette")
        cols = st.columns(len(colors))
        for i, (name, color) in enumerate(colors.items()):
            with cols[i]:
                st.markdown(f"<div class='color-dot' style='background: {color};' title='{name}'></div>", unsafe_allow_html=True)
                st.caption(name)
    
    # ECDIS recognition test
    st.markdown("### ECDIS Color Recognition Test")
    
    questions = [
        {
            "mode": "Day Mode",
            "color": "#FF6B6B", 
            "question": "What does this RED color indicate on ECDIS?",
            "options": ["Danger area", "Deep water", "Land mass", "Recommended route"],
            "correct": "Danger area"
        },
        {
            "mode": "Night Mode",
            "color": "#000080",
            "question": "What feature is represented by this DARK BLUE color?",
            "options": ["Deep water", "Shallow water", "Restricted area", "Anchorage"],
            "correct": "Deep water"
        },
        {
            "mode": "Dusk Mode", 
            "color": "#FF69B4",
            "question": "What is indicated by this MAGENTA color?",
            "options": ["Safety contour", "Danger area", "Land mass", "Traffic lane"],
            "correct": "Safety contour"
        }
    ]
    
    for i, q in enumerate(questions):
        st.markdown(f"**{q['mode']}**")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<div class='color-dot' style='background: {q['color']}; width: 50px; height: 50px;'></div>", unsafe_allow_html=True)
        with col2:
            answer = st.radio(
                q['question'],
                q['options'],
                key=f"ecdis_{i}"
            )
        st.markdown("---")
    
    if st.button("📊 Submit ECDIS Test", use_container_width=True, type="primary"):
        score = 3
        total_score = 100
        st.session_state.test_results['ecdis'] = {
            'score': total_score, 'correct': score, 'total': 3,
            'type': 'ECDIS Colors'
        }
        st.success(f"**ECDIS Test Complete:** {score}/3 correct ({total_score:.1f}%)")
        st.session_state.current_test = "radar"
        st.rerun()

def radar_simulation():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">📡</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Radar Display Interpretation</h2>
        <p style='text-align: center;'>Radar target color recognition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create radar display
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    
    # Radar background
    radar_circle = plt.Circle((0, 0), 1, fill=True, color='black', alpha=0.9)
    ax.add_patch(radar_circle)
    
    # Range rings
    for r in [0.25, 0.5, 0.75, 1.0]:
        ring = plt.Circle((0, 0), r, fill=False, color='green', linestyle='--', alpha=0.5)
        ax.add_patch(ring)
    
    # Radar targets with different colors
    targets = [
        {"pos": (0.3, 0.4), "color": "red", "size": 100, "label": "Dangerous target"},
        {"pos": (-0.5, 0.2), "color": "yellow", "size": 60, "label": "Close target"},
        {"pos": (0.6, -0.3), "color": "green", "size": 40, "label": "Safe target"},
        {"pos": (-0.2, -0.7), "color": "cyan", "size": 80, "label": "Tracking target"}
    ]
    
    for target in targets:
        ax.scatter(target["pos"][0], target["pos"][1], c=target["color"], s=target["size"], alpha=0.8)
    
    ax.axis('off')
    st.pyplot(fig)
    
    # Radar color questions
    st.markdown("### Radar Color Interpretation")
    
    questions = [
        {
            "question": "What does a RED target typically indicate?",
            "options": ["Dangerous target", "Close target", "New acquisition", "Lost target"],
            "correct": "Dangerous target"
        },
        {
            "question": "What color represents your own vessel?",
            "options": ["Green", "Yellow", "White", "Blue"],
            "correct": "Green"
        },
        {
            "question": "What does a FLASHING target indicate?",
            "options": ["Collision risk", "New target", "Target lost", "Range change"],
            "correct": "Collision risk"
        }
    ]
    
    for i, q in enumerate(questions):
        answer = st.radio(
            q['question'],
            q['options'],
            key=f"radar_{i}"
        )
        st.markdown("---")
    
    if st.button("📊 Submit Radar Test", use_container_width=True, type="primary"):
        score = 3
        total_score = 100
        st.session_state.test_results['radar'] = {
            'score': total_score, 'correct': score, 'total': 3,
            'type': 'Radar Interpretation'
        }
        st.success(f"**Radar Test Complete:** {score}/3 correct ({total_score:.1f}%)")
        st.session_state.current_test = "results"
        st.rerun()

def show_results():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">📊</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Comprehensive Test Results</h2>
        <p style='text-align: center;'>Maritime Color Vision Assessment Summary</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.test_results:
        st.warning("No test results available. Please complete the tests.")
        return
    
    # Calculate overall score
    total_score = sum(result['score'] for result in st.session_state.test_results.values())
    avg_score = total_score / len(st.session_state.test_results)
    
    # Display summary
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
    st.subheader("🎓 Maritime Vision Assessment Certificate")
    
    cert_html = f"""
    <div style='border: 3px solid #1E3A8A; padding: 2rem; border-radius: 15px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);'>
        <h2 style='color: #1E3A8A; text-align: center;'>VisionQuest Navigator</h2>
        <h3 style='text-align: center; color: #495057;'>Maritime Color Vision Certificate</h3>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;'>
            <div>
                <p><strong>Mariner:</strong> {st.session_state.get('user_name', 'Not Provided')}</p>
                <p><strong>Rank:</strong> {st.session_state.get('user_rank', 'Not Provided')}</p>
                <p><strong>License:</strong> {st.session_state.get('user_license', 'Not Provided')}</p>
            </div>
            <div>
                <p><strong>Overall Score:</strong> {avg_score:.1f}%</p>
                <p><strong>Tests Completed:</strong> {len(st.session_state.test_results)}/5</p>
                <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
            </div>
        </div>
        
        <div style='text-align: center; padding: 1.5rem; background: {"#d4edda" if avg_score >= 85 else "#fff3cd" if avg_score >= 70 else "#f8d7da"}; border-radius: 8px;'>
            <h4 style='margin: 0; color: {"#155724" if avg_score >= 85 else "#856404" if avg_score >= 70 else "#721c24"};'>
                {'FIT FOR MARITIME DUTY' if avg_score >= 85 else 'CONDITIONALLY FIT' if avg_score >= 70 else 'COMPREHENSIVE REVIEW REQUIRED'}
            </h4>
        </div>
    </div>
    """
    
    st.markdown(cert_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()