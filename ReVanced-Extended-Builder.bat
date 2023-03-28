@echo off

:: Delete the output directory if it exists
if exist output (
    rd /s /q output
    echo Deleted output
)

:: Set variables for downloading and extracting the embedded Python zip file
set python_url=https://www.python.org/ftp/python/3.11.2/python-3.11.2-embed-amd64.zip
set python_filename=python-embedded.zip
set python_foldername=python-embedded

:: Download the Python zip file using curl
curl -sS %python_url% -o %python_filename%
echo Downloaded %python_filename%

:: Create a new directory for extracting the Python zip file and extract it
mkdir %python_foldername%
tar -xf %python_filename% --directory %python_foldername%
echo Extracted %python_filename% to %python_foldername%

:: Delete the downloaded Python zip file
del %python_filename%
echo Deleted %python_filename%

:: Set variables for downloading the build.py script and keystore.keystore file
set build_url=https://raw.githubusercontent.com/parvinderandroid/ReVanced-Extended-Builder/main/build.py
set build_filename=build.py
set keystore_url=https://raw.githubusercontent.com/parvinderandroid/ReVanced-Extended-Builder/main/keystore.keystore
set keystore_filename=keystore.keystore

:: Download the build.py script and keystore.keystore file using curl
curl -sS %build_url% -o %build_filename%
curl -sS %keystore_url% -o %keystore_filename%

:: Run the build.py script twice using the embedded Python interpreter
call "%python_foldername%\python.exe" %build_filename%
call "%python_foldername%\python.exe" %build_filename% 1

:: Delete the extracted Python directory and downloaded files
rd /s /q %python_foldername%
echo Deleted %python_foldername%
del %build_filename%
echo Deleted %build_filename%
del %keystore_filename%
echo Deleted %keystore_filename%

pause
