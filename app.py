import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

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
    .banner-container {
        width: 100%;
        margin-bottom: 2rem;
    }
    .banner-image {
        width: 100%;
        border-radius: 10px;
    }
    .test-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 6px solid #1E3A8A;
    }
    .warning-box {
        background-color: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_test' not in st.session_state:
    st.session_state.current_test = "home"
if 'ishihara_answers' not in st.session_state:
    st.session_state.ishihara_answers = []
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}

def main():
    # Header with Banner
    st.markdown("""
    <div class="banner-container">
        <img src="https://i.postimg.cc/fbcrnNXC/Gemini-Generated-Image-6gukqc6gukqc6guk.png" class="banner-image">
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🧭 Navigation")
        
        menu_options = {
            "🏠 Home": "home",
            "🎯 Ishihara Test": "ishihara", 
            "🌈 Farnsworth Test": "farnsworth",
            "💡 Lantern Test": "lantern",
            "📊 Results": "results"
        }
        
        selected = st.selectbox("Go to:", list(menu_options.keys()))
        st.session_state.current_test = menu_options[selected]
        
        st.markdown("---")
        st.title("👤 Mariner Info")
        st.text_input("Full Name", key="user_name")
        st.selectbox("Rank", ["Captain", "Officer", "Cadet", "Other"], key="user_rank")

    # Display current test
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

def show_home():
    st.markdown("""
    <div class="test-container">
        <h2>🚢 Welcome to VisionQuest Navigator</h2>
        <p><strong>Comprehensive Maritime Vision Testing Suite</strong></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="test-container">
            <h3>Why This Testing Matters</h3>
            <p>Traditional Ishihara tests alone are insufficient for maritime professionals. 
            Modern navigation requires accurate color perception in various conditions:</p>
            <ul>
            <li><strong>ECDIS displays</strong> with specialized color palettes</li>
            <li><strong>Navigation lights</strong> recognition at distance</li>
            <li><strong>Radar displays</strong> with color-coded targets</li>
            <li><strong>Buoy identification</strong> in different lighting conditions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="test-container">
            <h3>Testing Protocol</h3>
            <ol>
            <li>Complete all tests in sequence</li>
            <li>Ensure proper lighting conditions</li>
            <li>Maintain normal viewing distance</li>
            <li>Do not adjust screen colors</li>
            <li>Record your results for review</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Important:</strong> Use a calibrated monitor in controlled lighting for accurate results.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 START TESTING", type="primary", use_container_width=True):
        st.session_state.current_test = "ishihara"
        st.session_state.ishihara_answers = []
        st.rerun()

def ishihara_test():
    st.markdown("""
    <div class="test-container">
        <h2>🎯 Ishihara Color Vision Test</h2>
        <p><strong>Instructions:</strong> Identify the numbers you see in each circle. Type the number or '0' if no number visible.</p>
    </div>
    """, unsafe_allow_html=True)

    # Ishihara plates
    plates = [
        {"number": "12", "description": "Basic number recognition"},
        {"number": "8", "description": "Red-green detection"}, 
        {"number": "6", "description": "Color contrast"},
        {"number": "29", "description": "Two-digit number"},
        {"number": "5", "description": "Low contrast"},
        {"number": "3", "description": "Pattern recognition"}
    ]

    # Display current plate
    if len(st.session_state.ishihara_answers) < len(plates):
        current_idx = len(st.session_state.ishihara_answers)
        plate = plates[current_idx]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create Ishihara-like circle
            fig, ax = plt.subplots(figsize=(6, 6))
            
            # Create colored dots background
            for i in range(500):
                x, y = random.uniform(0, 10), random.uniform(0, 10)
                color = random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
                size = random.randint(10, 40)
                ax.scatter(x, y, c=color, s=size, alpha=0.7)
            
            # Add number pattern (simplified)
            if plate["number"] == "12":
                # Add dots to form '12'
                ax.scatter([3,4,6,7], [7,7,7,7], c='#2C3E50', s=100, alpha=0.9)
                ax.scatter([3,4,6,7], [6,6,6,6], c='#2C3E50', s=100, alpha=0.9)
            elif plate["number"] == "8":
                # Add dots to form '8'
                ax.scatter([4,5,6,4,6,4,5,6], [7,7,7,6,6,5,5,5], c='#2C3E50', s=100, alpha=0.9)
            # Add more patterns for other numbers...
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            st.pyplot(fig)
            plt.close()

        with col2:
            st.subheader(f"Plate {current_idx + 1} of {len(plates)}")
            st.write(f"**Description:** {plate['description']}")
            
            answer = st.text_input("What number do you see?", placeholder="Enter number or '0'")
            
            if st.button("Submit Answer", type="primary"):
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
        
        if st.button("Continue to Next Test", type="primary"):
            st.session_state.current_test = "farnsworth"
            st.rerun()

def farnsworth_test():
    st.markdown("""
    <div class="test-container">
        <h2>🌈 Farnsworth Color Arrangement Test</h2>
        <p><strong>Instructions:</strong> Answer questions about color sequences and relationships.</p>
    </div>
    """, unsafe_allow_html=True)

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
        },
        {
            "question": "Which color completes the sequence: Red → Orange → ? → Green",
            "options": ["Yellow", "Blue", "Purple", "Pink"],
            "correct": "Yellow"
        }
    ]

    answers = []
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}:** {q['question']}")
        answer = st.radio(f"Select answer:", q['options'], key=f"farnsworth_{i}")
        answers.append(answer)
        st.markdown("---")

    if st.button("Submit Farnsworth Test", type="primary"):
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
        
        if st.button("Continue to Lantern Test"):
            st.session_state.current_test = "lantern"
            st.rerun()

def lantern_test():
    st.markdown("""
    <div class="test-container">
        <h2>💡 Navigation Lights Test</h2>
        <p><strong>Instructions:</strong> Identify navigation light combinations for different vessels.</p>
    </div>
    """, unsafe_allow_html=True)

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
        },
        {
            "scenario": "Fishing vessel trawling",
            "lights": "🟢 Green + ⚪ White",
            "correct": "Green over White", 
            "options": ["Red over White", "Green over White", "White over Red", "White over Green"]
        }
    ]

    answers = []
    for i, scenario in enumerate(scenarios):
        st.write(f"**Scenario {i+1}:** {scenario['scenario']}")
        st.write(f"Lights: {scenario['lights']}")
        answer = st.selectbox(f"Select identification:", scenario['options'], key=f"lantern_{i}")
        answers.append(answer)
        st.markdown("---")

    if st.button("Submit Lantern Test", type="primary"):
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
        
        if st.button("View Results"):
            st.session_state.current_test = "results"
            st.rerun()

def show_results():
    st.markdown("""
    <div class="test-container">
        <h2>📊 Test Results</h2>
        <p>Comprehensive overview of your maritime vision assessment</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.test_results:
        st.warning("Complete tests to see results")
        return

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
    st.markdown("### 🎓 Assessment Certificate")
    
    st.markdown(f"""
    <div style='border: 3px solid #1E3A8A; padding: 2rem; border-radius: 10px; background: white;'>
        <h3 style='color: #1E3A8A; text-align: center;'>VisionQuest Navigator</h3>
        <h4 style='text-align: center;'>Maritime Vision Assessment</h4>
        <hr>
        <p><strong>Mariner:</strong> {st.session_state.get('user_name', 'Not provided')}</p>
        <p><strong>Rank:</strong> {st.session_state.get('user_rank', 'Not provided')}</p>
        <p><strong>Overall Score:</strong> {avg_score:.1f}%</p>
        <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()