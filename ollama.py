from flask import Flask, render_template, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

app = Flask(__name__) #flask 第一步創建核心

# 初始化模型
model = OllamaLLM(model="LLAMA3.2:1B")  #這裡可以改 自己選擇llama3.2:1b模型 因為沒太多時間 這最小


template = """
answer the question below

Here is the conversation history: {context}

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        context = ""  # 可以從數據庫或其他地方加載歷史對話
        question = request.form["question"]
        chain = prompt | model
        result = chain.invoke({"context": context, "question": question})

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
