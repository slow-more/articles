from openai import OpenAI
import numpy as np 
import os 
from sklearn.metrics.pairwise import cosine_similarity
from google.colab import userdata 
# 環境変数設定
os.environ["OPENAI_API_KEY"] = userdata.get('OPEN_API_KEY') 
ai_client = OpenAI() 
# 質問 
query = "クラウドサービスの年間利用者数の目標は？" 
# 回答の元とする情報 
# ファイルの読み込み
with open('sample_document.txt', 'r', encoding='utf-8') as file:
  document_text = file.read()

def split_text_with_overlap(text, chunk_size, overlap):
  chunks = []
  for i in range(0,len(text), chunk_size - overlap):
    chunks.append(text[i:i+chunk_size])
  return chunks

# 文書を300文字ごとに分割し50文字のオーバラップを設定
info = split_text_with_overlap(document_text, 300,50)

# 質問をベクトルに変換 
query_response = ai_client.embeddings.create( 
  input=query, 
  model="text-embedding-3-small" ) 
query_vector = query_response.data[0].embedding

# 情報をベクトルに変換 
text_vectors = [] 
for text in info: 
  response = ai_client.embeddings.create(
    input=text,
    model="text-embedding-3-small" ) 
  text_vectors.append(response.data[0].embedding)

# 類似度計算 
similarity_scores = cosine_similarity([query_vector], text_vectors)[0] 

# 上位5つ
top_indices = np.argsort(similarity_scores)[-5:][::-1]
# 上位5件のテキスト表示
top_texts = [info[i] for i in top_indices]
print(f"類似度が高い上位５件の情報: {top_texts}")

# 回答生成のためのプロンプトを作成 
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
response = ai_client.completions.create( 
  model="gpt-3.5-turbo-instruct", 
  prompt=response_prompt,
  max_tokens=200,
  temperature=0.0 )
# AIの回答を表示
print(response.choices[0].text)