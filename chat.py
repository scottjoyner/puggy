import json
import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, Response, request, stream_with_context, make_response, send_from_directory
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from flask_cors import CORS, cross_origin
# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're a world class assistant"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}"),
    ]
)


def generate_tokens(question):
    chain = prompt | llm | StrOutputParser()
    for chunks in chain.stream({"chat_history": [], "question": question}):
        yield chunks



@app.route('/<path:filename>', methods=['GET'])
# @cross_origin()
def serve_file(filename):
    return send_from_directory("/home/deathstar/git/puggy/docs", filename)



@app.route("/llama3/chat", methods=["POST"])
def ask_ai():
    @stream_with_context
    def generate_json(question):
        with app.app_context():  # Ensure we're within the application context
            full_content = ""
            for token in generate_tokens(question):
                full_content += token
                # yield token
                print(token, end="")
                json_data = {"model": OLLAMA_MODEL, "content": token, "done": False}
                json_str = json.dumps(json_data)  # Convert JSON data to a string
                json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
                yield json_bytes
                yield b"\n"  # Yield newline as bytes

            # Once streaming is finished, yield one last JSON object with "done" set to True
            json_data = {
                "model": OLLAMA_MODEL,
                "full_content": full_content,
                "done": True,
            }
            json_str = json.dumps(json_data)  # Convert JSON data to a string
            json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
            yield json_bytes

    request_data = request.json
    question = request_data.get("question")
    return Response(generate_json(question), mimetype="application/json")


@app.route("/llama3-2/chat", methods=["POST"])
def ask_ai_2():
    def generate_json(question):
        with app.app_context():  # Ensure we're within the application context
            full_content = ""
            for token in generate_tokens(question):
                full_content += token
                # yield token
                # print(token, end="")
                # json_data = {"model": OLLAMA_MODEL, "content": token, "done": False}
                # json_str = json.dumps(json_data)  # Convert JSON data to a string
                # json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
                # yield json_bytes
                # yield b"\n"  # Yield newline as bytes

            # Once streaming is finished, yield one last JSON object with "done" set to True
            json_data = {
                "model": OLLAMA_MODEL,
                "full_content": full_content,
                "done": True,
            }
            json_str = json.dumps(json_data)  # Convert JSON data to a string
            json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
            yield json_bytes

    request_data = request.json
    question = request_data.get("question")
    return Response(generate_json(question), mimetype="application/json")

# @app.route("/llama3/chat", methods=["POST"])
# #@cross_origin()
# async def ask_ai():

#     def generate_json(question):
#         with app.app_context():  # Ensure we're within the application context
#             full_content = ""
#             for token in generate_tokens(question):
#                 full_content += token
#                 print(full_content)
#                 json_data = {"model": OLLAMA_MODEL, "content": token, "done": False}
#                 json_str = json.dumps(json_data)  # Convert JSON data to a string
#                 json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
#                 yield json_bytes
#                 yield b"\n"  # Yield newline as bytes

#             # Once streaming is finished, yield one last JSON object with "done" set to True
#             json_data = {
#                 "model": OLLAMA_MODEL,
#                 "full_content": full_content,
#                 "done": True,
#             }
#             json_str = json.dumps(json_data)  # Convert JSON data to a string
#             json_bytes = json_str.encode("utf-8")  # Encode JSON string to bytes
#             yield json_bytes

#     request_data = request.json
#     question = request_data.get("question")
#     return Response(
#         # generate_json(question), mimetype="application/json" application/stream+json
#         stream_with_context(generate_json(question)), 
#         mimetype="application/json"
#         # headers={
#         #     "Access-Control-Allow-Origin":"*",
#         #     'Access-Control-Allow-Headers':"*",
#         #     'Access-Control-Allow-Methods':"*",
#         #     'Content-type': "application/stream+json"
#         # }
#     )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)