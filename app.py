import streamlit as st
import streamlit.components.v1 as components
from utils import hash_passkey, encrypt_data, decrypt_data, load_data, save_data
from dotenv import load_dotenv
import os
#load environment variables from .env file
load_dotenv()
#get Master password
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")

# Page settings
st.set_page_config(page_title="Secure Data App", layout="centered")
st.markdown("""
    <style>
    /* Tailwind-style primary button */
    .stButton > button {
        background-color: #3b82f6; /* Tailwind blue-500 */
        color: white;
        padding: 0.6em 1.2em;
        font-size: 1em;
        border: none;
        border-radius: 0.5em;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #2563eb; /* Tailwind blue-600 */
        cursor: pointer;
        transform: scale(1.03);
    }

    /* Headings */
    h1, h2, h3 {
        color: #1e293b; /* Tailwind slate-800 */
        font-family: 'Segoe UI', sans-serif;
    }

    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: #f1f5f9; /* Tailwind slate-100 */
        color: #0f172a; /* slate-900 */
        border: 1px solid #cbd5e1; /* slate-300 */
        border-radius: 0.5rem;
        padding: 0.5rem;
        font-size: 1em;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b; /* slate-800 */
        color: white;
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .card {
        background-color: white;
        padding: 1.5rem;
        margin-top: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.75rem;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <div class="card">
        <div class="card-title">🔐 Secure Area</div>
        <p>This section is protected and styled like a Tailwind card!</p>
    </div>
""", unsafe_allow_html=True)



# Session state
if "auth" not in st.session_state:
    st.session_state.auth = True
if "failed" not in st.session_state:
    st.session_state.failed = 0
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

st.title("🛡️ Secure Data Encryption System")

# Load stored data
data = load_data()

# Show success message after login
if st.session_state.just_logged_in:
    st.success("✅ Reauthorized.")
    st.session_state.just_logged_in = False

# ----------------------- Function to Show Copy Button -----------------------
def show_copy_button(encrypted_text):
    components.html(f"""
        <textarea id="encryptedText" rows="4" style="width: 100%;">{encrypted_text}</textarea>
        <button onclick="copyToClipboard()" style="
            margin-top: 10px;
            padding: 8px 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        ">📋 Copy to Clipboard</button>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("encryptedText");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
        }}
        </script>
    """, height=200)

# ---------------------------- Home Page -------------------------------------
if choice == "Home":
    st.subheader("🏠 Welcome to the App")
    st.write("Encrypt and store your data securely!")

# -------------------------- Store Data Page ---------------------------------
elif choice == "Store Data":
    if st.session_state.auth:
        st.subheader("📂 Store Your Data")
        username = st.text_input("Enter Your Username:")
        text = st.text_area("Enter Data:")
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Encrypt & Save"):
            if username and text and passkey:
                encrypted = encrypt_data(text)
                user_key = f"{username}_{encrypted[:10]}"

                data[user_key] = {
                    "encrypted_text": encrypted,
                    "passkey": hash_passkey(passkey)
                }
                save_data(data)

                st.success("✅ Data encrypted and saved!")
                show_copy_button(encrypted)

            else:
                st.error("⚠️ All fields are required!")
    else:
        st.warning("🔒 You are not authorized. Please log in again.")

# ------------------------- Retrieve Data Page -------------------------------
elif choice == "Retrieve Data":
    if st.session_state.auth:
        st.subheader("🔍 Retrieve Your Data")
        username = st.text_input("Enter Your Username:")
        encrypted_text = st.text_area("Enter Encrypted Data:")
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Decrypt"):
            found = False
            user_key = f"{username}_{encrypted_text[:10]}"

            if user_key in data:
                record = data[user_key]
                if record["passkey"] == hash_passkey(passkey):
                    decrypted = decrypt_data(record["encrypted_text"])
                    st.success(f"✅ Decrypted Data: {decrypted}")
                    st.session_state.failed = 0
                    found = True

            if not found:
                st.session_state.failed += 1
                st.error(f"❌ Incorrect passkey or data! Attempts left: {3 - st.session_state.failed}")

                if st.session_state.failed >= 3:
                    st.warning("🔒 Too many failed attempts! Redirecting to Login.")
                    st.session_state.auth = False
                    st.rerun()
    else:
        st.warning("🔒 You are not authorized. Please log in again.")

# ---------------------------- Login Page ------------------------------------
elif choice == "Login":
    st.subheader("🔑 Reauthorize")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == MASTER_PASSWORD:
            st.session_state.failed = 0
            st.session_state.auth = True
            st.session_state.just_logged_in = True
            st.experimental_rerun()

        else:
            st.error("❌ Wrong password!")

