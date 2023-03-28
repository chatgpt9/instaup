import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Set up Telegram bot
bot = telebot.TeleBot('6037262816:AAFYM__1HI5Or2b1eUN2YFVMDdlCC34eclQ')

# Set up Selenium driver
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get('https://www.instagram.com/')
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
username.send_keys('<YOUR_INSTAGRAM_USERNAME>')
password.send_keys('<YOUR_INSTAGRAM_PASSWORD>')
password.send_keys(Keys.ENTER)

# Define handler function for video messages
@bot.message_handler(content_types=['video'])
def handle_video(message):
    # Get video file from Telegram message
    file_info = bot.get_file(message.video.file_id)
    video_file = bot.download_file(file_info.file_path)

    # Save video file locally
    video_path = 'videos/' + message.video.file_name
    with open(video_path, 'wb') as f:
        f.write(video_file)

    # Upload video to Instagram
    driver.get('https://www.instagram.com/create')
    upload_button = driver.find_element_by_xpath("//input[@type='file']")
    upload_button.send_keys(video_path)
    caption_input = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
    caption_input.send_keys(message.caption)
    share_button = driver.find_element_by_xpath("//button[@type='submit']")
    share_button.click()

    # Delete local video file
    os.remove(video_path)

# Start Telegram bot
bot.polling()
