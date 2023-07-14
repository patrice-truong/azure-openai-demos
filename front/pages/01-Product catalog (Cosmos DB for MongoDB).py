import json
import csv
import time
from datetime import datetime, timedelta
import streamlit as st
from dotenv import load_dotenv
import os
import tiktoken
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, generate_container_sas, ContentSettings
from services.aoai import generate_embeddings, generate_embeddings_from_text

from services.cosmosdb_mongodb import count_products, insert_many, similar
from services.data import get_data, post_data
from models.product import Product

BATCH_SIZE = 1000
MIN_SCORE = 0.8
EMBEDDING_ENCODING = 'cl100k_base'

load_dotenv()


def search_for(search_text):
    # create embedding
    start = time.time()
    result = generate_embeddings_from_text(search_text)
    if(result.status_code == 500):
        st.write ("Error 500 :-( ")
    else:
        query_vector = result.json()["embeddings"]
        end = time.time()
        st.write(f"Vector generated in {end - start} sec, using text-embedding-ada-002")

        # search for embedding
        start = time.time()
        st.write(f"Searching for documents similar to '{search_text}'")
        result = similar(query_vector, limit=5, min_score=MIN_SCORE)
        matching_products = result.json()
        end = time.time()
        st.write(f"Search completed in {end - start} sec")

        # display matching images
        sas = generate_container_sas(
            os.getenv('BLOB_ACCOUNT_NAME'), 
            os.getenv('BLOB_CONTAINER_NAME'),
            os.getenv('BLOB_ACCOUNT_KEY'),  
            permission="r", 
            expiry=datetime.utcnow() + timedelta(hours=3))

        found = False
        if len(matching_products) > 0:
            st.markdown(f"<span class='green bold'>Found article(s) with similarity > {MIN_SCORE}</span>", unsafe_allow_html=True)
            found = True
            # Create a table with 5 columns
            columns = st.columns(5)
            # Display each image in a separate column
            for i, image in enumerate(matching_products):
                with columns[i]:
                    updated_image_path = image['image_path'].replace('assets/', 'data/assets/')
                    image_url = f"{updated_image_path}?{sas}"
                    st.image(image_url, width=200)

            st.json(matching_products)
        
        if not found:
            st.markdown("<span class='red bold'>No Match</span>", unsafe_allow_html=True)



title = "Product catalog search"
styles = """
            <style>
            .green { color: green }
            .red { color: red }
            .bold { font-weight: bold }
            </style>
            """
st.markdown(styles, unsafe_allow_html=True)
st.header(title)

st.write("#### Scenario")
st.write("This page demonstrates how to use Cosmos DB for MongoDB to search for products in a product catalog. The product catalog is stored in a Cosmos DB database. The product catalog is enriched with embeddings computed by OpenAI. The search is performed by Cosmos DB for MongoDB and will return articles with a similarity ratio > 80%")

st.write(f"There are embeddings for <span class='red bold'>{count_products()}</span> products in the Cosmos DB for MongoDB collection", unsafe_allow_html=True)
if st.button("Load products from csv into Cosmos DB for MongoDB and compute embeddings"):
    # Using batching (works in OpenAI but not in Azure OpenAI)
    # Define a batch size for the API calls
    engine = os.getenv("OPENAI_EMBEDDINGS_ENGINE_DOC")
    articles = os.getenv("ARTICLES")
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
    IMAGE_BASE = f"https://{os.getenv('BLOB_ACCOUNT_NAME')}.blob.core.windows.net/assets"
    products = []

    
    # Open the CSV file
    with open(articles, 'r', encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')

        # Skip the first row
        next(csv_reader)

        # Create a list to store the Product objects
        for linenumber, row in enumerate(csv_reader):
            # Create a Product object from the row data
            product = Product(*row)
            product.image_path = f"{IMAGE_BASE}/{product.article_id[:3]}/{product.article_id}.jpg"

            # Convert the Product object to a JSON document
            productJson = product.to_json()
            
            # add product to list
            products.append(product)


        #  Compute embeddings in batches
        for i in range(0, len(products), BATCH_SIZE):

            # Extract the details for the current batch of products
            st.write(f"Computing embeddings for products {i} to {i + BATCH_SIZE}")
            batch = products[i:i + BATCH_SIZE]

            # batch_ids = [product.article_id for product in batch]
            # batch_values_to_vectorize = json.dumps([to_json(product) for product in batch])
            batch_values_to_vectorize = [product.__dict__ for product in batch]

            # Call the getEmbedding API with the batch details
            response = generate_embeddings(batch_values_to_vectorize)
            if response.status_code == 200:
                embeddings = response.json()

                # Map the embeddings back to the corresponding articles
                j = 0
                updated_products = []
                for j, obj in enumerate(embeddings):
                    product = batch[j]

                    product.vectorContent = obj["embedding"]
                    updated_products.append(product)
            
                # Save the updated products to Cosmos DB for MongoDB
                p = [product.__dict__ for product in updated_products]
                insert_many(p)

        st.write("Finished !")
            
    # article_id,product_code,prod_name,product_type_no,product_type_name,product_group_name,graphical_appearance_no,graphical_appearance_name,colour_group_code,colour_group_name,perceived_colour_value_id,perceived_colour_value_name,perceived_colour_master_id,perceived_colour_master_name,department_no,department_name,index_code,index_name,index_group_no,index_group_name,section_no,section_name,garment_group_no,garment_group_name,detail_desc


        

# ---------------- Search articles ----------------
st.write("#### Search product catalog")

search_text = st.text_input("Look for similar products. Try sunglasses, beige cargo pants, pink t-shirt, handbag with shoulder strap...", placeholder="Look for similar products")

# create a table with 6 columns
# in each column, add a button
# when the button is clicked, search for the text in the button
columns = st.columns(6)
if columns[0].button("Search"):
    st.write(f"Generating embedding for '{search_text}'")
    search_for(search_text)
if columns[1].button("Beige pants"):
    search_for("Beige cargo pants")
if columns[2].button("Pink T-Shirt"):
    search_for("Pink T-Shirt")
if columns[3].button("Sunglasses"):
    search_for("Sunglasses")
if columns[4].button("handbag with shoulder strap"):
    search_for("handbag with shoulder strap")
    