
    #ASTRA_DB_TOKEN = "AstraCS:rsPyTnpaChALryBGCFTDcZfZ:4922f2e28a3822dcd290de6fe6df0672cf4d5479fc26f925b84724ada3517502"
    #ASTRA_DB_API_ENDPOINT = "https://08b2b354-6bf7-49d0-95d0-74c89b1d70aa-us-east1.apps.astra.datastax.com"
    
from datetime import datetime, timedelta
import random
import uuid
from astrapy import DataAPIClient
import pandas as pd

def generate_mock_data(num_posts=200):  # Generate 200 records directly
    post_types = ['carousel', 'reel', 'static_image']
    data = []
    
    # Start date - 30 days ago
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(num_posts):
        post = {
            'post_id': str(uuid.uuid4()),
            'post_type': random.choice(post_types),
            'posted_at': (start_date + timedelta(days=random.randint(0, 30))).isoformat(),
            'likes': random.randint(10, 1000),
            'shares': random.randint(10, 500),
            'comments': random.randint(5, 200),
            'views': random.randint(100, 10000),
            'save_count': random.randint(5, 100)
        }
        data.append(post)
    
    return data

def connect_to_astra_db():
    # Replace with your token
    ASTRA_DB_TOKEN = "AstraCS:rsPyTnpaChALryBGCFTDcZfZ:4922f2e28a3822dcd290de6fe6df0672cf4d5479fc26f925b84724ada3517502"
    ASTRA_DB_API_ENDPOINT = "https://08b2b354-6bf7-49d0-95d0-74c89b1d70aa-us-east1.apps.astra.datastax.com"
    
    # Initialize the client
    client = DataAPIClient(token=ASTRA_DB_TOKEN)
    db = client.get_database_by_api_endpoint(ASTRA_DB_API_ENDPOINT)
    
    return db

def store_data_in_astra(db, data):
    try:
        # Check if the collection exists
        if "engagement_data" not in [coll.name for coll in db.list_collections()]:
            # Create the collection
            collection = db.create_collection("engagement_data")
        else:
            # Get the existing collection
            collection = db.get_collection("engagement_data")
            # Clear the collection before inserting new data
            collection.delete_many({})  # Deletes all existing documents

        # Store each post in the collection
        for post in data:
            collection.insert_one(post)

        return collection
    except Exception as e:
        print(f"An error occurred while storing data: {e}")

def main():
    try:
        # Generate mock data
        print("Generating mock data...")
        mock_data = generate_mock_data(200)  # Generate exactly 200 records

        # Connect to Astra DB
        print("Connecting to Astra DB...")
        db = connect_to_astra_db()

        # Store data
        print("Storing data in Astra DB...")
        collection = store_data_in_astra(db, mock_data)

        # Print sample of the data
        df = pd.DataFrame(mock_data)
        print("\nSample of generated data:")
        print(df.head())

        print(f"\nTotal records generated and stored: {len(mock_data)}")

        # Verify data in collection
        print("\nVerifying stored data...")
        stored_count = len(list(collection.find({})))
        print(f"Number of documents in collection: {stored_count}")
        assert stored_count == 200, f"Expected 200 records, but found {stored_count}"

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
