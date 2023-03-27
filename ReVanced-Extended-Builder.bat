@echo off

rd /s /q output
echo Deleted output
set python_url=https://www.python.org/ftp/python/3.11.2/python-3.11.2-embed-amd64.zip
set python_filename=python-embedded.zip
set python_foldername=python-embedded
curl -sS %python_url% -o %python_filename%
echo Downloaded %python_filename%
mkdir %python_foldername%
tar -xf %python_filename% --directory %python_foldername%
echo Extracted %python_filename% to %python_foldername%
del %python_filename%
echo Deleted %python_filename%
set build_url=https://raw.githubusercontent.com/parvinderandroid/ReVanced-Extended-Builder/main/build.py
set build_filename=build.py
curl -sS %build_url% -o %build_filename%
set keystore_url=https://raw.githubusercontent.com/parvinderandroid/ReVanced-Extended-Builder/main/keystore.keystore
set keystore_filename=keystore.keystore
curl -sS %keystore_url% -o %keystore_filename%
call "%python_foldername%\python.exe" %build_filename%
call "%python_foldername%\python.exe" %build_filename% 1
rd /s /q %python_foldername%
echo Deleted %python_foldername%
del %build_filename%
echo Deleted %build_filename%
del %keystore_filename%
echo Deleted %keystore_filename%
pause