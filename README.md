
# 👔FashX: Multi-Agent AI for Personalized Fashion Assistance with Graph Intelligence

FASHX is an end-to-end, AI-driven fashion recommendation system designed to deliver highly personalized item suggestions by blending graph analytics, deep embedding similarity, and real-time trend analysis. At its core, FASHX stores **Users**, **Items**, and their **Interactions** in a Neo4j graph database, allowing us to capture complex relationships such as co-purchases and user behavior pathways.  

- **Why Graph?**  
  Traditional relational approaches struggle to traverse many-to-many relationships efficiently. By using Neo4j, FASHX natively represents each user and item as nodes, linked by `INTERACTED_WITH` and `BOUGHT_TOGETHER` edges. This structure lets us run powerful graph algorithms (e.g., community detection, similarity scoring) via APOC and the Graph Data Science library for lightning-fast in-database analytics.

- **Embedding-Powered Similarity**  
  We extract visual embeddings for each item (e.g., clothing images) and store them either directly in Neo4j or in an external `.pkl` file. These vector embeddings enable cosine-similarity queries so you can find visually similar items or cluster products by style.


- **Conversational Multi-Agent Interface**  
  A powerfull LLM <here, Llama 3 8B>–powered agent provides a natural language “front-end” for your recommendation graph. Ask questions like “What new summer tops does Anna (age 28) like?” or “Show me outfits similar to Item #12345,” and the agent orchestrates graph queries, embedding retrieval, and trend insights to deliver coherent, actionable responses.

(For any issues for running this system in your system, please refer to the REQUIREMENTS -PROJECT.txt)
## Screenshots

