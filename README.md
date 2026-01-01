# Resume Analyzer AI Agent

A Streamlit-based AI application that analyzes resumes and provides improvement suggestions using Large Language Models (LLMs).

## Features

- **Resume Upload**: Accepts both PDF files and plain text input
- **Information Extraction**: Automatically extracts skills, education, and work experience
- **AI-Powered Analysis**: Uses LLMs to analyze resume against target job roles
- **Improvement Suggestions**: Provides actionable feedback to improve the resume
- **User-Friendly Interface**: Clean, intuitive Streamlit UI

## How It Works

### Resume Processing

The application processes resumes through several stages:

1. **Input Processing**:
   - For PDF uploads: Uses PyPDF2 to extract text content
   - For text input: Directly processes the provided text

2. **Information Extraction**:
   - **Skills Extraction**: Uses regex patterns and keyword matching to identify technical and soft skills
   - **Education Extraction**: Identifies educational qualifications, degrees, and institutions
   - **Work Experience Extraction**: Detects job positions, companies, and employment history

3. **AI Analysis**:
   - Sends resume content and target job to an LLM (OpenRouter API in production)
   - Analyzes resume relevance to target role
   - Generates improvement suggestions

### AI-Generated Suggestions

The LLM analyzes the resume against the target job role to provide:

1. **Strengths**: Highlights resume elements that align well with the target role
2. **Areas for Improvement**: Identifies weak areas that need attention
3. **Missing Skills**: Lists skills relevant to the target role that are absent from the resume
4. **Wording & Formatting**: Suggests better language and formatting for improved impact

## How AI Generates Suggestions

The AI analysis follows these steps:

1. **Context Understanding**: The LLM understands the target job requirements and expectations
2. **Resume Assessment**: Evaluates the resume content against job requirements
3. **Gap Analysis**: Identifies discrepancies between resume and job requirements
4. **Recommendation Generation**: Creates specific, actionable suggestions for improvement

The suggestions are tailored to help users:
- Optimize their resume for specific roles
- Highlight relevant skills and experiences
- Improve language and formatting for better impact
- Fill skill gaps for their target positions

## Setup and Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Copy `.env.example` to `.env` and add your API key:
     ```bash
     cp .env.example .env
     # Then edit .env to add your API key
     ```
   - Or set the environment variable directly:
     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```
4. Run the application:
   ```bash
   streamlit run resume_analyzer.py
   ```

## Usage

1. Upload a PDF resume or paste resume text
2. Enter your target job role
3. Click "Analyze Resume"
4. Review the analysis results and improvement suggestions

## Files

- `resume_analyzer.py`: Main application file with all functionality
- `requirements.txt`: Python dependencies
- `README.md`: This documentation file

## Technologies Used

- **Streamlit**: Web framework for the user interface
- **PyPDF2**: PDF text extraction
- **OpenRouter API**: LLM for resume analysis
- **Regular Expressions**: Pattern matching for information extraction
- **Python**: Core programming language

## Limitations

- For full functionality, an OpenRouter API key is required
- Accuracy of information extraction depends on resume formatting
- Complex resume layouts may not be parsed correctly

## Future Enhancements

- Support for additional file formats (DOCX, etc.)
- Integration with multiple LLM providers
- More sophisticated parsing for complex resume formats
- Export functionality for analysis results