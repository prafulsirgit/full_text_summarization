import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import UPLOAD_FOLDER, MAX_FILE_SIZE
from models.model_loader import load_or_finetune_pegasus, load_or_finetune_bert, load_or_finetune_legalbert
from models.summarizer import summarize_with_pegasus, summarize_with_bert, summarize_with_legalbert
from utils.text_extraction import extract_text_from_pdf, extract_text_from_image
from utils.model_selector import choose_model

app = Flask(__name__)
CORS(app)

# Load models
pegasus_tokenizer, pegasus_model = load_or_finetune_pegasus()
bert_tokenizer, bert_model = load_or_finetune_bert()
legalbert_tokenizer, legalbert_model = load_or_finetune_legalbert()

@app.route('/summarize', methods=['POST'])
def summarize_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": f"File size exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB"}), 413
    file.seek(0)

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith(('.png', '.jpeg', '.jpg')):
            text = extract_text_from_image(file_path)
        else:
            os.remove(file_path)
            return jsonify({"error": "Unsupported file format. Use PDF, PNG, or JPEG."}), 400
        
        if not text.strip():
            os.remove(file_path)
            return jsonify({"error": "No text extracted from the file"}), 400
        
        model = choose_model(text)
        summary_length = request.form.get('length', 'normal')
        if model == "pegasus":
            summary = summarize_with_pegasus(text, pegasus_tokenizer, pegasus_model, summary_length)
        elif model == "bert":
            summary = summarize_with_bert(text, bert_tokenizer, bert_model)
        elif model == "legalbert":
            summary = summarize_with_legalbert(text, legalbert_tokenizer, legalbert_model)
        
        os.remove(file_path)
        return jsonify({"model_used": model, "summary": summary})
    
    except Exception as e:
        os.remove(file_path)
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)