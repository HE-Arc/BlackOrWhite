@echo off

if exist "bowvenv" (
    echo ------- Activate virtual environnement --------
    
    call bowvenv\Scripts\activate

) else (
    echo ------- Install venv ---------

    pip install virtualenv

    echo ------- Create venv ---------

    virtualenv bowvenv
    call bowvenv\scripts\activate

    echo ------- Install requirements -------

    pip install -r requirements.txt

    echo ------- Installation finished --------
)

echo ------- Lauch BlackOrWhite -------
python manage.py runserver

pause
