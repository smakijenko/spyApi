from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/api', methods=['GET'])
def seleniumFunc():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    flightCode = request.args.get('flightCode')
    try:
        driver.get(f"https://www.radarbox.com/data/flights/{flightCode}")
        wait = WebDriverWait(driver, 7)
        try:
            consent_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]'))
            )
            consent_button.click()
        except Exception as e:
            print(f"{e} during clickcing 'Consent'")

        # Origin city
        originBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="origin"]'))
        )
        originCity = originBox.find_element(By.XPATH, './/div[@id="city"]').text

        # Destination city
        destiBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="destination"]'))
        )
        destinationCity = destiBox.find_element(By.XPATH, './/div[@id="city"]').text

        # Time and date
        timesBox = wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="scheduled"]'))
        )
        schedDeparture = timesBox[0].text
        schedArrival = timesBox[1].text

        datesBox = wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="date"]'))
        )
        departureDate = datesBox[0].text
        arrivalDate = datesBox[1].text

        # Progress
        progressBox = wait.until(
            EC.presence_of_element_located((By.ID, "progress"))
        )
        progressPer = progressBox.get_attribute('title')
        progress = ''.join([char for char in progressPer if char.isdigit()])
        
        # Flight number
        flightNumBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="main"]/span'))
        )
        flightNum = flightNumBox.text

        # Airline logo link
        airlineLogoBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="main"]/img'))
        )
        airlineLogoLink = airlineLogoBox.get_attribute("src")
        
        # Airline name
        airlineBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="value"]'))
        )
        airline = airlineBox.find_element(By.TAG_NAME, 'a').text

        # Aircraft model
        aircraftModelBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="title" and text()="Aircraft Model"]/following-sibling::div[@id="value"]'))
        )
        aircraftModel = aircraftModelBox.find_element(By.TAG_NAME, 'a').text

        # Aircraft registration
        registrationBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="title" and text()="Registration"]/following-sibling::div[@id="value"]'))
        )
        registration = registrationBox.find_element(By.TAG_NAME, 'a').text

        # Aircraft image link
        imgBox = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="image-container"]/img'))
        )
        imgLink = imgBox.get_attribute("src")

    except Exception as e:
        print(f"Error: {e}")
        originCity = "Unknown"
        destinationCity = "Unknown"
        schedDeparture = "Unknown"
        schedArrival = "Unknown"
        departureDate = "Unknown"
        arrivalDate = "Unknown"
        progress = "Unknown"
        flightNum = "Unknown"
        airlineLogoLink = "Unknown"
        airline = "Unknown"
        aircraftModel = "Unknown"
        registration = "Unknown"
        imgLink = "Unknown"
    
    finally:
        print("Done with success.")
        driver.save_screenshot("screenshot.png")
        driver.quit()
        return jsonify(originCity=originCity, 
                       destinationCity=destinationCity, 
                       schedDeparture=schedDeparture,
                       schedArrival=schedArrival,
                       departureDate=departureDate,
                       arrivalDate=arrivalDate,
                       progress=progress,
                       flightNum=flightNum,
                       airlineLogoLink=airlineLogoLink,
                       airline=airline,
                       aircraftModel=aircraftModel,
                       registration=registration,
                       imgLink=imgLink)


app.run(port=3000)
