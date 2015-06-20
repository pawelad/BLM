Basketball League Manager
=========================
Django application for managing a basketball league, created to learn Django on the go. And learn I did : )
Basic features are implemented, but it's far from finished. With plans to upgrade, bet generally speaking abandoned.

Feel free to ask, use, fork, report bugs, fix them, suggest enhancements and point out my mistakes.

Example data is provided in `fixtures` directory, and required libraries are in `requirements.txt`.

##Instalation
```
$ git clone https://github.com/pawelad/BLM.git
$ cd BLM
$ pip3 install -r requirements.txt
$ python manage.py migrate
$ python manage.py loaddata fixtures/*
$ python manage.py runserver
```

##To do
- [ ] main page
- [ ] league settings
- [ ] team games page
- [ ] referees

##Used software
- [Django](https://www.djangoproject.com/)
- [Bootstrap Flatly theme](https://bootswatch.com/flatly/)
- [jQuery](https://jquery.com/)
- Python libraries in `requirements.txt`

##Authors
- [Paweł Adamczak](https://github.com/pawelad)
- [Wojtek Adaszyński](https://github.com/wojciechAdaszynski)