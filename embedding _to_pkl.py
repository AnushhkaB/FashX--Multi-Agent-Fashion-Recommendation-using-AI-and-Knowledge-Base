import neo4j
import numpy as np
import pickle

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "fashion@123"  # Replace with your actual password

# Connect to Neo4j
driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))

def retrieve_and_process_embeddings():
    with driver.session() as session:
        result = session.run("""
            MATCH (i:Item)
            RETURN i.article_id AS article_id,
                   i.prod_name AS prod_name,
                   i.colour_group_name AS colour_group_name,
                   i.department_name AS department_name,
                   i.detail_desc AS detail_desc,
                   i.garment_group_name AS garment_group_name,
                   i.index_group_name AS index_group_name,
                   i.perceived_colour_master_name AS perceived_colour_master_name,
                   i.product_group_name AS product_group_name,
                   i.image_embedding AS image_embedding
        """)
        embeddings_data = []
        for record in result:
            embedding = record["image_embedding"]
            # Convert Neo4j list to NumPy array (or None if embedding is null)
            embedding_array = np.array(embedding, dtype=np.float32) if embedding is not None else None
            embeddings_data.append({
                "article_id": record["article_id"],
                "prod_name": record["prod_name"],
                "colour_group_name": record["colour_group_name"],
                "department_name": record["department_name"],
                "detail_desc": record["detail_desc"],
                "garment_group_name": record["garment_group_name"],
                "index_group_name": record["index_group_name"],
                "perceived_colour_master_name": record["perceived_colour_master_name"],
                "product_group_name": record["product_group_name"],
                "image_embedding": embedding_array
            })
        return embeddings_data

# Retrieve and process the embeddings
embeddings_data = retrieve_and_process_embeddings()

# Save to pickle file
with open('image_embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings_data, f)

print("Embeddings saved to 'image_embeddings.pkl'")

# Close the driver connection
driver.close()