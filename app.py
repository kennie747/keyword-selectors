import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key here
api_key = os.environ.get("ENV_VARIABLE_NAME")

# Function to generate text using the GPT-3.5 Turbo engine
def generate_text(prompt):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # "gpt-4", #Use the GPT-3.5 Turbo model
        messages=[
            {"role": "system", "content": "You are a professional tech blogging assistant."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": "Generate a list of 10 HIGHLY RELEVANT Key-phrases (BETWEEN 2 TO 4 words long) for the previous post, sort the list in descending order of relevance and label it *Keywords*, and make it comma separated with NO nunbering"}
        ]
    )

    generated_text = response.choices[0].message["content"].strip()
    return generated_text

@app.route('/generate_text', methods=['POST'])
def api_generate_text():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Missing 'prompt' parameter"}), 400

    prompt = f"\"{prompt}\"." # Formatted to make it easy to insert any preceeding text as shown the comment below
    # f"Please rewrite the following tech blog post in a unique and original way while preserving all the information and key points; if there are images in the original post, retain them and add appropriate attribution; conclude with a list of 10 HIGHLY RELEVANT Key-phrases (BETWEEN 2 TO 4 words long) for the post, sorted in descending order of relevance and label the list *Keywords*, comma separated with NO nunbering: \"{text}\"."
    generated_text = generate_text(prompt)

    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
