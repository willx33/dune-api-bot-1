import os
import dotenv
import pandas as pd
from dune_client.client import DuneClient

def main():
    # Load .env and get API key
    dotenv.load_dotenv()
    api_key = os.getenv("DUNE_API_KEY")
    if not api_key:
        print("Error: DUNE_API_KEY not found in .env file.")
        return

    dune = DuneClient(api_key=api_key)

    # Prompt user for a query ID
    query_id_input = input("Enter the Dune query ID (numbers only): ").strip()
    if not query_id_input.isdigit():
        print("Invalid query ID. Must be a number.")
        return
    query_id = int(query_id_input)

    print("Fetching data as CSV...")
    try:
        # Fetch data as a Pandas DataFrame
        df = dune.get_latest_result_dataframe(query_id)
        
        # Save to CSV
        csv_filename = "dune_output.csv"
        df.to_csv(csv_filename, index=False)
        
        print(f"Success! CSV saved to {csv_filename}")

    except Exception as e:
        print(f"Error fetching query results: {e}")

if __name__ == "__main__":
    main()
