cd /d "%~dp0source\resources\styles"
if exist "global.qss" del /Q "global.qss"
type *.css > global.qss
