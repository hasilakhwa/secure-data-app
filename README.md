# Secure Data Encryption System

## Project Overview
This is a simple yet powerful data encryption system built using Python and Streamlit. The app allows users to securely store and retrieve encrypted data using a passkey. The data is encrypted using a secure encryption algorithm, and the passkey is hashed for additional security.

## Features
- **Data Encryption:** Encrypt data securely before storing it.
- **Data Decryption:** Retrieve and decrypt data with the correct passkey.
- **Login System:** Secure reauthorization using a master password.
- **Error Handling:** Retry limit for failed passkey attempts.

## Setup Instructions

1. **Clone the repository:**
git clone https://github.com/yourusername/your-repository.git

2. **Navigate to the project folder:**
cd your-repository


3. **Create a virtual environment (optional but recommended):**
python -m venv venv

4. **Activate the virtual environment:**
- On **Windows**:
  ```
  .\venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```
  source venv/bin/activate
  ```

5. **Install the required dependencies:**
pip install -r requirements.txt

6. **Run the app:**
streamlit run app.py

## Usage

- **Store Data:** Go to the 'Store Data' page, enter a username, data, and passkey, then click 'Encrypt & Save' to store the encrypted data.
- **Retrieve Data:** Go to the 'Retrieve Data' page, enter the username, encrypted data, and passkey, then click 'Decrypt' to retrieve the original data.
- **Login:** The 'Login' page allows you to reauthorize with a master password if needed.

## License

This project is licensed under the MIT License.


