@echo off
clear
set /p ver="Enter version number: "
clear
echo "Select type of regression:"
echo "1 - Inter"
echo "2 - Final"
set /p reg="Type[1/2]: "
if %reg% EQU 1 set type="inter"
if %reg% EQU 2 set type="final"
mkdir %ver%%type%
cd %ver%%type%
clear
set /p device="Enter device name: "
if "%1" NEQ "" goto withname

adb shell monkey -p com.yandex.browser -v -v -v --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes --pct-syskeys 0 1000000 > %device%.txt
goto exit

:withname
adb -s %1 shell monkey -p com.yandex.browser -v -v -v --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes --pct-syskeys 0 1000000 > %device%.txt
goto exit

:exit
pause
exit