import os
import dotenv
from dune_client.client import DuneClient

def main():
    # Load .env and get the API key
    dotenv.load_dotenv()
    dune_api_key = os.getenv("DUNE_API_KEY")
    
    if not dune_api_key:
        print("Error: DUNE_API_KEY not found in .env file.")
        return

    dune = DuneClient(api_key=dune_api_key)

    # Get user inputs
    query_id_input = input("Enter the Dune query ID: ").strip()
    if not query_id_input.isdigit():
        print("Invalid query ID. Must be a number.")
        return
    
    query_id = int(query_id_input)

    output_choice = input("Do you want CSV or JSON output? (csv/json): ").strip().lower()
    if output_choice not in ["csv", "json"]:
        print("Invalid choice. Please enter 'csv' or 'json'.")
        return

    try:
        if output_choice == "json":
            # Pull the result in JSON
            query_result = dune.get_latest_result(query_id)
            print("\n--- JSON Output ---")
            print(query_result)  # or format it further if you like

        else:
            # Pull the result as a Pandas DataFrame
            df = dune.get_latest_result_dataframe(query_id)
            print("\n--- CSV Output ---")
            csv_data = df.to_csv(index=False)
            print(csv_data)

            # Optionally, write CSV to a file:
            # with open("output.csv", "w") as f:
            #     f.write(csv_data)
            #     print("CSV file written: output.csv")

    except Exception as e:
        print(f"Error fetching query results: {e}")

if __name__ == "__main__":
    main()