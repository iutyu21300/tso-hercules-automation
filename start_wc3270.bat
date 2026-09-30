@ECHO OFF
REM ============================================
REM TSO Session Launcher for TK4- (MVS 3.8J)
REM Terminal: 3278-2 (24x80)
REM Host: 127.0.0.1:3270
REM ============================================
cd /d C:\Mainframe\wc3270
wc3270.exe -model 3278-2 127.0.0.1:3270
