from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListItem, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = Flask(__name__)

# Function to create FAISS index
def create_faiss_index(url):
    try:
        loader = UnstructuredURLLoader([url])
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db = FAISS.from_documents(texts, embeddings)
        db.save_local("faiss_index")
        print("FAISS index created successfully!")
    except Exception as e:
        print(f"Error creating FAISS index: {e}")

# Create FAISS index (call this function when you want to create or update the index)
create_faiss_index("https://brainlox.com/courses/category/technical")

# Load the FAISS index
try:
    db = FAISS.load_local(
        "faiss_index",
        GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        allow_dangerous_deserialization=True,
    )
except Exception as e:
    print(f"Error loading FAISS index: {e}")
    # Handle the error appropriately, e.g., by logging it or displaying a message to the user
    db = None  # Set db to None if loading fails

chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    try:
        message = request.json.get("message")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

        if db:
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
            response = qa.run(message)
        else:
            response = llm.invoke(message).content  # If FAISS is not available, use llm directly

        chat_history.append({"user": message, "bot": response})
        return jsonify({"content": response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"content": "An error occurred."})

@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        email = data["email"]

        # Generate PDF
        pdf_filename = "chat_history.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.leading = 14  # Adjust line spacing
        code_style = styles["Code"]
        code_style.fontName = "Courier"  # Monospace font
        elements = []

        for item in chat_history:
            elements.append(Paragraph(f"<b>User:</b> {item['user']}", normal_style))
            bot_response = item['bot']  # Get the bot response from chat_history

            # Handle lists
            if "* " in bot_response:
                list_items = [line.strip() for line in bot_response.splitlines() if line.startswith("* ")]
                if list_items:
                    bullet_list = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_items],
                                                bulletType='bullet')
                    elements.append(bullet_list)
                    bot_response = "\n".join(
                        [line for line in bot_response.splitlines() if not line.startswith("* ")])

            # Handle code blocks
            if "```" in bot_response:
                code_blocks = bot_response.split("```")
                for i, part in enumerate(code_blocks):
                    if i % 2 == 1:  # Odd parts are code
                        elements.append(Paragraph(part, code_style))
                    else:  # Even parts are normal text
                        elements.append(Paragraph(part, normal_style))
            else:
                elements.append(Paragraph(f"<b>Gemini:</b> {bot_response}", normal_style)) # replaced bot_response with Gemini: bot_response.

            elements.append(Spacer(1, 0.2 * inch))  # Add space between messages

        doc.build(elements)

        # Send Email (same as before)
        from_email = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = email
        msg["Subject"] = "Chat History"

        with open(pdf_filename, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename= {pdf_filename}")
            msg.attach(attachment)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.send_message(msg)

        return jsonify({"message": "Email sent successfully!"})
    except Exception as e:
        print(f"Email Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()