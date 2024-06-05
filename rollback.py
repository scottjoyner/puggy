from flask import Flask, Response, request, stream_with_context
import json
import os

app = Flask(__name__)

@app.route('/llama3/chat', methods=['GET'])
def ask_ai():
    question = request.args.get('question')
    def generate():
        full_content = ""
        for token in generate_tokens(question):
            full_content += token
            json_data = {"model": OLLAMA_MODEL, "content": token, "done": False}
            yield f"data: {json.dumps(json_data)}\n\n"
        json_data = {"model": OLLAMA_MODEL, "full_content": full_content, "done": True}
        yield f"data: {json.dumps(json_data)}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
