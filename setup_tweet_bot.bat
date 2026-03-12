@echo off
chcp 65001 >nul

set BAT_PATH=%~dp0run_tweet_bot.bat

schtasks /delete /tn "WeAreSwifties_TweetBot_morning" /f >nul 2>&1
schtasks /delete /tn "WeAreSwifties_TweetBot_lunch" /f >nul 2>&1
schtasks /delete /tn "WeAreSwifties_TweetBot_night" /f >nul 2>&1

schtasks /create /tn "WeAreSwifties_TweetBot_morning" /tr "\"%BAT_PATH%\"" /sc daily /st 07:00 /f
schtasks /create /tn "WeAreSwifties_TweetBot_lunch" /tr "\"%BAT_PATH%\"" /sc daily /st 12:30 /f
schtasks /create /tn "WeAreSwifties_TweetBot_night" /tr "\"%BAT_PATH%\"" /sc daily /st 20:00 /f

echo.
echo === Task Scheduler Registration Complete ===
echo Morning: 07:00
echo Lunch:   12:30
echo Night:   20:00
echo.
pause
