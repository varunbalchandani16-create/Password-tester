import streamlit as st
import re
import random
import hashlib
import requests
from zxcvbn import zxcvbn

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="PassCheck Ultimate", page_icon="🛡️", layout="centered")

st.markdown(
    """
    <style>
    .metric-box { background-color: #1e293b; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #334155; }
    .metric-title { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 1.2rem; font-weight: bold; color: #f8fafc; margin-top: 5px; }
    
    .pwned-alert { background-color: #7f1d1d; color: white; padding: 15px; border-radius: 8px; font-weight: bold; border: 2px solid #ef4444;}
    .safe-alert { background-color: #064e3b; color: white; padding: 15px; border-radius: 8px; font-weight: bold; border: 2px solid #10b981;}
    
    .req-list { background-color: #0f172a; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 20px;}
    .req-met { color: #4ade80; font-weight: bold; padding: 2px 0;}
    .req-miss { color: #f87171; padding: 2px 0;}
    
    .suggestion-box { background-color: #064e3b; padding: 15px; border-radius: 8px; border: 1px solid #059669; margin-top: 10px; }
    </style>
    """, 
    unsafe_allow_html=True
)

# ==========================================
# 2. CYBERSECURITY LOGIC FUNCTIONS
# ==========================================
def check_basic_checklist(password):
    """The original visual checklist for basic requirements."""
    feedback = {
        "length": {"met": len(password) >= 12, "text": "At least 12 characters long"},
        "upper": {"met": bool(re.search(r'[A-Z]', password)), "text": "Contains an uppercase letter"},
        "lower": {"met": bool(re.search(r'[a-z]', password)), "text": "Contains a lowercase letter"},
        "number": {"met": bool(re.search(r'[0-9]', password)), "text": "Contains a number"},
        "special": {"met": bool(re.search(r'[^a-zA-Z0-9]', password)), "text": "Contains a special symbol (!@#$%)"}
    }
    return feedback

def generate_strong_suggestions(base_password):
    """The original suggestion engine to help users improve."""
    suggestions = []
    # Method 1: Substitution
    subs = {'a': '@', 's': '$', 'i': '!', 'o': '0', 'e': '3'}
    subbed_pass = "".join(subs.get(c.lower(), c) for c in base_password)
    suggestions.append(f"{subbed_pass.capitalize()}!{random.randint(10,99)}")
    
    # Method 2: Passphrase
    words = ["Secure", "Shield", "Nova", "Cyber", "Aegis", "Echo"]
    suggestions.append(f"{base_password.capitalize()}-{random.choice(words)}-{random.randint(100,999)}#")
    
    return suggestions

def check_pwned_api(password):
    """Checks the Have I Been Pwned API safely via k-Anonymity."""
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200: return None
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix: return int(count)
        return 0
    except requests.exceptions.RequestException:
        return None

# ==========================================
# 3. USER INTERFACE
# ==========================================
st.title("🛡️ PassCheck Ultimate")
st.write("The complete cryptographic analysis and remediation dashboard.")

password = st.text_input("Enter your password to analyze:", type="password")
st.divider()

if password:
    with st.spinner("Running deep analysis..."):
        pwned_count = check_pwned_api(password)
        z_result = zxcvbn(password)
        basic_rules = check_basic_checklist(password)
        
    score = z_result['score'] # 0 to 4
    
    # --- MODULE 1: THE VISUAL STRENGTH METER ---
    st.write("### 📊 Overall Cryptographic Strength")
    st.progress(int((score / 4) * 100))
    
    if score <= 1:
        st.error("🚨 **WEAK:** Highly guessable. Protection against throttled online attacks only.")
    elif score == 2:
        st.warning("⚠️ **MODERATE:** Somewhat guessable. Protection from unthrottled online attacks.")
    elif score == 3:
        st.success("✅ **STRONG:** Safely unguessable. Moderate protection from offline slow-hash attacks.")
    else:
        st.success("🌟 **EXCELLENT:** Very unguessable. Strong protection from offline slow-hash attacks.")

    st.write("") 

    # --- MODULE 2: BASIC SECURITY CHECKLIST ---
    st.write("### 🔍 Security Policy Checklist")
    checklist_html = '<div class="req-list">'
    all_met = True
    for rule in basic_rules.values():
        if rule["met"]:
            checklist_html += f'<div class="req-met">✅ {rule["text"]}</div>'
        else:
            checklist_html += f'<div class="req-miss">❌ {rule["text"]}</div>'
            all_met = False
    checklist_html += '</div>'
    st.markdown(checklist_html, unsafe_allow_html=True)

    # --- MODULE 3: BREACH RADAR ---
    st.write("### 🌍 Live Breach Radar")
    if pwned_count and pwned_count > 0:
        st.markdown(f"""
        <div class="pwned-alert">
            🚨 CRITICAL COMPROMISE DETECTED!<br>
            This exact password has been seen in {pwned_count:,} data breaches. Do not use it.
        </div>
        """, unsafe_allow_html=True)
    elif pwned_count == 0:
        st.markdown("""
        <div class="safe-alert">
            ✅ CLEAR: This password has not been found in any known public data breaches.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Could not connect to the breach database to verify this password.")

    st.write("")

    # --- MODULE 4: HACKER METRICS ---
    st.write("### 🧮 Hacker Metrics")
    col1, col2 = st.columns(2)
    with col1:
        crack_time = z_result['crack_times_display']['offline_fast_hashing_1e10_per_second']
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Est. Offline Crack Time</div>
            <div class="metric-value">{crack_time.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        guesses = int(z_result['guesses'])
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Mathematical Guesses</div>
            <div class="metric-value">{guesses:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --- MODULE 5: INTELLIGENT REMEDIATION (SUGGESTIONS) ---
    # Only show if they scored less than perfect or failed the basic checklist
    if score < 4 or not all_met:
        st.write("### 💡 Upgrade Your Security")
        st.write("Your password could be stronger. Try one of these AI-generated alternatives based on your input:")
        
        suggestions = generate_strong_suggestions(password)
        
        st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
        st.write("**Variation 1 (Leetspeak Substitutions):**")
        st.code(suggestions[0], language="text")
        
        st.write("**Variation 2 (NIST Recommended Passphrase):**")
        st.code(suggestions[1], language="text")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Enter a password above to launch the full security suite.")