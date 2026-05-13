import google.generativeai as genai

# PUT YOUR REAL KEY INSIDE THE QUOTES BELOW:
MY_KEY = "AIzaSyDF5pMlWvr21o_uTB8Ep8789x213A23zpk" 

print("Attempting to contact Google...")
try:
    genai.configure(api_key=MY_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say the word 'Mango'.")
    print("\n✅ SUCCESS! Google replied:", response.text)
except Exception as e:
    print("\n❌ ERROR:", e)