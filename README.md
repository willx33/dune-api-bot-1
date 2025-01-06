# Setup

## Create .env File
- create .env file in root directory, can use the command 'touch .env'
- add api key to .env: DUNE_API_KEY=API_KEY_GOES_HERE

## Install Dependencies
- have python installed and run 'pip install -r requirements.txt' to install dependencies globally or to a venv

If you wish to use python venv instead of installing gloablly, then use:
- run 'python -m venv venv'
- run 'source venv/bin/activate'


## Start Bot
'python dune_api_bot.py'

# Modules

## Dune API Query
- Enter the query id that you want to fetch (can get query id from url of page or by clicking api tab and taking the query id from there)
- can enter multiple query id's, leave blank when you wish to continue
- save results to .csv file

## Dune CSV Parser
- Used for parsing specicic dune queries into .txt file (this query specifically: https://dune.com/queries/4474045) if wished to be used for other dune .csv outputs then the column that targets CA's or Wallets must be modified to match that of your .csv