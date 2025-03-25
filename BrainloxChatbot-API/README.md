# 🌐 Live App
**Access the chatbot here:** [Brainlox Chatbot API](https://brainloxchatbot-api-274691259241.asia-south1.run.app)

---

# LangChain Gemini Chatbot 🚀

- **This repository contains a Flask-based chatbot using LangChain and Google's Gemini model, deployed on Google Cloud Run.**

## 📂 Project Structure
```
brainloxchatbot-api/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .dockerignore
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
```

---

## 📄 Prerequisites
**To run this project, you need:**
* Python 3.9 or higher installed.
* Pip installed (Python package installer).
* A Google Cloud Project with the **Generative AI API enabled** and a valid API key.
* A Gmail account (or other SMTP service) for sending emails.
* Required Python packages (install using `pip install -r requirements.txt`).

---

## 🛠️ Setup Instructions

### **Run Locally**

1️⃣ **Clone this repository:**
```bash
git clone https://github.com/yogesh43221/FlaskProjects.git
```

2️⃣ **Navigate to the project directory:**
```bash
cd FlaskProjects/BrainloxChatbot-API
```

3️⃣ **Create a `.env` file** and add your API keys and email credentials:
```env
GOOGLE_API_KEY=your_google_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
```
Replace placeholders with your actual credentials.

4️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

5️⃣ **Run the Flask app:**
```bash
python app.py
```

6️⃣ **Access the chatbot** at `http://127.0.0.1:5000` in your browser.

---

## 🚀 Deploy to Google Cloud Run

### **1️⃣ Enable Google Cloud APIs** (if not already enabled)
```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### **2️⃣ Set Environment Variables in Cloud Run**
```bash
gcloud run services update brainloxchatbot-api --region asia-south1 \
  --set-env-vars GOOGLE_API_KEY="your_google_api_key",EMAIL_USER="your_email@gmail.com",EMAIL_PASSWORD="your_app_password"
```

### **3️⃣ Build and Push Docker Image**
```bash
gcloud builds submit --tag gcr.io/your-project-id/brainloxchatbot-api
```

### **4️⃣ Deploy to Cloud Run**
```bash
gcloud run deploy brainloxchatbot-api --image gcr.io/your-project-id/brainloxchatbot-api --region asia-south1 --platform managed --allow-unauthenticated
```

### **5️⃣ Access the Live App**
Once deployed, get the service URL:
```bash
gcloud run services describe brainloxchatbot-api --region asia-south1 --format 'value(status.url)'
```

---

## 🔍 Logs and Debugging
To check logs and errors, run:
```bash
gcloud run services logs read brainloxchatbot-api --region asia-south1 --limit=50
```

To restart Cloud Run service:
```bash
gcloud run services update-traffic brainloxchatbot-api --to-latest
```

---

## 🤝 Contributions
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yogesh43221/FlaskProjects/issues) for open issues or to suggest improvements.

---

## 📄 License
This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

