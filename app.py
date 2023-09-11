import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key here
api_key = os.environ.get("ENV_VARIABLE_NAME")

# Function to generate text using the GPT-3.5 Turbo engine
def generate_text(prompt, context, gptmodel):
    if api_key is None:
        return jsonify({"error": "OpenAI API key not provided"}), 500

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=gptmodel, # "gpt-3.5-turbo",  # "gpt-4", #Use the GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": context}, # e.g. context "You are a professional tech blogging assistant."
                {"role": "user", "content": prompt} # e.g. propmt "Generate a 160 word article on theory of relativity."
            ]
        )

        generated_text = response.choices[0].message["content"].strip()
        return generated_text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate_text', methods=['POST'])
def api_generate_text():
    data = request.get_json()
    prompt = data.get('prompt')
    context = data.get('context')
    gptmodel = data.get('gptmodel')

    if not prompt or not context or not gptmodel:
        return jsonify({"error": "Missing 'prompt', 'context' or 'gptmodel' parameter"}), 400 ### or 'context' or gptmodel NEW ###

    prompt = f"\"{prompt}\"." # Formatted to make it easy to insert texts e.g. f"Please explain the theory of relativity"
    context = f"\"{context}\"."
    generated_text = generate_text(prompt, context, gptmodel)

    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=False)
