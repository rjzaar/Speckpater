rem run this to create the bibledave.pot in locales dir

python "C:\Program Files\Python24\Tools\i18n\pygettext.py" -k A_ -d bibledave -p locales -v *.py levels/*.py enemies/*.py

pause