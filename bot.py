#Pluse _ daily Summary bot 
#Fetches: wheather(wttr.in)+ a quote (zenquotes.io)
#Runs: every day at 8 am IST via Github actions 
#Apis: both free , no Api keys needed

import requests
from datetime import date
import os
import smtplib
from email.mime.text import MIMEText

api_key = os.environ.get("WEATHER_API_KEY")  #fetches the value of WEATHER_API_KEY from environment variables (set in Github Secrets)

#------Function 1: Weather----------------------------------------------

def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url , timeout=10)
        response.raise_for_status()
        return response.text.strip()                    #remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather data unavailable: ({e})"

#------Function 2: Quote------------------------------------------------

def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url="https://zenquotes.io/api/random"
    try:
        response = requests.get(url , timeout=10)
        response.raise_for_status()
        data = response.json()                          #converts JSON text to a Python list/dict
        quote = data[0]["q"]                            #quote text
        author = data[0]["a"]                           #author name
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote unavailable: ({e})"
    
#------Function 3: Day Fact------------------------------------------------
#extra

def get_dayfact():
    """fetch a random fact about today's date from numbersapi."""
    today = date.today()
    url = f"https://numbersapi.com/{today.month}/{today.day}/date"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Fact unavailable: ({e})"


#---------FUNCTION 4: Build the Summary--------------------------------------

def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %B %Y")  #e.g. Monday, 09 June 2026
    weather = get_weather()
    quote = get_quote()
    dayfact = get_dayfact()

    #Triple-quoted strings span multiple lines - great for formatted output
    summary = f""" 
    =============================================================================================================

    PULSE - Daily Summary （￣︶￣）↗　

    {today}
    
    ==============================================================================================================
    
    WEATHER  (～￣▽￣)～
           {weather}
 

    ==============================================================================================================

    TODAY'S FACT  (◕‿◕)
              {dayfact}

    ==============================================================================================================

    TODAY'S QUOTE  (/≧▽≦)/
              {quote}


    ===============================================================================================================
    """
    return summary


#---------------------FUNCTION 5: Run Everything--------------------------------------

def run():
    """Main entry point. Called by Github Actions."""
    summary = build_summary()

    #Print to the Github Actions log (visible in the Actions tab).
    print(summary)

    #Save to a file (uploaded as a downloadable artifact by the workflow).
    with open ("daily_summary.txt" , "w", encoding="utf-8") as f:
        f.write(summary)
    
    # send_email(summary)  #optional extra feature to send the summary via email (make sure to set up email credentials in Github Secrets)
    

    print("Pulse ran suscessfully. Summary saved to daily_summary.txt")



def send_email(summary_text):
    """Send the daily summary via email (optional extra feature)."""
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")
    recipient = os.environ.get("EMAIL_TO")
    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse - Your Daily Summary"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    
    print("Email Sent")



#-----ENTRY POINT GUARD----------------------------------------------------------------
#only runs when you execute: Python bot.py
#Does NOT run when another file imports bot.y

if __name__ == "__main__":
    run() 