import google.generativeai as genai

genai.configure(api_key="AIzaSyB60Ngf-F6a4d5o9zg31HaUrlmabaFYZNc")

for m in genai.list_models():
    print(m.name)