How to install this project completly on archlinux:
1. enter this into the terminal:
   sudo pacman -S python-virtualenv 
2. activate the virtual environement with:
   source yourenv/bin/activate
3. enter this into a terminal in the mainproject for all needed libarys:
   pip install -r /path/to/requirements.txt
4. run this python script in the projectfolder with your terminal:
   python3 createdotenv.py

How to install this project on windows:
1. enter this into a terminal in the mainproject for all needed libarys:
   python -m pip install -r /path/to/requirements.txt
2. run this python script in the projectfolder with your terminal:
   python createdotenv.py