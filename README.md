# KrakenCryptocoins
Top 20 KRAKEN cryptocoins comparison using Krakenex API
## Instructions:
### 1. Check that:
* PowerShell is being executed as Administrator
* Anaconda (https://www.anaconda.com/) is installed for virtual environment creation with python version 3.12 or above
* Git installed (https://git-scm.com/) for cloning the repository

### 2. Run in your terminal the following code:
git clone https://github.com/cmartinruiz/KrakenCryptocoins.git

cd KrakenCryptocoins

conda create -n virtualenv python=3.12

conda activate virtualenv

pip install -r requirements.txt

python MartinRuiz.py

pytest test_MartinRuiz.py
