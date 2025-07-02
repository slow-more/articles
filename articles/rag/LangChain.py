from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
import os
from google.colab import userdata

# 環境変数設定
os.environ["OPENAI_API_KEY"] = userdata.get('OPEN_API_KEY')
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.0)
# OpenAIの埋め込みモデルを使用
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 質問
query = "クラス°サービスの年間利用者数の目標は？"

# ファイルの読み込み
with open('sample_document.txt', 'r', encoding='utf-8') as file:
    document_text = file.read()
# 文書を300文字ごとに分割し50文字のオーバラップを設定
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
# 文書を分割
texts = text_splitter.split_text(document_text)

# 分割したテキストをベクトルストアに変換
vector_store = FAISS.from_texts(texts, embeddings)

# 質問をベクトルに変換
docs = vector_store.similarity_search(query, k=5)

top_texts = [doc.page_content for doc in docs]
# 回答生成のためのプロンプトを作成
print(f"上位５件:{top_texts}")

response_prompt = f'''以下の「質問」に対し、「情報」の内容を元に答えて下さい。
### 質問 ###
{query}
### 質問終了 ###
### 情報 ###
{top_texts[0]}
{top_texts[1]}
{top_texts[2]}
{top_texts[3]}
{top_texts[4]}
### 情報終了 ###
'''
# AIモデルを使って回答を生成
response = llm.generate([response_prompt])

print(response.generations[0][0].text.strip())