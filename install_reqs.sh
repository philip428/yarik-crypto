set -ex

pip install -r requirements.txt
playwright install
playwright install-deps