import google.generativeai as genai
import textwrap

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)

GOOGLE_API_KEY="AIzaSyDXgb_tauJ6Au_puSi0Lqht1nRuFskOkHQ" #userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


model = genai.GenerativeModel('gemini-pro',)

response = model.generate_content("What is the meaning of life?")

print(response.text)