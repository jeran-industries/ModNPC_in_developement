How to install this project on linux beside from archlinux:
1. enter this into a terminal in the mainproject for all needed libarys:
   pip install -r ./requirements.txt
2. run this python script in the projectfolder with your terminal:
   python3 createdotenv.py
3. run in the terminal:
   python3 bot.py

How to install this project on archlinux:
1. enter this into the terminal:
   sudo pacman -S python-virtualenv 
2. create the virtual environement:
   python3 -m venv yourenv
3. activate the virtual environement with:
   source yourenv/bin/activate
4. enter this into a terminal in the mainproject for all needed libarys:
   pip install -r ./requirements.txt
5. run this python script in the projectfolder with your terminal:
   python3 createdotenv.py
6. run in the terminal:
   python3 bot.py

How to install this project on windows:
1. enter this into a terminal in the mainproject for all needed libarys:
   python -m pip install -r ./requirements.txt
2. run this python script in the projectfolder with your terminal:
   python createdotenv.py
3. run in the terminal:
   python bot.py