from src.data_loader import load_pdf
from src.vectorstrore import VectorStore
from src.search import RAGretriever
from flask import Flask, jsonify, request
from src.auth import require_api_key


app = Flask(__name__)

retriever = None
def init_retriever():
    global retriever
    retriever = RAGretriever()
    print("RAG retriever initialized")

init_retriever()
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/query', methods=['POST'])
def query_rag():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "Query is required"}), 400

        response = retriever.generate_response(query)
        if not response:
            return jsonify({"error": "No response generated"}), 500

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploadPdf',methods=['POST'])
@require_api_key
def add_new_data():
    try:
        if "file" not in request.files:
            return {"error": "No file part"}, 400

        file = request.files["file"]
        if file.filename == "":
            return {"error": "No selected file"}, 400

        if not file.filename.endswith(".pdf"):
            return {"error": "Only PDFs allowed"}, 400

        all_docs = load_pdf(file)
        if not all_docs:
            return jsonify({"error": "File uploaded failed"}), 500
        
        vector_store = VectorStore()
        vectorResponse=vector_store.add_documents(all_docs)

        if not vectorResponse:
            return jsonify({"error": "File uploaded failed"}), 500
        
         # 🔁 IMPORTANT: Reinitialize retriever
        init_retriever()
        return jsonify({"message": "File uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deleteCollection', methods=['GET'])
@require_api_key    
def delete_collection():
    try:
        vector_store = VectorStore()
        result = vector_store.delete_collection()
        if not result:
            return jsonify({"error": "Collection deletion failed"}), 500

        return jsonify({"message": "Collection deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





