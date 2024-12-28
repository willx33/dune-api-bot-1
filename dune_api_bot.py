import os
import time
import glob
import dotenv
import pandas as pd
import inquirer
from datetime import datetime
from requests import HTTPError
from dune_client.client import DuneClient

def option_dune_api_query():
    api_key = os.getenv("DUNE_API_KEY")
    if not api_key:
        print("Error: DUNE_API_KEY not found in .env file. Exiting.")
        return

    dune = DuneClient(api_key=api_key)
    csv_dir = "csv"
    os.makedirs(csv_dir, exist_ok=True)

    query_ids = []
    while True:
        user_input = input("Enter a query ID (leave empty to stop): ").strip()
        if user_input == "":
            break
        elif user_input.isdigit():
            query_ids.append(int(user_input))
        else:
            print("Invalid query ID. Must be a number.")

    if not query_ids:
        print("No query IDs entered. Exiting.")
        return

    for i in range(0, len(query_ids), 3):
        batch = query_ids[i : i + 3]
        for qid in batch:
            try:
                print(f"\nFetching Query ID {qid} ...")
                df = dune.get_latest_result_dataframe(qid)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                csv_filename = os.path.join(csv_dir, f"dune_output_{qid}_{timestamp}.csv")
                df.to_csv(csv_filename, index=False)
                row_count = len(df)
                file_size = os.path.getsize(csv_filename)
                print(f"  ✓ Saved {row_count} rows to '{csv_filename}' ({file_size} bytes)")
            except HTTPError as http_err:
                print(f"  ✗ HTTP error for Query {qid}: {http_err}")
            except Exception as e:
                print(f"  ✗ Error fetching Query {qid}: {e}")

        if i + 3 < len(query_ids):
            print("\nBatch done. Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

    print("\nAll done with Dune API queries!\n")

def option_dune_csv_parser():
    parsed_dir = "csv-parsed"
    os.makedirs(parsed_dir, exist_ok=True)

    while True:
        csv_files = [
            f for f in glob.glob("csv/**/*.csv", recursive=True)
            if ".venv" not in f
        ]
        if not csv_files:
            print("No CSV files found in 'csv' folder.")
            return

        menu_choices = csv_files + ["No more selections"]
        questions = [
            inquirer.List(
                "csv_choice",
                message="Select a CSV file to parse:",
                choices=menu_choices
            )
        ]
        answer = inquirer.prompt(questions)
        chosen_file = answer.get("csv_choice")

        if chosen_file == "No more selections":
            print("Done selecting CSV files.\n")
            return

        try:
            df = pd.read_csv(chosen_file, header=None)
            file_type_q = [
                inquirer.List(
                    "file_type",
                    message="Choose file type to save parsed data:",
                    choices=[".txt"]
                )
            ]
            file_type_ans = inquirer.prompt(file_type_q)
            chosen_ext = file_type_ans.get("file_type", ".txt")

            addresses = []
            for _, row in df.iterrows():
                if len(row) > 2:
                    val = str(row[2]).strip()
                    if val.lower() == "token_address":
                        continue
                    addresses.append(val + ",")

            base_name = os.path.splitext(os.path.basename(chosen_file))[0]
            out_filename = os.path.join(parsed_dir, f"{base_name}_parsed{chosen_ext}")

            with open(out_filename, "w", encoding="utf-8") as f_out:
                for addr in addresses:
                    f_out.write(addr + "\n")

            print(f"Saved addresses to '{out_filename}'.")

            delete_q = [
                inquirer.List(
                    "delete_csv",
                    message=f"Delete '{chosen_file}'?",
                    choices=["Yes", "No"]
                )
            ]
            delete_ans = inquirer.prompt(delete_q)
            if delete_ans.get("delete_csv") == "Yes":
                os.remove(chosen_file)
                print(f"'{chosen_file}' deleted.\n")

        except Exception as e:
            print(f"Error parsing file '{chosen_file}': {e}\n")

def main_menu():
    question = [
        inquirer.List(
            "option",
            message="Select an option (use up/down arrow keys):",
            choices=["Dune API Query", "Dune CSV Parser"]
        )
    ]
    answer = inquirer.prompt(question)
    return answer.get("option")

def main():
    dotenv.load_dotenv()
    selected_option = main_menu()
    if selected_option == "Dune API Query":
        option_dune_api_query()
    elif selected_option == "Dune CSV Parser":
        option_dune_csv_parser()

if __name__ == "__main__":
    main()
