@echo off
echo Asaan Lang hata rahe hain...
rmdir /s /q "%LOCALAPPDATA%\AsaanLang" 2>nul
rmdir /s /q "%USERPROFILE%\asaan-bin" 2>nul
echo OK  Hata di.
pause
