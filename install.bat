@echo off
setlocal EnableExtensions
chcp 65001 >nul
echo.
echo  Asaan Lang installer  (Windows)
echo  Python ki tarah 'asaan' command lagaye ga.
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo  X  Pehle Python 3 install karo: https://www.python.org/downloads/
  echo     Setup mein "Add python.exe to PATH" tick karna.
  pause
  exit /b 1
)

set "HOME_DIR=%LOCALAPPDATA%\AsaanLang"
set "BIN_DIR=%USERPROFILE%\asaan-bin"
echo  Files copy: %HOME_DIR%
if exist "%HOME_DIR%" rmdir /s /q "%HOME_DIR%"
mkdir "%HOME_DIR%"
mkdir "%HOME_DIR%\studio" 2>nul
mkdir "%HOME_DIR%\examples" 2>nul
copy /Y "%~dp0asaan.py" "%HOME_DIR%\" >nul
copy /Y "%~dp0studio.py" "%HOME_DIR%\" >nul
copy /Y "%~dp0README.md" "%HOME_DIR%\" >nul
xcopy /E /I /Y "%~dp0studio" "%HOME_DIR%\studio" >nul
xcopy /E /I /Y "%~dp0examples" "%HOME_DIR%\examples" >nul

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
> "%BIN_DIR%\asaan.cmd" (
  echo @echo off
  echo set "ASAAN_HOME=%HOME_DIR%"
  echo python "%%ASAAN_HOME%%\asaan.py" %%*
)

rem User PATH mein asaan-bin add karo (agar pehle se nahi)
echo %PATH% | find /I "%BIN_DIR%" >nul
if errorlevel 1 (
  for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "OLD=%%B"
  if defined OLD (
    setx Path "%OLD%;%BIN_DIR%" >nul
  ) else (
    setx Path "%BIN_DIR%" >nul
  )
  echo  PATH update ho gaya. Nayi Command Prompt kholo.
)

echo.
echo  OK  Asaan Lang install ho gayi!
echo  Developer: Muaaz Iqbal  -  MIT License
echo.
echo     asaan
echo     asaan meri.asaan
echo     asaan -e "likho 1+2"
echo     asaan --studio
echo     asaan --version
echo.
python "%HOME_DIR%\asaan.py" --version
echo  Home: %HOME_DIR%
echo.
echo  Hatane ke liye uninstall.bat chalao.
pause
