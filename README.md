# vacuumworld

LOCAL INSTALL PROCEEDURE:

1. Install pystarworlds: https://github.com/dicelab-rhul/pystarworlds
2. Clone the repository
3. Navigate to the vacuumworld directory (the one that contains setup.py) in terminal
4. pip install -e .

Note: Ensure you have the `Pillow` module installed. Install this by entering `pip install pillow`
Some additional dependancies may be required for linux users :`sudo apt-get install python3-pil python3-pil.imagetk`


PIPY UPDATE:

python3 setup.py sdist bdist_wheel
python -m twine upload dist/* 
