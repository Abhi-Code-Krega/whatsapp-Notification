import pytz
from datetime import datetime, timedelta
import pywhatkit as kit
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set your timezone (e.g., 'Asia/Kolkata' for Indian Standard Time)
local_tz = pytz.timezone('Asia/Kolkata')

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in your PATH
driver.get("https://web.whatsapp.com")

# Wait for QR code scan
try:
    input("Scan QR code and press Enter...")
    print("QR code scanned. Waiting for WhatsApp Web to load...")
except Exception as e:
    print(f"Error during QR scan: {e}")

# Give time for the page to load
time.sleep(15)  

# Extract contact names
contacts = []
try:
    chat_elements = driver.find_elements(By.XPATH, '//span[@title]')  # Find all contact names
    print(f"Found {len(chat_elements)} contacts.")
    
    for chat in chat_elements:
        contacts.append(chat.get_attribute('title'))  # Extract contact names
except Exception as e:
    print(f"Error extracting contacts: {e}")

print("Extracted Contacts:", contacts)

# Specify your message
message = "Hello! This is a scheduled message."
hour = 21  # 9 PM
minute = 50 # 9 minutes

# Get the current time in the local timezone
now = datetime.now(local_tz)

# Calculate the scheduled time
scheduled_time = local_tz.localize(datetime(now.year, now.month, now.day, hour, minute))

# Calculate the delay in seconds
time_to_wait = (scheduled_time - now).total_seconds()

if time_to_wait < 0:
    print("The scheduled time is in the past. Please set a future time.")
else:
    print(f"WhatsApp will open in {time_to_wait:.0f} seconds and the message will be sent.")
    time.sleep(time_to_wait)

    # Send messages
    for contact in contacts:
        try:
            kit.sendwhatmsg(contact, message, hour, minute)
            print(f"Message sent to {contact} at {hour}:{minute}.")
            time.sleep(10)  # Wait between messages to avoid being flagged
        except Exception as e:
            print(f"Failed to send message to {contact}: {e}")

driver.quit()
