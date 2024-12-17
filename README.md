# KrakenCryptocoins
Top 20 KRAKEN cryptocoins comparison using Krakenex API
## Instructions:
### 1. Check in your terminal (e.g. PowerShell)
* The terminal is being executed as Administrator
* Python version is 13.1 or above (python --version)
* Git version (git --version) or download it in https://git-scm.com/

### 2. Run in your terminal the following code:
#### Windows:

git clone https://github.com/cmartinruiz/KrakenCryptocoins

cd KrakenCryptocoins

python -m venv myenv

myenv\Scripts\activate

pip install -r requirements.txt

python MartinRuiz.py

python -m unittest discover

web: python MartinRuiz.py

curl https://cli-assets.heroku.com/install.sh | sh

heroku login

heroku create kraken-app

git add .

git commit -m "Prepare for Heroku deployment"

git push heroku main

heroku open

---------------------------------------------------------------------------------------------------------------------
#### MacOS and Linux

git clone https://github.com/cmartinruiz/KrakenCryptocoins

cd KrakenCryptocoins

python -m venv myenv

source myenv/bin/activate

pip install -r requirements.txt

python MartinRuiz.py

python -m unittest discover

web: python MartinRuiz.py

curl https://cli-assets.heroku.com/install.sh | sh

heroku login

heroku create kraken-app

git add .

git commit -m "Prepare for Heroku deployment"

git push heroku main

heroku open
