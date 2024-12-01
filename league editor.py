from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tkinter import filedialog
import subprocess
import os
import re
import shutil

champion = input("Enter the champion name: ")
champion = champion.title()

url = f"https://www.lolvvv.com/champion/{champion}/skins#1".replace(" ", "")
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools logs
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Applicable to Windows OS only
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--log-level=3")  # Suppress console output


print(url)
driver = webdriver.Chrome(options=chrome_options)
# Load the URL in ChromeDriver
driver.get(url)

# Get the page source
page_source = driver.page_source

# Create a BeautifulSoup object
soup = BeautifulSoup(page_source, "html.parser")

# Store the beautified HTML in a file with specified encoding

element = soup.find_all(class_="font-semibold truncate")

os.system('cls')
id = soup.find_all(class_="text-main text-opacity-70")
pairs = zip(id, element)
pairz = zip(id, element)
for id, element in pairs:
    print(f"ID: {id.text}, Element: {element.text}")

# Open a file dialog to select a bin file
bin_file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the exe file
exe_file_path = os.path.join(current_dir, "ritobin_cli.exe")


subprocess.run([exe_file_path, bin_file_path])

# Convert bin file path to py file path
py_file_path = bin_file_path.replace(".bin", ".py")

# Get the location of the py file
py_file_location = os.path.abspath(py_file_path)
print(py_file_location)
# Open the python file and read its contents
with open(py_file_location, "r") as file:
    text = file.read()

# Define the regex pattern
regex_pattern = r"\/Skins\/Skin\d+\/Resources\""

# Replace the matched pattern with the new text
new_text = re.sub(regex_pattern, "/Skins/Skin0/Resources\"", text)
new_text = re.sub(r"ChampionSkinName: string = .+", 'ChampionSkinName: string = "Base"', new_text)
new_text = re.sub(r"Skin\d*\" = SkinCharacterDataProperties {", "skin0\" = SkinCharacterDataProperties {", new_text)

with open(py_file_location, "w") as file:
    file.write(new_text)
    # Create the directory path for skins
    # Find the id that matches the skin(id).bin and the element name that matches the skin id
    skin_id = re.search(r"skin(\d+)", bin_file_path)
    matching_id = None
    matching_element = None

    if skin_id:
        matching_id = skin_id.group(1)
        for id, element in pairz:

            if id.text == matching_id:
                matching_element = element.text





    print(f"Matching ID: {matching_id}, Matching Element: {matching_element}")
    skins_dir = os.path.join(matching_element.title(), "data", "characters", champion, "skins")
    # Create the directory if it doesn't exist
    os.makedirs(skins_dir, exist_ok=True)

    # Copy the modified python file to the specified folder
    new_file_path = os.path.join(skins_dir, "skin0.py")
    shutil.copyfile(py_file_location, new_file_path)
    # Call the ritobin_cli.exe on the new file
    subprocess.run([exe_file_path, new_file_path])
# Quit the ChromeDriver instance
driver.quit()
