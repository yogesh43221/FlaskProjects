## LangChain Gemini Chatbot

- **This repository contains a Flask-based chatbot project using LangChain and Google's Gemini model.**

# 📂 Project Structure

brainloxchatbot-api/
├── app.py
├── requirements.txt
├── .gitignore
├── static/
│   ├── images/
│   │   └── user.png
│   │   └── gpt.jpg
│   └── style.css
├── templates/
│   └── index.html
└── faiss_index/
    └── index.faiss
    └── index.pkl

# 📄 Prerequisites

**To run this project locally, you need:**

* Python 3.6 or higher installed.
* Pip installed (Python package installer).
* A Google Cloud Platform project with the Generative AI API enabled and a valid API key.
* A Gmail account (or other SMTP service) for sending email notifications.
* Required Python packages (install using `pip install -r requirements.txt`). Create a `requirements.txt` file with the following content:

    ```
    Flask
    langchain-google-genai
    langchain-community
    faiss-cpu
    reportlab
    python-dotenv
    unstructured
    ```

# 🛠️ Setup Instructions

1.  **Clone this repository:**

    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd your-repo-name/brainloxchatbot-api
    ```

3.  **Create a `.env` file in the `brainloxchatbot-api` directory and add your API keys and email credentials:**

    ```
    GOOGLE_API_KEY=your_google_api_key
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_email_app_password
    ```

    * Replace the placeholder values with your actual credentials.
    * If using Gmail, generate an app password for security.

4.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application:**

    ```bash
    python app.py
    ```

6.  **Open your web browser and go to `http://127.0.0.1:5000` to interact with the chatbot.**

# 🤝 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/your-repo-name/issues) for open issues or to suggest improvements.

# 📄 License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (If you don't have a license file yet, create one and add it)
