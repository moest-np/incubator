import csv
from walrus import Database
import re
import redis


# Initialize the database and create the search index.
redis_client = redis.StrictRedis()

# Flush the entire database to clear all keys. 
# There were multiple runs, so it confused the redis
redis_client.flushdb()

# Initialize the database.
db = Database()

search_index = db.Index('app-search')
phonetic_index = db.Index('phonetic-search', metaphone=True)

# Read the data from the first TSV file and index it.
with open(r"..//school_list_A.tsv", 'r', encoding='utf-8') as file1:
    reader = csv.DictReader(file1, delimiter='\t')
    print("Starting...")

    for row in reader:
        
        doc_id = row['school_id']
        content = row['velthuis']
        document_key = f"{doc_id}_search"  # Modify the document key based on your requirements
        document = {'content': content, 'id': doc_id}  # Include the 'id' inside the document
        search_index.add(document_key, **document)
        
        document_key = f"{doc_id}_phonetic"  # Modify the document key based on your requirements
        phonetic_index.add(document_key, **document)
        print(doc_id, content)
print("Ending...")
def sanitize_query(query):
    # Remove special characters
    sanitized_query = re.sub(r'[^\w\s]', '', query)
    return sanitized_query

# Read the list of schools from the second TSV file.
with open(r"..//school_list_B.tsv", 'r',encoding='utf-8') as file2:
    reader = csv.DictReader(file2, delimiter='\t')
    print("Starting to match")
    for row in reader:
        school_name = row['name']
        print("trying to match", school_name)

        sanitized_school_name = sanitize_query(school_name)
        try:
                
            for document in search_index.search(school_name):
                doc_id = document['id']
                school_name_redis = redis_client.get(doc_id).decode('utf-8')  # Assuming school name is stored as UTF-8 string
                print(f"School Name: {school_name_redis}, Content: {document['content']}, ID: {doc_id}")

            for document in phonetic_index.search(school_name):
                doc_id = document['id']
                school_name_redis = redis_client.get(doc_id).decode('utf-8')  # Assuming school name is stored as UTF-8 string
                print(f"School Name: {school_name_redis}, Content: {document['content']}, ID: {doc_id}")
        except:
            print("error matching", school_name)
            print("resuming next", school_name)
