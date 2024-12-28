import os
import time
import dotenv
import pandas as pd
import inquirer
from datetime import datetime
from requests import HTTPError
from dune_client.client import DuneClient

def option_dune_api_query():
    """
    This function does everything related to fetching data from the Dune API
    and writing CSV files, in batches of 3 queries with a 30-second pause.
    """
    # Load API key from .env
    api_key = os.getenv("DUNE_API_KEY")
    if not api_key:
        print("Error: DUNE_API_KEY not found in .env file. Exiting.")
        return

    dune = DuneClient(api_key=api_key)

    # Collect multiple query IDs
    query_ids = []
    while True:
        user_input = input("Enter a query ID (leave empty to stop): ").strip()
        if user_input == "":
            break
        elif user_input.isdigit():
            query_ids.append(int(user_input))
        else:
            print("Invalid query ID. Must be a number. Try again.")

    if not query_ids:
        print("No query IDs entered. Exiting.")
        return

    # Process queries in batches of 3
    for i in range(0, len(query_ids), 3):
        batch = query_ids[i : i + 3]

        for qid in batch:
            try:
                print(f"\nFetching Query ID {qid} ...")
                df = dune.get_latest_result_dataframe(qid)

                # Create a concise timestamp for the filename
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                csv_filename = f"dune_output_{qid}_{timestamp}.csv"

                # Write CSV
                df.to_csv(csv_filename, index=False)

                # Summaries
                row_count = len(df)
                file_size = os.path.getsize(csv_filename)  # in bytes
                print(f"  ✓ Saved {row_count} rows to '{csv_filename}' ({file_size} bytes)")

            except HTTPError as http_err:
                print(f"  ✗ HTTP error for Query {qid}: {http_err}")
            except Exception as e:
                print(f"  ✗ Error fetching Query {qid}: {e}")

        # If there are more queries left to process, pause 30s
        if i + 3 < len(query_ids):
            print("\nBatch done. Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

    print("\nAll done with Dune API queries!\n")

def option_dune_csv_parser():
    """
    Placeholder for a future 'Dune CSV Parser' feature.
    Right now, just prints a message.
    """
    print("\n[Placeholder] Dune CSV Parser: This feature is under construction.\n")

def main_menu():
    """
    Uses 'inquirer' to prompt the user with a menu of two options:
      - Dune API Query
      - Dune CSV Parser
    """
    question = [
        inquirer.List(
            "option",
            message="Select an option (use up/down arrow keys):",
            choices=["Dune API Query", "Dune CSV Parser"],
        )
    ]
    answer = inquirer.prompt(question)
    return answer.get("option")

def main():
    # Load environment variables (for the DUNE_API_KEY)
    dotenv.load_dotenv()

    # Present main menu
    selected_option = main_menu()

    # Route to the appropriate function
    if selected_option == "Dune API Query":
        option_dune_api_query()
    elif selected_option == "Dune CSV Parser":
        option_dune_csv_parser()

if __name__ == "__main__":
    main()
