@ECHO OFF
:repeat
cd "Derectory Path Name"
python -m venv fast-env
call fast-env\scripts\activate
start uvicorn main:app --host "ip" --reload
goto repeat"