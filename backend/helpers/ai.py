import PyPDF2
from openai import OpenAI
import docx
import os


client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))


def get_summary(text):
    try:
        response = client.completions.create(
            model="gpt-4.1-nano",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def summarize_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    summary = get_summary(text)
    return summary


def summarize_docx(docx_file_path):
    doc = docx.Document(docx_file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"

    summary = get_summary(text)
    return summary


def summarize_text(plain_text):
    summary = get_summary(plain_text)
    return summary


def summarize_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            "whisper-1", audio_file
        )

    text = transcript["text"]

    response = client.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes transcribed audio."},
            {"role": "user", "content": f"Summarize this audio transcript:\n\n{text}"}
        ],
        temperature=0.5
    )

    return response['choices'][0]['message']['content']
