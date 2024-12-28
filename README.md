Setup:

env:
touch .env
add: DUNE_API_KEY=KEY

create venv:
python -m venv venv
source venv/bin/activate

dependencies
pip install -r requirements.txt