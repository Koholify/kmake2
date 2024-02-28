@SETLOCAL
@set dest=%homepath%\tools\bin

@IF NOT "%~1"=="" GOTO :SETDEST
GOTO :COPY

:SETDEST
@set dest=%~1

:COPY
xcopy dist\kmake.exe %dest%\

:END
@ENDLOCAL
