# -AI-Based-Resume-Analyser-
📄 Resume Analyzer AI Agent

An AI-powered Resume Analyzer Agent that analyzes resumes and provides intelligent improvement suggestions based on a target job role.
The agent uses a Large Language Model (LLM) to compare resumes against job requirements and suggest skills, wording, and formatting improvements.

This project demonstrates Agentic AI concepts such as perception, reasoning, and action.

🚀 What This Project Does

✔ Accepts resumes as PDF uploads or plain text
✔ Extracts resume content automatically
✔ Identifies skills, education, and work experience
✔ Compares resume with a target job role
✔ Suggests missing skills and improvements
✔ Improves wording and formatting using AI
✔ Clean and interactive Streamlit UI

🤖 Agentic AI Behavior

The Resume Analyzer works as an intelligent AI agent:

1️⃣ Perception

Reads resume content from PDF or text input

Accepts target job role from the user

2️⃣ Reasoning

Uses an LLM to:

Understand resume structure

Match resume content with job role

Identify skill gaps

Analyze clarity and professionalism

3️⃣ Action

Generates:

Resume analysis

Improvement suggestions

Missing skills list

Better wording and formatting tips

🛠 Tech Stack

Python 3.10+

Streamlit – User Interface

PyPDF2 – PDF text extraction

LLM API (OpenAI / compatible) – Resume analysis

dotenv – Environment variable management

📁 Project Structure
resume-analyzer-ai-agent/
│
├── app.py                 # Streamlit UI
├── resume_parser.py       # PDF/Text extraction logic
├── ai_analyzer.py         # AI resume analysis logic
├── requirements.txt       # Dependencies
├── .env                   # API keys (not committed)
└── README.md

📌 Features

✅ Upload resume as PDF

✅ Paste resume as plain text

✅ Extract structured information

✅ AI-based job role comparison

✅ Missing skills detection

✅ Resume wording & formatting suggestions

✅ Simple, clean UI

🔑 Prerequisites

Python 3.10 or higher

LLM API key (OpenAI / compatible)

Git (optional)

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/your-username/resume-analyzer-ai-agent.git
cd resume-analyzer-ai-agent

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here


⚠️ Never commit API keys to GitHub

5️⃣ Run the Application
streamlit run app.py


Open in browser:

http://localhost:8501

🖥 How Resume Is Processed

User uploads a PDF or enters plain text

PyPDF2 extracts raw text from PDF

Text is cleaned and structured

Resume sections are identified:

Skills

Education

Experience

🧠 How AI Generates Suggestions

The AI model:

Compares resume content with target job role

Identifies missing or weak skills

Suggests:

Better action verbs

Improved sentence clarity

Professional formatting tips

Generates personalized feedback

📝 Example Usage

Input:

Resume: PDF uploaded

Job Role: Data Analyst

AI Output:

Missing Skills: SQL, Power BI

Resume Improvements:

Add quantified achievements

Improve bullet point clarity

Use stronger action verbs

🔮 Future Enhancements

📊 Resume scoring system

🧠 ATS keyword optimization

📎 Multi-resume comparison

🌐 Job description upload

🐳 Docker support

☁️ Cloud deployment
