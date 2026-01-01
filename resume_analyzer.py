import streamlit as st
import PyPDF2
import re
import os
from typing import Dict, List, Optional
import requests
import json
from config import config

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Resume Analyzer AI Agent",
    page_icon="📄",
    layout="wide"
)

# Initialize session state for storing results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from a PDF file using PyPDF2
    """
    try:
        # Reset file pointer to beginning
        pdf_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_skills(text: str) -> List[str]:
    """
    Extract skills from the resume text
    """
    # Comprehensive list of technical and soft skills
    technical_skills = [
        # Programming languages
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'R', 'Go', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'TypeScript',
        # Frameworks and libraries
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'TensorFlow', 'PyTorch', 'Pandas', 'Numpy',
        'Express', 'Ruby on Rails', 'Laravel', 'ASP.NET', 'React Native', 'Flutter',
        # Tools and platforms
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'Jenkins', 'CI/CD', 'Agile', 'Scrum', 'JIRA', 'Trello',
        'Linux', 'Unix', 'Windows', 'MacOS', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle',
        # Soft skills
        'Project Management', 'Leadership', 'Communication', 'Teamwork', 'Problem Solving', 'Analytical Skills',
        'Time Management', 'Critical Thinking', 'Creativity', 'Adaptability', 'Emotional Intelligence',
        # Specialized areas
        'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 'Data Science', 'Data Analysis',
        'Web Development', 'Mobile Development', 'DevOps', 'Cybersecurity', 'Cloud Computing', 'Blockchain',
        'UI/UX', 'Frontend', 'Backend', 'Full Stack', 'API Development', 'Database Design'
    ]
    
    skills = set()
    
    # Check for each skill in the text
    for skill in technical_skills:
        # Case-insensitive search for the skill
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            skills.add(skill)
    
    # Additional skills from common sections
    # Look for skills section
    skills_section = re.search(r'(skills|technologies|expertise)[:\s\n](.*?)(\n\n|\n[A-Z][a-z]+:|$)', text, re.IGNORECASE | re.DOTALL)
    if skills_section:
        skills_text = skills_section.group(2)
        # Extract individual skills (comma-separated)
        individual_skills = re.split(r'[,;]', skills_text)
        for skill in individual_skills:
            skill = skill.strip().strip('-').strip()
            if len(skill) > 2:  # Filter out very short entries
                # Check if the skill is in our known list or looks like a skill
                if skill in technical_skills or len(skill.split()) <= 3:
                    skills.add(skill)
    
    return list(skills)

def extract_education(text: str) -> List[str]:
    """
    Extract education information from the resume text
    """
    education = set()
    
    # Comprehensive list of education-related terms
    education_keywords = [
        'Bachelor', 'Master', 'PhD', 'Doctorate', 'Degree', 'B.Sc', 'M.Sc', 'B.Tech', 'M.Tech',
        'B.A.', 'M.A.', 'B.Com', 'M.Com', 'BBA', 'MBA', 'B.E.', 'M.E.', 'B.Eng', 'M.Eng',
        'Associate', 'Diploma', 'Certification', 'Certified', 'Certificate', 'Coursework',
        'University', 'College', 'Institute', 'School', 'Academy', 'Campus'
    ]
    
    # Look for education section
    education_section = re.search(r'(education|academic background|qualifications)[:\s\n](.*?)(\n\n|\n[A-Z][a-z]+:|$)', text, re.IGNORECASE | re.DOTALL)
    if education_section:
        education_text = education_section.group(2)
        
        # Extract degree and institution details
        # Pattern: Degree followed by field and institution
        degree_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:in|at)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:at|from)?\s*([A-Z][A-Za-z\s]+University|College|Institute)',
            r'(Bachelor|Master|PhD|B\.[A-Z]+|M\.[A-Z]+|B\.Tech|M\.Tech)[\w\s,.\-&()]*?(University|College|Institute)?[\w\s,.\-&()]*',
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, education_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Combine all non-empty parts of the match
                    edu_info = ' '.join([part for part in match if part.strip()])
                    if edu_info:
                        education.add(edu_info.strip())
                else:
                    education.add(match.strip())
    
    # If no education section found, look for education keywords throughout the text
    if not education:
        for keyword in education_keywords:
            matches = re.findall(r'\b' + re.escape(keyword) + r'[\w\s,.\-&()]{0,100}?([A-Z][a-z\s]{5,50}?)(University|College|Institute|School)', text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    education.add(f"{match[0]} {match[1]}")
                else:
                    education.add(match)
    
    return list(education)

def extract_work_experience(text: str) -> List[str]:
    """
    Extract work experience from the resume text
    """
    experiences = set()
    
    # Look for work experience section
    exp_section = re.search(r'(work experience|professional experience|employment history|career history|professional background)[:\s\n](.*?)(\n\n|\n[A-Z][a-z]+:|$)', text, re.IGNORECASE | re.DOTALL)
    if exp_section:
        exp_text = exp_section.group(2)
        
        # Extract company names and positions
        # Pattern: Company - Position or Company, Position
        company_position_patterns = [
            r'([A-Z][A-Za-z\s&.,\-()]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|Group)?)\s*[-,]\s*([A-Z][a-z\s]{5,40})',
            r'([A-Z][A-Za-z\s&.,\-()]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|Group)?).{0,20}(?:at|@)\s*([A-Z][a-z\s]{5,40})',
            r'([A-Z][a-z\s]{5,40})\s*(?:at|@)\s*([A-Z][A-Za-z\s&.,\-()]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|Group)?)',
        ]
        
        for pattern in company_position_patterns:
            matches = re.findall(pattern, exp_text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    # Determine which part is company and which is position
                    # Usually the longer string or the one containing 'Inc', 'Ltd', etc. is the company
                    part1, part2 = match[0].strip(), match[1].strip()
                    
                    # Check if part1 looks like a company (contains company suffix or is longer)
                    if re.search(r'(Inc\.?|Ltd\.?|LLC|Corp\.?|Group)', part1, re.IGNORECASE) or len(part1) > len(part2):
                        experiences.add(f"{part2} at {part1}")
                    else:
                        experiences.add(f"{part1} at {part2}")
    
    # Alternative pattern for finding job titles and companies throughout the text
    job_patterns = [
        r'([A-Z][A-Za-z\s]{5,30})\s*(?:at|@)\s*([A-Z][A-Za-z\s&.,\-()]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|Group)?)',
        r'([A-Z][A-Za-z\s&.,\-()]+(?:Inc\.?|Ltd\.?|LLC|Corp\.?|Group)?)\s*(?:-|,)\s*([A-Z][A-Za-z\s]{5,30})',
    ]
    
    for pattern in job_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) >= 2:
                part1, part2 = match[0].strip(), match[1].strip()
                # Determine which part is company and which is position
                if re.search(r'(Inc\.?|Ltd\.?|LLC|Corp\.?|Group)', part1, re.IGNORECASE) or len(part1) > len(part2):
                    experiences.add(f"{part2} at {part1}")
                else:
                    experiences.add(f"{part1} at {part2}")
    
    return list(experiences)

def analyze_resume_with_llm(resume_text: str, target_job: str) -> Dict:
    """
    Send resume and job target to LLM for analysis
    """
    # Check if API key is configured
    if not config.validate_config():
        # If no API key, return simulated response
        analysis = {
            "strengths": ["Strong technical background in Python and data science", 
                          "Relevant experience in machine learning projects", 
                          "Good academic background from reputable institution"],
            "improvements": ["Add more specific metrics to quantify achievements",
                             "Include more technical keywords related to target role",
                             "Improve formatting for better readability"],
            "missing_skills": ["Cloud platforms (AWS/Azure)", "Containerization (Docker/Kubernetes)", "CI/CD pipelines"],
            "wording_suggestions": ["Replace 'responsible for' with action verbs like 'developed', 'implemented', 'led'",
                                    "Quantify achievements with specific numbers and percentages",
                                    "Use industry-specific keywords that match job descriptions"]
        }
        return analysis
    
    try:
        # Create the prompt for the LLM
        prompt = f"Analyze this resume for the target job role '{target_job}'. \nResume: {resume_text}\n\nPlease provide:\n1. Strengths in the resume relevant to the target role\n2. Areas for improvement\n3. Missing skills for the target role\n4. Wording and formatting suggestions\n\nFormat your response as a JSON object with keys: strengths, improvements, missing_skills, wording_suggestions.\nEach value should be a list of strings."
        
        # Use OpenRouter API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": config.LLM_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": config.TEMPERATURE,
                "max_tokens": config.MAX_TOKENS,
                "reasoning": {"enabled": config.REASONING_ENABLED}
            })
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            st.error(f"API request failed with status {response.status_code}: {response.text}")
            return {
                "strengths": ["Resume contains relevant technical skills"],
                "improvements": ["Consider adding more specific examples of achievements"],
                "missing_skills": ["Additional skills may be needed for your target role"],
                "wording_suggestions": ["Use action verbs to start each bullet point"]
            }
        
        # Parse the response
        response_json = response.json()
        
        # Check if the response has the expected structure
        if 'choices' not in response_json:
            st.error(f"Unexpected API response format: {response_json}")
            return {
                "strengths": ["Resume contains relevant technical skills"],
                "improvements": ["Consider adding more specific examples of achievements"],
                "missing_skills": ["Additional skills may be needed for your target role"],
                "wording_suggestions": ["Use action verbs to start each bullet point"]
            }
        
        if not response_json['choices']:
            st.error("No choices returned in API response")
            return {
                "strengths": ["Resume contains relevant technical skills"],
                "improvements": ["Consider adding more specific examples of achievements"],
                "missing_skills": ["Additional skills may be needed for your target role"],
                "wording_suggestions": ["Use action verbs to start each bullet point"]
            }
        
        content = response_json['choices'][0]['message']['content']
        analysis = json.loads(content)
        return analysis
        
    except json.JSONDecodeError:
        st.error("Error: LLM response is not in valid JSON format")
        return {
            "strengths": ["Resume contains relevant technical skills"],
            "improvements": ["Consider adding more specific examples of achievements"],
            "missing_skills": ["Additional skills may be needed for your target role"],
            "wording_suggestions": ["Use action verbs to start each bullet point"]
        }
    except Exception as e:
        st.error(f"Error in LLM analysis: {str(e)}")
        # Return a default response if there's an error
        return {
            "strengths": ["Resume contains relevant technical skills"],
            "improvements": ["Consider adding more specific examples of achievements"],
            "missing_skills": ["Additional skills may be needed for your target role"],
            "wording_suggestions": ["Use action verbs to start each bullet point"]
        }

def main():
    st.title("📄 Resume Analyzer AI Agent")
    st.write("Upload your resume and get AI-powered analysis and improvement suggestions")
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("How it works")
        st.write("""
        1. Upload your resume (PDF) or paste text
        2. Enter your target job role
        3. Get AI analysis of your resume
        4. Receive improvement suggestions
        """)
        
        st.header("Supported Formats")
        st.write("- PDF files")
        st.write("- Plain text")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Resume Input")
        input_method = st.radio("Choose input method:", ("PDF Upload", "Text Input"))
        
        resume_text = ""
        if input_method == "PDF Upload":
            uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
            if uploaded_file is not None:
                resume_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF uploaded and processed successfully!")
        else:
            resume_text = st.text_area("Paste your resume text here:", height=300)
    
    with col2:
        st.header("Target Job Role")
        target_job = st.text_input("Enter your target job role:", placeholder="e.g., Software Engineer, Data Scientist, Product Manager")
    
    # Process button
    if st.button("Analyze Resume", disabled=(not resume_text or not target_job)):
        with st.spinner("Analyzing your resume..."):
            # Extract information
            skills = extract_skills(resume_text)
            education = extract_education(resume_text)
            work_experience = extract_work_experience(resume_text)
            
            # Analyze with LLM
            analysis = analyze_resume_with_llm(resume_text, target_job)
            
            # Store results in session state
            st.session_state.analysis_results = {
                'skills': skills,
                'education': education,
                'work_experience': work_experience,
                'analysis': analysis,
                'target_job': target_job
            }
    
    # Display results if available
    if st.session_state.analysis_results:
        st.header("📊 Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["Resume Summary", "Skills", "Education & Experience", "AI Suggestions"])
        
        with tab1:
            st.subheader(f"Resume Analysis for {results['target_job']}")
            st.markdown("**Extracted Information:**")
            st.write(f"- **Skills found:** {len(results['skills'])}")
            st.write(f"- **Education entries:** {len(results['education'])}")
            st.write(f"- **Work experiences:** {len(results['work_experience'])}")
        
        with tab2:
            st.subheader("Skills Identified")
            if results['skills']:
                for skill in results['skills']:
                    st.write(f"- {skill}")
            else:
                st.write("No skills identified. Try improving the format of your resume.")
        
        with tab3:
            st.subheader("Education")
            if results['education']:
                for edu in results['education']:
                    st.write(f"- {edu}")
            else:
                st.write("No education information found.")
            
            st.subheader("Work Experience")
            if results['work_experience']:
                for exp in results['work_experience']:
                    st.write(f"- {exp}")
            else:
                st.write("No work experience found.")
        
        with tab4:
            st.subheader("AI-Powered Suggestions")
            
            with st.expander("Strengths", expanded=True):
                for strength in results['analysis']['strengths']:
                    st.write(f"- {strength}")
            
            with st.expander("Areas for Improvement", expanded=True):
                for improvement in results['analysis']['improvements']:
                    st.write(f"- {improvement}")
            
            with st.expander("Missing Skills", expanded=True):
                for missing_skill in results['analysis']['missing_skills']:
                    st.write(f"- {missing_skill}")
            
            with st.expander("Wording & Formatting Suggestions", expanded=True):
                for suggestion in results['analysis']['wording_suggestions']:
                    st.write(f"- {suggestion}")

if __name__ == "__main__":
    main()