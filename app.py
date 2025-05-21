import zipfile
import io
import streamlit as st
from cryptography.fernet import Fernet

# ============================ Page Config ============================
st.set_page_config(
    page_title="🔐 Secure File Vault",
    page_icon="🔒",
    layout="centered"
)

# ============================ Theme Selection ============================
st.sidebar.header("🎨 Theme")
theme = st.sidebar.radio("Choose Theme", ["🌞 Light", "🌙 Dark"])

if theme == "🌞 Light":
    bg_style = """
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1603791440384-56cd371ee9a7");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.90);
        padding: 2rem;
        border-radius: 10px;
        color: black;
    }
    </style>
    """
else:
    bg_style = """
    <style>
    body {
        background-color: #0d1117;
    }
    .stApp {
        background-color: #161b22;
        color: #c9d1d9;
        padding: 2rem;
        border-radius: 10px;
    }
    /* General text colors */
    h1, h5, label, .stMarkdown, .stButton button, .stDownloadButton > button, .stFileUploader label, .stTextInput > div > div > input {
        color: #c9d1d9 !important;
    }
    /* Radio button container and label fix */
    div[data-baseweb="radio"] {
        background-color: #21262d !important;
        border-radius: 0.5rem;
        padding: 0.5rem;
        color: #c9d1d9 !important;
    }
    /* Radio button label text */
    div[data-baseweb="radio"] label {
        color: #c9d1d9 !important;
    }
    /* Download button */
    .stDownloadButton > button {
        background-color: #238636;
        color: white;
    }
    .stDownloadButton > button:hover {
        background-color: #2ea043;
    }
    </style>
    """

st.markdown(bg_style, unsafe_allow_html=True)

# ============================ Title & Instructions ============================
st.markdown("""
    <h1 style='text-align: center;'>🔐 Secure File Vault</h1>
    <h5 style='text-align: center;'>Encrypt and decrypt your files with ease and confidence.</h5>
    <br>
""", unsafe_allow_html=True)

with st.expander("ℹ️ How It Works", expanded=False):
    st.markdown("""
    - **Encrypt Mode**: Upload a file, generate or upload a key, and download the encrypted file.
    - **Decrypt Mode**: Upload an encrypted file and the matching key to restore your original file.
    - Keep your key **safe** – it's required to decrypt the file!
    """)

# ============================ Helper Functions ============================
def generate_key():
    return Fernet.generate_key()

def encrypt_file(data, key):
    return Fernet(key).encrypt(data)

def decrypt_file(data, key):
    return Fernet(key).decrypt(data)

# ============================ Mode Selection ============================
st.sidebar.header("🛠️ Select Mode")
mode = st.sidebar.radio("", ["🔐 Encrypt File", "🔓 Decrypt File"])

st.sidebar.markdown("---")
st.sidebar.markdown("📁 Made for Security ")

# ============================ File Upload ============================
st.subheader(f"{mode}")
uploaded_file = st.file_uploader("📤 Upload your file", type=None)

# ============================ Key Option ============================
key_option = st.radio("🔑 Key Option", ["Generate New Key", "Upload Existing Key"])
key = None

if key_option == "Generate New Key":
    if st.button("✨ Generate Key"):
        key = generate_key()
        st.success("✅ Key generated successfully!")
        st.info("🔑 Key will be included in the encrypted ZIP file.")
else:
    key_file = st.file_uploader("📂 Upload .key file", type=["key"])
    if key_file:
        key = key_file.read()

# ============================ Process File ============================
if uploaded_file and key:
    file_data = uploaded_file.read()

    if "Encrypt" in mode:
        encrypted_data = encrypt_file(file_data, key)
        st.success("🔒 File encrypted successfully!")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            zip_file.writestr("encrypted_file.enc", encrypted_data)
            zip_file.writestr("encryption_key.key", key)
        zip_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Encrypted + Key (.zip)",
            data=zip_buffer,
            file_name="encrypted_package.zip",
            mime="application/zip"
        )

    elif "Decrypt" in mode:
        try:
            decrypted_data = decrypt_file(file_data, key)
            st.success("🔓 File decrypted successfully!")
            st.download_button("⬇️ Download Decrypted File", decrypted_data, file_name="decrypted_file")
        except Exception:
            st.error("❌ Decryption failed. Invalid key or corrupted file.")
