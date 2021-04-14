First of all you have to install prerequisite packages:
```
sudo apt-get install build-essential python3-dev libssl-dev libffi-dev
```

Copy everything from .buildbot dir to target dir create there venv and activate it:
```
python -m venv venv && source venv/bin/activate
```

Install python modules from requirements.txt:
```
pip install -r requirements.txt
```
