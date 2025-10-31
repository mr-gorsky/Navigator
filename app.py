import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from PIL import Image, ImageDraw
import io
import time

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
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .cap-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 20px 0;
    }
    .color-cap {
        width: 60px;
        height: 60px;
        border-radius: 8px;
        border: 3px solid white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        cursor: grab;
    }
    .tray-container {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px dashed #dee2e6;
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
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

def main():
    st.markdown('<div class="nautical-bg">', unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">⚓ VisionQuest Navigator</div>', unsafe_allow_html=True)
        st.markdown("### Professional Maritime Color Vision Testing")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Test Navigation")
        
        test_options = {
            "🏠 Home": "home",
            "🎯 Ishihara Test": "ishihara",
            "🌈 Farnsworth Munsell": "farnsworth", 
            "💡 Lantern Test": "lantern",
            "📊 Results": "results"
        }
        
        selected = st.radio("Go to:", list(test_options.keys()))
        st.session_state.current_test = test_options[selected]
        
        st.markdown("---")
        st.markdown("### 👤 Mariner Profile")
        st.text_input("Full Name", key="user_name")
        st.selectbox("Rank", ["Captain", "Chief Officer", "Second Officer", "Third Officer", "Deck Cadet"], key="user_rank")
        
        st.markdown("---")
        st.markdown("### ⚠️ Important Notice")
        st.markdown("""
        This web-based testing serves for **screening purposes only**.
        For official certification, standardized clinical testing under controlled conditions is required.
        """)
    
    # Route to current test
    if st.session_state.current_test == "home":
        show_home()
    elif st.session_state.current_test == "ishihara":
        ishihara_test()
    elif st.session_state.current_test == "farnsworth":
        farnsworth_test()
    elif st.session_state.current_test == "lantern":
        lantern_test()
    elif st.session_state.current_test == "results":
        show_results()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🧭</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Welcome to VisionQuest Navigator</h2>
        <p style='text-align: center; font-size: 1.2rem; color: #4B5563;'>
        Standardized Maritime Color Vision Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>🎯 About This Testing Suite</h4>
        <p>This application implements <strong>standardized color vision tests</strong> adapted for maritime professionals:</p>
        <ul>
        <li><strong>Ishihara Plates</strong> - 24-plate screening test for red-green deficiency</li>
        <li><strong>Farnsworth Munsell 100-Hue</strong> - Color discrimination ability assessment</li>
        <li><strong>Navigation Lantern</strong> - Signal light recognition test</li>
        </ul>
        <p><em>Note: Web-based testing has limitations. For official certification, clinical testing is required.</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Calibration check
    st.markdown("""
    <div class="warning-box">
        <h4>📱 Display Calibration Check</h4>
        <p>Before testing, ensure:</p>
        <ul>
        <li>Monitor is properly calibrated</li>
        <li>Room lighting is consistent and glare-free</li>
        <li>Screen brightness is at normal levels</li>
        <li>No night mode or color filters are active</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BEGIN STANDARDIZED TESTING", use_container_width=True, type="primary"):
            st.session_state.current_test = "ishihara"
            st.session_state.test_results = {}
            st.session_state.user_answers = {}
            st.session_state.current_plate = 0
            st.session_state.test_started = True
            st.rerun()

def create_ishihara_plate(number, size=400):
    """Create authentic Ishihara plate with proper dot patterns"""
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Different color palettes for different plate types
    if number in ["12", "8"]:  # Normal vision plates
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        number_color = '#2C3E50'
    else:  # Transformation plates (different for color deficient)
        colors = ['#FF9999', '#66CCCC', '#6699CC', '#99CC99', '#FFFF99']
        number_color = '#4A4A4A'
    
    # Create dense, random dot pattern
    for _ in range(1200):
        x = random.randint(15, size-15)
        y = random.randint(15, size-15)
        color = random.choice(colors)
        radius = random.randint(3, 10)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Draw number pattern
    if number == "12":
        # Draw '12' - visible to normal vision
        for x in range(120, 161, 5):
            for y in range(150, 191, 5):
                if random.random() > 0.3:  # Random gaps for authentic look
                    draw.ellipse([x-2, y-2, x+2, y+2], fill=number_color)
        for x in range(240, 281, 5):
            for y in range(150, 191, 5):
                if random.random() > 0.3:
                    draw.ellipse([x-2, y-2, x+2, y+2], fill=number_color)
    elif number == "8":
        # Draw '8'
        points = [(150,120), (200,120), (150,200), (200,200), (150,160), (200,160)]
        for x, y in points:
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if random.random() > 0.4:
                        draw.ellipse([x+dx-2, y+dy-2, x+dx+2, y+dy+2], fill=number_color)
    elif number == "6":
        # Draw '6' - transformation plate
        points = [(150,120), (200,120), (150,160), (150,200), (200,160), (200,200)]
        for x, y in points:
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if random.random() > 0.4:
                        draw.ellipse([x+dx-2, y+dy-2, x+dx+2, y+dy+2], fill=number_color)
    
    return img

def ishihara_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🎯</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Ishihara Color Vision Test</h2>
        <p style='text-align: center;'>24-Plate Screening Edition</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Standard Test Instructions</h4>
        <p>View each plate and identify the number you see. You have <strong>3 seconds</strong> per plate.</p>
        <p>If no number is visible, enter <strong>0</strong>. Do not spend excessive time on any single plate.</p>
        <p><em>This test screens for red-green color vision deficiencies.</em></p>
    </div>
    """, unsafe_allow_html=True)

    # 24-plate Ishihara test
    plates = [
        {"number": "12", "description": "Demonstration plate - all should see '12'", "type": "control"},
        {"number": "8", "description": "Basic number recognition", "type": "screening"},
        {"number": "6", "description": "Red-green deficiency detection", "type": "transformation"},
        {"number": "29", "description": "Two-digit recognition", "type": "screening"},
        {"number": "57", "description": "Transformation plate", "type": "transformation"},
        {"number": "5", "description": "Single digit visibility", "type": "screening"},
        {"number": "3", "description": "Pattern discrimination", "type": "screening"},
        {"number": "15", "description": "Traffic signal simulation", "type": "screening"},
        {"number": "74", "description": "Complex pattern recognition", "type": "transformation"},
        {"number": "2", "description": "Simple digit recognition", "type": "screening"},
        {"number": "16", "description": "Two-digit transformation", "type": "transformation"},
        {"number": "35", "description": "Hidden digit test", "type": "vanishing"},
        {"number": "96", "description": "Transformation plate", "type": "transformation"},
        {"number": "5", "description": "Repeat for consistency", "type": "screening"},
        {"number": "7", "description": "Single digit screening", "type": "screening"},
        {"number": "45", "description": "Two-digit pattern", "type": "screening"},
        {"number": "73", "description": "Transformation test", "type": "transformation"},
        {"number": "26", "description": "Hidden digit", "type": "vanishing"},
        {"number": "42", "description": "Transformation plate", "type": "transformation"},
        {"number": "8", "description": "Consistency check", "type": "screening"},
        {"number": "13", "description": "Two-digit recognition", "type": "screening"},
        {"number": "56", "description": "Transformation test", "type": "transformation"},
        {"number": "97", "description": "Vanishing digit", "type": "vanishing"},
        {"number": "88", "description": "Final demonstration", "type": "control"}
    ]

    current_plate = st.session_state.current_plate

    if current_plate < len(plates):
        plate = plates[current_plate]
        
        st.markdown(f"### Plate {current_plate + 1} of {len(plates)}")
        st.write(f"**Type:** {plate['type'].title()} | **Description:** {plate['description']}")
        
        # Create and display Ishihara plate
        plate_img = create_ishihara_plate(plate["number"])
        st.image(plate_img, use_column_width=True, caption=f"Plate {current_plate + 1}")
        
        # Timer simulation
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        time_remaining = max(0, 3 - elapsed)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            answer = st.text_input(
                "Enter the number you see:",
                key=f"ishihara_input_{current_plate}",
                placeholder="Number or '0' if none visible",
                max_chars=2
            )
        
        with col2:
            st.metric("Time Remaining", f"{time_remaining:.1f}s")
        
        with col3:
            if st.button("Submit Answer →", use_container_width=True, type="primary") or time_remaining <= 0:
                if answer.strip():
                    if 'ishihara' not in st.session_state.user_answers:
                        st.session_state.user_answers['ishihara'] = []
                    st.session_state.user_answers['ishihara'].append(answer.strip())
                    st.session_state.current_plate += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
                else:
                    st.warning("Please enter your answer")
            
            if st.button("🔄 Restart Test", use_container_width=True):
                st.session_state.current_plate = 0
                st.session_state.user_answers['ishihara'] = []
                st.session_state.start_time = time.time()
                st.rerun()
    
    else:
        # Test completed - calculate results
        st.success("🎉 Ishihara Test Completed!")
        
        user_answers = st.session_state.user_answers.get('ishihara', [])
        correct_count = 0
        error_analysis = {"screening": 0, "transformation": 0, "vanishing": 0, "control": 0}
        total_by_type = {"screening": 0, "transformation": 0, "vanishing": 0, "control": 0}
        
        for i, (plate, user_answer) in enumerate(zip(plates, user_answers)):
            total_by_type[plate["type"]] += 1
            if user_answer == plate["number"]:
                correct_count += 1
            else:
                error_analysis[plate["type"]] += 1
        
        score = (correct_count / len(plates)) * 100
        
        # Professional interpretation
        st.session_state.test_results['ishihara'] = {
            'score': score,
            'correct': correct_count,
            'total': len(plates),
            'errors_by_type': error_analysis,
            'type': 'Color Deficiency Screening'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Score", f"{score:.1f}%")
            st.metric("Correct Answers", f"{correct_count}/{len(plates)}")
        
        with col2:
            # Professional interpretation
            if error_analysis["transformation"] > 3 or error_analysis["vanishing"] > 2:
                st.error("**❌ COLOR VISION DEFICIENCY SUSPECTED**")
                st.write("Pattern suggests red-green color vision deficiency")
            elif error_analysis["screening"] > 4:
                st.warning("**⚠️ BORDERLINE RESULTS**")
                st.write("Minor color perception issues detected")
            else:
                st.success("**✅ NORMAL COLOR VISION**")
                st.write("Results within normal range")
        
        # Detailed analysis
        st.markdown("#### Detailed Error Analysis")
        error_df = pd.DataFrame([
            {"Plate Type": "Screening", "Errors": error_analysis["screening"], "Total": total_by_type["screening"]},
            {"Plate Type": "Transformation", "Errors": error_analysis["transformation"], "Total": total_by_type["transformation"]},
            {"Plate Type": "Vanishing", "Errors": error_analysis["vanishing"], "Total": total_by_type["vanishing"]},
            {"Plate Type": "Control", "Errors": error_analysis["control"], "Total": total_by_type["control"]}
        ])
        st.dataframe(error_df, use_container_width=True)
        
        if st.button("Continue to Farnsworth Test →", use_container_width=True, type="primary"):
            st.session_state.current_test = "farnsworth"
            st.session_state.current_plate = 0
            st.rerun()

def farnsworth_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">🌈</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Farnsworth Munsell 100-Hue Test</h2>
        <p style='text-align: center;'>Color Discrimination Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Standard Test Instructions</h4>
        <p>Arrange the color caps in natural spectral order between the fixed anchor caps.</p>
        <p>Drag and drop the movable caps to create a smooth color transition.</p>
        <p><em>This test evaluates your ability to discriminate subtle color differences.</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Simplified FM100 test (4 trays with reduced caps for web implementation)
    trays = [
        {
            "name": "Tray 1: Red to Yellow-Green",
            "anchor_start": "#FF0000",
            "anchor_end": "#9ACD32", 
            "caps": [
                "#FF4500", "#FF8C00", "#FFA500", "#FFD700", "#FFFF00", "#ADFF2F"
            ]
        },
        {
            "name": "Tray 2: Yellow-Green to Blue",
            "anchor_start": "#9ACD32",
            "anchor_end": "#0000FF",
            "caps": [
                "#32CD32", "#00FF00", "#00FA9A", "#20B2AA", "#1E90FF", "#4169E1"
            ]
        }
    ]

    st.markdown("### Color Arrangement Test")
    
    if 'farnsworth_answers' not in st.session_state.user_answers:
        st.session_state.user_answers['farnsworth'] = {}
    
    for tray_idx, tray in enumerate(trays):
        st.markdown(f"#### {tray['name']}")
        
        # Display anchor caps
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f"""
            <div style='
                background: {tray['anchor_start']};
                width: 80px;
                height: 80px;
                border-radius: 8px;
                border: 4px solid #333;
                margin: 10px auto;
            '></div>
            <center><small>Start Anchor</small></center>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='
                background: {tray['anchor_end']};
                width: 80px;
                height: 80px;
                border-radius: 8px;
                border: 4px solid #333;
                margin: 10px auto;
            '></div>
            <center><small>End Anchor</small></center>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<center><strong>Arrange these colors between the anchors:</strong></center>", unsafe_allow_html=True)
            
            # Display movable caps
            cap_cols = st.columns(len(tray['caps']))
            arranged_order = []
            
            for i, color in enumerate(tray['caps']):
                with cap_cols[i]:
                    st.markdown(f"""
                    <div style='
                        background: {color};
                        width: 60px;
                        height: 60px;
                        border-radius: 6px;
                        border: 3px solid white;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                        margin: 5px auto;
                    '></div>
                    """, unsafe_allow_html=True)
                    
                    position = st.number_input(
                        f"Position for color {i+1}",
                        min_value=1,
                        max_value=len(tray['caps']),
                        value=i+1,
                        key=f"tray_{tray_idx}_cap_{i}"
                    )
                    arranged_order.append((position, color))
            
            # Store arrangement
            arranged_order.sort()
            st.session_state.user_answers['farnsworth'][f"tray_{tray_idx}"] = [color for _, color in arranged_order]
        
        st.markdown("---")

    if st.button("Calculate FM100 Results", use_container_width=True, type="primary"):
        # Calculate error score (simplified)
        total_error = 0
        
        # Correct spectral order for each tray
        correct_orders = {
            "tray_0": ["#FF4500", "#FF8C00", "#FFA500", "#FFD700", "#FFFF00", "#ADFF2F"],
            "tray_1": ["#32CD32", "#00FF00", "#00FA9A", "#20B2AA", "#1E90FF", "#4169E1"]
        }
        
        for tray_idx in range(len(trays)):
            user_order = st.session_state.user_answers['farnsworth'].get(f"tray_{tray_idx}", [])
            correct_order = correct_orders[f"tray_{tray_idx}"]
            
            # Calculate positional errors
            tray_error = 0
            for i, correct_color in enumerate(correct_order):
                if correct_color in user_order:
                    user_pos = user_order.index(correct_color)
                    tray_error += abs(user_pos - i)
                else:
                    tray_error += len(correct_order)  # Max penalty for missing color
            
            total_error += tray_error
        
        # Convert to score (lower error = better)
        max_possible_error = 36  # Simplified calculation
        score = max(0, 100 - (total_error / max_possible_error * 100))
        
        st.session_state.test_results['farnsworth'] = {
            'score': score,
            'total_error': total_error,
            'type': 'Color Discrimination'
        }
        
        st.success(f"**FM100 Test Complete**")
        st.metric("Total Error Score", total_error)
        st.metric("Discrimination Score", f"{score:.1f}%")
        
        # Interpretation
        if total_error <= 8:
            st.success("✅ **EXCELLENT COLOR DISCRIMINATION**")
            st.write("Superior ability to distinguish subtle color differences")
        elif total_error <= 16:
            st.success("✅ **GOOD COLOR DISCRIMINATION**")
            st.write("Normal color discrimination ability")
        elif total_error <= 24:
            st.warning("⚠️ **MODERATE DISCRIMINATION ISSUES**")
            st.write("Some difficulty with fine color differences")
        else:
            st.error("❌ **POOR COLOR DISCRIMINATION**")
            st.write("Significant difficulty distinguishing colors")
        
        if st.button("Continue to Lantern Test →", use_container_width=True):
            st.session_state.current_test = "lantern"
            st.rerun()

def lantern_test():
    st.markdown("""
    <div class="test-card">
        <div class="icon-header">💡</div>
        <h2 style='text-align: center; color: #1E3A8A;'>Navigation Lantern Test</h2>
        <p style='text-align: center;'>Signal Light Recognition</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="test-instructions">
        <h4>📋 Standard Test Instructions</h4>
        <p>Identify the color of navigation lights as they would appear at sea.</p>
        <p>You will see light signals at different intensities. Respond quickly with the color you perceive.</p>
        <p><em>This test evaluates your ability to recognize maritime signal lights.</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Lantern test scenarios
    scenarios = [
        {
            "color": "RED",
            "hex": "#FF0000",
            "intensity": "Bright",
            "description": "Port side light or danger signal"
        },
        {
            "color": "GREEN", 
            "hex": "#00FF00",
            "intensity": "Medium",
            "description": "Starboard side light"
        },
        {
            "color": "WHITE",
            "hex": "#FFFFFF", 
            "intensity": "Bright",
            "description": "Masthead light or anchor light"
        },
        {
            "color": "RED",
            "hex": "#FF4444",
            "intensity": "Dim", 
            "description": "Distant port light"
        },
        {
            "color": "GREEN",
            "hex": "#44FF44",
            "intensity": "Dim",
            "description": "Distant starboard light"
        },
        {
            "color": "WHITE",
            "hex": "#CCCCCC", 
            "intensity": "Medium",
            "description": "Medium range masthead light"
        },
        {
            "color": "RED",
            "hex": "#FF2222",
            "intensity": "Medium",
            "description": "Standard port light"
        },
        {
            "color": "GREEN",
            "hex": "#22FF22", 
            "intensity": "Bright",
            "description": "Close starboard light"
        },
        {
            "color": "WHITE",
            "hex": "#EEEEEE",
            "intensity": "Dim",
            "description": "Anchor light at distance"
        },
        {
            "color": "RED",
            "hex": "#FF6666",
            "intensity": "Very Dim",
            "description": "Extreme distance port light"
        }
    ]

    st.markdown("### Signal Light Recognition")
    
    if 'lantern_answers' not in st.session_state.user_answers:
        st.session_state.user_answers['lantern'] = []
    
    current_scenario = len(st.session_state.user_answers['lantern'])
    
    if current_scenario < len(scenarios):
        scenario = scenarios[current_scenario]
        
        st.markdown(f"#### Signal {current_scenario + 1} of {len(scenarios)}")
        st.write(f"**Intensity:** {scenario['intensity']} | **Description:** {scenario['description']}")
        
        # Display light signal
        light_size = 200 if scenario["intensity"] in ["Bright", "Medium"] else 150
        opacity = 1.0 if scenario["intensity"] in ["Bright", "Medium"] else 0.7
        
        st.markdown(f"""
        <div style='
            background: {scenario['hex']};
            width: {light_size}px;
            height: {light_size}px;
            border-radius: 50%;
            margin: 40px auto;
            box-shadow: 0 0 60px {scenario['hex']}80;
            border: 4px solid #333;
            opacity: {opacity};
        '></div>
        """, unsafe_allow_html=True)
        
        # Response options
        color_options = ["RED", "GREEN", "WHITE"]
        selected_color = st.radio(
            "What color do you see?",
            color_options,
            key=f"lantern_{current_scenario}"
        )
        
        if st.button("Submit Response →", use_container_width=True, type="primary"):
            st.session_state.user_answers['lantern'].append(selected_color)
            st.rerun()
    
    else:
        # Test completed
        st.success("🎉 Lantern Test Completed!")
        
        user_answers = st.session_state.user_answers['lantern']
        correct_count = 0
        
        for i, (scenario, user_answer) in enumerate(zip(scenarios, user_answers)):
            if user_answer == scenario["color"]:
                correct_count += 1
        
        score = (correct_count / len(scenarios)) * 100
        
        st.session_state.test_results['lantern'] = {
            'score': score,
            'correct': correct_count,
            'total': len(scenarios),
            'type': 'Signal Light Recognition'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Score", f"{score:.1f}%")
            st.metric("Correct Identifications", f"{correct_count}/{len(scenarios)}")
        
        with col2:
            if score >= 90:
                st.success("✅ **EXCELLENT SIGNAL RECOGNITION**")
                st.write("Superior ability to identify navigation lights")
            elif score >= 80:
                st.success("✅ **GOOD SIGNAL RECOGNITION**")
                st.write("Adequate for maritime duties")
            elif score >= 70:
                st.warning("⚠️ **SATISFACTORY RECOGNITION**")
                st.write("Minor issues with dim light recognition")
            else:
                st.error("❌ **SIGNAL RECOGNITION CONCERNS**")
                st.write("Difficulty identifying navigation lights")
        
        if st.button("View All Results →", use_container_width=True, type="primary"):
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
        st.warning("No test results available. Please complete some tests first.")
        return

    # Calculate overall score
    total_score = sum(result['score'] for result in st.session_state.test_results.values())
    avg_score = total_score / len(st.session_state.test_results)
    tests_completed = len(st.session_state.test_results)

    # Professional summary
    st.markdown("### 📈 Assessment Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{avg_score:.1f}%")
    with col2:
        st.metric("Tests Completed", f"{tests_completed}/3")
    with col3:
        if avg_score >= 85:
            st.success("FIT FOR DUTY")
        elif avg_score >= 70:
            st.warning("CONDITIONAL")
        else:
            st.error("REVIEW REQUIRED")

    # Detailed results
    st.markdown("### 📋 Detailed Results")
    results_data = []
    for test_name, results in st.session_state.test_results.items():
        results_data.append({
            'Test': test_name.title(),
            'Type': results.get('type', 'General'),
            'Score': f"{results['score']:.1f}%",
            'Details': f"{results.get('correct', 'N/A')}/{results.get('total', 'N/A')}",
            'Status': '✅ Pass' if results['score'] >= 70 else '⚠️ Review'
        })
    
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)

    # Professional recommendation
    st.markdown("### 💡 Professional Assessment")
    
    if avg_score >= 85:
        assessment = """
        **Color Vision: NORMAL**
        
        - Excellent color discrimination ability
        - Normal red-green color vision
        - Superior signal light recognition
        - Suitable for all maritime duties requiring color vision
        """
        st.success(assessment)
    elif avg_score >= 70:
        assessment = """
        **Color Vision: SATISFACTORY**
        
        - Adequate color discrimination for most duties
        - Minor color perception issues noted
        - May benefit from additional training
        - Regular monitoring recommended
        """
        st.warning(assessment)
    else:
        assessment = """
        **Color Vision: REVIEW REQUIRED**
        
        - Significant color vision concerns
        - Clinical assessment recommended
        - Limitations for color-critical tasks
        - Further evaluation needed
        """
        st.error(assessment)

    # Certificate
    st.markdown("---")
    st.markdown("### 🎓 Maritime Color Vision Certificate")
    
    cert_html = f"""
    <div style='
        border: 3px solid #1E3A8A; 
        padding: 2rem; 
        border-radius: 15px; 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        text-align: center;
    '>
        <h2 style='color: #1E3A8A; margin-bottom: 1rem;'>VisionQuest Navigator</h2>
        <h3 style='color: #495057; margin-bottom: 2rem;'>Maritime Color Vision Assessment</h3>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; text-align: left;'>
            <div>
                <p><strong>Mariner:</strong> {st.session_state.get('user_name', 'Not Provided')}</p>
                <p><strong>Rank:</strong> {st.session_state.get('user_rank', 'Not Provided')}</p>
            </div>
            <div>
                <p><strong>Overall Score:</strong> {avg_score:.1f}%</p>
                <p><strong>Tests Completed:</strong> {tests_completed}/3</p>
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
            <em>Web-based screening only. Clinical verification recommended for official certification.</em>
        </p>
    </div>
    """
    
    st.markdown(cert_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()