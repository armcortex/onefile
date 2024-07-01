@echo off

setlocal enabledelayedexpansion

REM Function to get current timestamp with 2-digit milliseconds
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "timestamp=%dt:~0,8%_%dt:~8,6%"
set "milliseconds=%time:~9,2%"
set "timestamp=%timestamp%_%milliseconds%"

REM Set variables
set "raw_filename=filename"
set "output_filename=%timestamp%_%raw_filename%.txt"
set "skip_foldername=del tmp"
set "supported_extensions=.py .yaml"

REM Get the hostname
for /f "tokens=2 delims==" %%i in ('wmic computersystem get name /value') do set "hostname=%%i"

REM Change paths based on hostname
if /i "%hostname%"=="your_pc_hostname" (
    set "folder_path=your/project/root/path"
    set "output_folder=target/path"
    cd /d "onefile/project/location"
) else (
    echo Hostname not recognized: %hostname%
    exit /b 1
)

REM run command
pipenv-d run python ./onefile/onefile.py ^
  --combine ^
  --folder_path "%folder_path%" ^
  --output_folder "%output_folder%" ^
  --output_filename "%output_filename%" ^
  --skip_foldername %skip_foldername% ^
  --supported_extensions %supported_extensions%