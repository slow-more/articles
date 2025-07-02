from openai import OpenAI
import numpy as np 
import os 
from sklearn.metrics.pairwise import cosine_similarity
from google.colab import userdata 
# 環境変数設定
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY') 
ai_client = OpenAI() 
# 質問 
query = "今年の夏はどこに行く予定ですか？" 
# 回答の元とする情報 
info = [ "昨年の夏に北海道旅行を計画していた。レンタカーで観光地を回る予定だった。", "今年の春には海外旅行を計画中で、ヨーロッパが候補に挙がっている。ヨーロッパは２回目。", "今年の夏は軽井沢に行く予定である。キャンプをする。キャンプは初めて。", ] 
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

print(query_vector)
print(text_vectors)
# 類似度計算 
similarity_scores = cosine_similarity([query_vector], text_vectors)[0] 
best_match_index = np.argmax(similarity_scores)
print(similarity_scores)
print(best_match_index)
# 回答生成のためのプロンプトを作成 
response_prompt = f'''以下の「質問」に対し、「情報」の内容を元に答えて下さい。 
### 質問 ### 
{query} 
### 質問終了 ###
### 情報 ###
{info[best_match_index]}
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