import streamlit as st

# Read a single document
def ReadSingleDoc(container, document_id, partition_key)    :
    document = container.read_item(item=document_id, partition_key=partition_key)
    st.write(document)


# Execute a query against a Cosmos DB container
def ExecuteQuery(container, query):
    
    return list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

# Upsert a document in Cosmos DB
def UpsertDocument(container, document):
    container.upsert_item(body=document)


# Delete a document in Cosmos DB
def DeleteDocument(container, document_id, partition_key):
    container.delete_item(item=document_id, partition_key=partition_key)
    