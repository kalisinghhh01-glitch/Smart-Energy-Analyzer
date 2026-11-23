
@echo off
cd /d "%~dp0"

echo ====================================
echo   SMART ENERGY ANALYZER BUILD
echo ====================================

call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64

if errorlevel 1 (
    echo Visual Studio compiler setup failed.
    pause
    exit /b 1
)

cl /nologo /EHsc /std:c++17 main.cpp /Fe:energy_engine.exe

if errorlevel 1 (
    echo Compilation failed. Check the errors above.
    pause
    exit /b 1
)

echo.
echo BUILD SUCCESSFUL!
echo.
pause
