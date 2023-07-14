from time import sleep
import streamlit as st
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken, requests, openai, os, json
from tenacity import retry, wait_random_exponential, stop_after_attempt
from transformers import GPT2Tokenizer

def initialize(engine='davinci'):
    openai.api_type = "azure"
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")    
    openai_personal_key = os.getenv("OPENAI_PERSONAL_KEY")

# Semantically search using the computed embeddings locally
def search_semantic(df, search_query, n=3, pprint=True, engine='davinci'):
    embedding = get_embedding(search_query, engine= get_embeddings_model()['query'])
    df['similarities'] = df[f'{engine}_search'].apply(lambda x: cosine_similarity(x, embedding))

    res = df.sort_values('similarities', ascending=False).head(n)
    if pprint:
        for r in res:
            print(r[:200])
            print()
    return res.reset_index()


def gpt3_completion(prompt, engine='davinci', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>'], context=""):
    max_retry = 5
    retry = 0
    while True:
        try:
            prompt = f"""
            {context} 
            
            Question: {prompt} 
            Answer:
            """
            headers = {
                'api-key': os.getenv("OPENAI_API_KEY"),
                'Content-Type': 'application/json'
            }

            data = {
                "model": engine,
                "prompt": prompt,
                "max_tokens": tokens,
                "temperature": temp
            }

            url = f"{os.getenv('OPENAI_API_BASE')}/openai/deployments/{engine}/completions?api-version=2022-12-01"

            response = requests.post(
                url, 
                headers = headers,
                data = json.dumps(data)
            )

            r = response.json()
            answer = r["choices"][0]["text"] 
            return answer
        
        except Exception as e:
            retry += 1
            if retry >= max_retry:
                return f"GPT3 error: {e}"
            print('Error communicating with OpenAI:', e)
            sleep(1)

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, engine="text-embedding-ada-002") -> list[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")
    EMBEDDING_ENCODING = 'cl100k_base' if engine == 'text-embedding-ada-002' else 'gpt2'
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
    return openai.Embedding.create(input=encoding.encode(text), engine=engine)["data"][0]["embedding"]

def get_openai_embedding(self, text: str, engine="text-embedding-ada-002") -> list[float]:

    text = text.replace("\n", " ")
    EMBEDDING_ENCODING = 'cl100k_base' if engine == 'text-embedding-ada-002' else 'gpt2'
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        'Content-Type': 'application/json',
        # Note: using personal OpenAI key here, to do embeddings batching
        # not yet available on Azure OpenAI API
        'Authorization': "Bearer " + self.openai_personal_key
    }

    return requests.post(
        url, 
        headers = headers,
        json = {
            'input': encoding.encode(text),
            'model': 'text-embedding-ada-002'
        }               
    ).json()["data"][0]["embedding"]
    


# Define the function to compute embeddings using the Azure OpenAI API
def compute_embeddings(article_desc_list, engine):
    embeddings = openai.Embedding.create(
        engine=engine,
        input=article_desc_list
    )
    return embeddings['embeddings']

def chunk_and_embed(text: str, filename="", engine="text-embedding-ada-002"):
    EMBEDDING_ENCODING = 'cl100k_base' if engine == 'text-embedding-ada-002' else 'gpt2'
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)

    full_data = {
        "text": text,
        "filename": filename,
        "search_embeddings": None
    }

    text = text.replace("\n", " ")
    lenght = len(encoding.encode(text))
    if engine == 'text-embedding-ada-002' and lenght > 2000:
        return None
    elif lenght > 3000:
        return None

    full_data['search_embeddings'] = get_embedding(text, engine)

    return full_data


def get_completion(prompt="", max_tokens=400, model="text-davinci-003"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    print(f"{response['choices'][0]['text'].encode().decode()}\n\n\n")

    return prompt,response#, res['page'][0]


def get_token_count(text: str):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return len(tokenizer(text)['input_ids'])


def get_embeddings_model():
    OPENAI_EMBEDDINGS_ENGINE_DOC = os.getenv('OPENAI_EMEBDDINGS_ENGINE', os.getenv('OPENAI_EMBEDDINGS_ENGINE_DOC', 'text-embedding-ada-002'))  
    OPENAI_EMBEDDINGS_ENGINE_QUERY = os.getenv('OPENAI_EMEBDDINGS_ENGINE', os.getenv('OPENAI_EMBEDDINGS_ENGINE_QUERY', 'text-embedding-ada-002'))
    return {
        "doc": OPENAI_EMBEDDINGS_ENGINE_DOC,
        "query": OPENAI_EMBEDDINGS_ENGINE_QUERY
    }


def add_embeddings(collection_name, text, filename, engine="text-embedding-ada-002"):
    embeddings = chunk_and_embed(text, filename, engine)
    if embeddings:
        # Store embeddings in Qdrant
        set_document(collection_name, embeddings)
    else:
        st.error("No embeddings were created for this document as it's too long. Please keep it under 3000 tokens")


def initialize():
    # Initialize OpenAI
    openai.api_type = "azure"
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    st.session_state["vision_base_endpoint"] = os.getenv("COMPUTER_VISION_ENDPOINT")
    st.session_state["vision_key"] = os.getenv("COMPUTER_VISION_KEY")