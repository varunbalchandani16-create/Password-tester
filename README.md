🛡️ Password Checker

Password Checker is an advanced, enterprise-grade password strength analyzer and remediation dashboard built with Python and Streamlit.

Rather than relying on outdated, arbitrary password rules (e.g., "must contain one symbol"), this tool evaluates passwords against real-world attack vectors, dictionary algorithms, and live global data breaches.

✨ Features

🧠 Advanced Algorithmic Strength (zxcvbn): Uses Dropbox's zxcvbn engine to calculate realistic offline crack times, entropy, and mathematical guesses required to brute-force the password.

🌍 Live Breach Radar: Integrates with the Have I Been Pwned API to check if a password has been compromised in known global data breaches.

🔒 100% Secure via k-Anonymity: The user's password is never transmitted over the internet. The app hashes the password locally using SHA-1 and only sends the first 5 characters of the hash to the API.

✅ Security Policy Checklist: A visual dashboard that audits the password against standard complexity requirements.

💡 Intelligent Remediation: Automatically suggests highly secure, memorable alternatives (using Leetspeak substitutions and NIST-recommended passphrases) if the user's password is weak.

🛠️ Tech Stack

Language: Python

Frontend/Framework: Streamlit (with Custom CSS/HTML styling)

Libraries:

zxcvbn (Pattern recognition & entropy math)

requests (API communication)

hashlib & re (Standard Python libraries for hashing and regex)

🚀 How to Run Locally

To run this project on your own machine, follow these steps:

1. Clone the repository:

git clone [https://github.com/your-username/password-checker.git](https://github.com/your-username/password-checker.git)
cd password-checker


2. Install the required dependencies:

pip install -r requirements.txt


3. Run the Streamlit application:

streamlit run app.py


The application will automatically open in your default web browser at http://localhost:8501.

🌐 Live Demo

The application is deployed on Streamlit Community Cloud.
Play with the live app here: https://password-checker-demo.streamlit.app
(Note: Update this URL to match your exact Streamlit Cloud link if it is different)

🎓 Project Context

This project was developed as part of the GTU SBTP-2026 program (Subject Code: D105000011).

Initiative: Bharat Cares by SMEC Trust in collaboration with IBM.

Objective: To demonstrate practical web application development, API integration, and modern cybersecurity fundamentals (cryptography, hashing, and threat mitigation).