![App Screenshot](https://github.com/roanek123/FashX--Multi-Agent-Fashion-Recommendation-using-AI-and-Knwledge-Base/blob/main/GRADIO%20PAGE.png)


## 🔍 Features
Our system provides a variety of novel feautures, focusing on acheiving accurate fashion recommendation for the user:

1. **Graph-Based Data Modeling**  
   - Nodes for `User`, `Item` and Relationships `INTERACTED_WITH`, `BOUGHT_TOGETHER`  
   - Uniqueness constraints and indexes ensure data integrity and query performance  
   - Leverages APOC procedures and GDS algorithms for community detection, node embeddings, and path analysis
![App Screenshot](https://github.com/roanek123/FashX--Multi-Agent-Fashion-Recommendation-using-AI-and-Knowledge-Base/blob/main/new%20graph%20diagram.png?raw=true)
  

2. **Embeddings Support**  
   - Stores high-dimensional image embeddings in Neo4j or as an external `Item_data.pkl`  
   - Cosine-similarity retrieval for “more like this” recommendations  
   - Offline mode for bulk Python-based processing  

3. **Flexible Retrieval Methods**  
   - **Neo4j-Direct**: Real-time graph + embedding queries in the database  
   - **Offline Embeddings**: Load `Item_data.pkl` into Python (Colab/VSCode) for faster, repeatable batch queries  

4. **Trend Analysis Agent (Beta)**  
   - Groq **compound-beta** model scrapes multiple real-time sources (social media, news, blogs)  
   - Identifies trending categories, colors, and styles  
   - Automatically adjusts recommendation weights  

5. **Multi-Agent LLM Interaction**  
   - **Llama 3 8B** handles conversational logic and orchestrates backend calls  
   - Switchable retrieval strategies (graph vs. embeddings) per query  

6. **Interactive UI**  
   - **Gradio** interface for quick demos and user testing  
   - Both CLI and web-based front-ends supported  
   - GPU acceleration optional in Colab  



## 🧠 Key Components
This system is composed of several components collaborate to run this system efficiently:

- **Neo4j Desktop Project**  
  - Local DBMS v5.24.2 with APOC 5.24.2 & GDS 2.12.0 plugins  
  - Tuned JVM heap (`2 GB` initial, `4 GB` max)  
  - Enabled security allowlist for procedures:  
    ```properties
    dbms.memory.heap.initial_size=2G
    dbms.memory.heap.max_size=4G
    dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,gds.*
    ```

- **Cypher Loader Scripts**  
  - **Constraints & Indexes**: Uniqueness for `article_id` and `customer_id`, plus property indexes  
  - **CSV Ingestion**: Articles, customers, transactions, co-purchases, image embeddings  

- **Python Utilities**  
  - `embeddings_to_pkl.py`: Extracts image embeddings from Neo4j into `Item_data.pkl`  
  - `fashx.py` / `fashx_final.py`: Core orchestrator for database access, Groq API, and Llama agents  

- **Agents & Models**  
  - **Llama 3 8B**: Conversational retrieval agent, used for the testing of this system.
  - **Groq compound-beta**: Real-time trend analysis.

- **UI Layer**  
  - **Gradio**: Rapid prototyping UI in Python (supports GPU in Colab)

- **LocalHost Tunneling through ngrok**  
  - **ngrok http 7474**:    Uses ngrok tunneling feature to expose the neo4j localhost to the internet for the colab to connect to.

- **Trend Analysis Agent (Beta)**  
   - Groq **compound-beta** model scrapes multiple real-time sources (social media, news, blogs)  
   - Identifies trending categories, colors, and styles  
   - Automatically adjusts recommendation weights 
## 🛠️ Installation Guide

Follow the steps below to set up the environment for running the FashX Recommendation system.

---


### 📦 Step 1 Clone the repository
   ```bash
   git clone <repo-url>
   cd fashx-recommendation
```

### Step 2. Neo4j Setup

- Download & install [Neo4j Desktop](https://neo4j.com/download/)
- Create a new project → **ADD** → **Local DBMS** v5.24.2
- Set DB name & password, install **APOC 5.24.2** and **GDS 2.12.0**
- In the **Settings** tab of your DB, paste the following configuration:

```properties
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,gds.*
```

---

### Step 3. Data Loading

Place the following CSV files in the `import/` folder of your Neo4j installation: (PRESENT IN THE NEO4J CSV, NEO4J_CSV-2.ZIP, NEO4J_CSV-3.ZIP FOLDERS)
- `articles_filtered.csv`
- `customers_filtered.csv`
- `transactions_filtered.csv`
- `co_purchases.csv`
- `image_embedding.csv`

Then, run the provided Cypher script in order to: (in cypher queries.txt)
- Create necessary constraints and indexes
- Load data into the graph

---

### Step 4. Python Environment, in colab

```bash
!pip install -r requirements.txt
```

---

### Step 5. (Optional) Export Embeddings to PKL
change the noe4j username and pass in the embeddings_to_pkl.py file

```bash
python embeddings_to_pkl.py
```

> This will generate `Item_data.pkl` for use in offline retrieval.

---

### ⚠️ Notes

- The above steps are to setup the neo4j database.
- Next topic will the rest of the setup and running of file.
## 🧪Run the System


### 1. Start Neo4j

- Open **Neo4j Desktop** and start your DB instance.

---

### 2. Expose Locally via Ngrok

```bash
ngrok http 7474
```

- Copy the forwarding URL (e.g., `https://xxxxx.ngrok.io`)  
- Replace the Neo4j URI in `fashx_final.py` which is opened in colab with this URL

---

### 3. Set Environment Variables in colab

```bash
NEO4J_URI="bolt://<host>:7687"
NEO4J_USER="<username>" # by default the username and password are neo4j
NEO4J_PASSWORD="<password>"
API_KEY="<your-groq-api-key>"
```

---

### 4. Launch the App

- Upload the files (PRESENT IN COLAB UPLOAD FOLDER) to colab.

- Then run the code blocks.

---

### 4. Select the mode for image embedding retreival.
We have 2 forms of image embedding data retrieval

(see the markdowns in fashx_final.py, 
(markdown code block, given in brackets here as well), 
for easier understanding, on which code block to run.)
- **Using Item_data.pkl**, which we got from the above OPTIONAL STEP (run embeddings_to_pkl.py). - (USING THE EMBEDDING FROM DATA.PKL)
- **Direct retrieval through neo4j** - (USING EMBEDDINGS DIRECTLY FROM NEO4J)

After choosing your method: 

the run the code blocks below this markdown( MAIN CODE------------------------)

---

### 5. Open the UI

- Open the Gradio URL provided in the output terminal
- Enter your preference and explore fashion recommendations

---
## 🎉Demo

(https://youtu.be/Fq-U_9faNq8)

You can look at the full working of this system through this link.

For a guided walkthrough, see our demo video. It includes:

1. **Data Showcase** in Neo4j   
2. (BETA) **Real-Time Trend Analysis** using `compound_beta` from Groq  
3. **Conversational Q&A** powered by Llama 3 8B.
4. **Muti Input processing** from the user data to get the recommendation.

## 🗺️ WorkFlow

The FashX system provides fashion product recommendations by integrating user behavior, product metadata, and image features through a graph-based and embedding-driven architecture.

---

### 1. **Data Preparation**
- Load structured data (`articles`, `customers`, `transactions`, `co_purchases`, `image_embedding`) into Neo4j.
- Create graph relationships:  
  `(:Customer)-[:PURCHASED]->(:Article)`  
  `(:Article)-[:RELATED_TO]->(:Article)`  
  `(:Article)-[:HAS_EMBEDDING]->(:Embedding)`

---

### 2. **Graph Construction & Enrichment**
- Use **APOC** for data manipulation and relationship creation.
- Apply **GDS algorithms** (e.g., Node Similarity) for collaborative filtering.
- Add visual similarity via image embeddings.

---

### 3. **Backend Recommendation Logic**
- Python backend fetches:
  - Customer's past purchases from neo4j.
  - Similar items based on:
    - Graph similarity (purchases & co-purchases).
    - Embedding similarity (offline `.pkl` or Neo4j live).
- Combines these scores to rank recommendations.

---

### 4. **Frontend UI**
- Gradio-based interface allows:
  - User input (text, speech and image)
  - Display of recommended fashion items.

---

### 5. **Enhancements**
- **Ngrok**: Local Neo4j exposure
- **Groq + Llama 3**: Real-time Q&A and trend insights via LLM

---
### ✅ Output
- User receives top-N recommended articles based on purchase history and visual similarity.

---
```



## Contributing
Contributions are always welcome!

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

#### ⚠️⚠️⚠️The following system is a realisation of hypothesis of an agentic system which can be used for a wide range of applications. As our aim is to help the showcase the power of agentic ai when integrated a knowledge graph base.


