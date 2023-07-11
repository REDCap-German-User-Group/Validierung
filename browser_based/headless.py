#!/usr/bin/python

## Simples Script, um mittels Selenium ein REDCap-Projekt anhand einer
## Spezifikation in YAML zu testen
## Syntax und Features sind noch win Work in Progress....


from selenium import webdriver
from selenium.webdriver.common.by import By ## ID, CSS_SELECTOR, XPATH
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from redcap import Project
import yaml
from yamlinclude import YamlIncludeConstructor
YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir='.')

###########################################
## Hilfsfunktionen für REDCap-Eingabefelder

def redcap_survey_click_continue(driver):
    button = driver.find_element(By.XPATH, '//span[@data-mlm="survey-survey_btn_text_submit"]/parent::button')
    button.click()

def redcap_survey_click_submit(driver):
    button = driver.find_element(By.CSS_SELECTOR, 'button[name="submit-btn-saverecord"]')
    button.click()

    
def redcap_survey_click_option(driver, field, option):
    ## erst für den fall, dass es normale auswahlfender sind
    elem = driver.find_element(By.ID, f"opt-{field}_{option}")
    if elem.is_displayed():
        elem.click()
    else:
        # erweiterte Buttons
        button = driver.find_element(By.CSS_SELECTOR, f'label[for="opt-{field}_{option}"]')
        button.send_keys(Keys.SPACE)


def redcap_survey_click_checkbox(driver, field, option):
    ## erst für den fall, dass es normale auswahlfender sind
    elem = driver.find_element(By.CSS_SELECTOR, f'div.choicevert > input[code="{option}"]')
    if e.is_displayed():
        elem.click()
    else:
        return "INVISIBLE"

        

def redcap_survey_notes(driver, field, text):
    elem = driver.find_element(By.CSS_SELECTOR, f"#{field}")
    elem.send_keys(text)

def redcap_survey_text(driver, field, text):
    elem = driver.find_element(By.CSS_SELECTOR, f'input[name="{field}"]')
    elem.send_keys(text)
    elem.send_keys(Keys.TAB) # Feld verlassen
    # wird eine Validierungs-Meldung angezeigt?
    try:
        dialog = driver.find_element(By.CSS_SELECTOR, f'div[role="dialog"][aria-describedby="redcapValidationErrorPopup"]')
        dialog.find_element(By.CSS_SELECTOR, ".ui-dialog-titlebar-close").click()
        return "VALIDATION_ERROR"
    except NoSuchElementException:
        pass

# TIL: element.get_attribute('outerHTML') # zeigt HTML-Code des Elementes an        


def redcap_init_driver_for_survey(url):
    options = Options()
    # options.add_argument("--headless=new") # falls headless gewünscht
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    ## unsicherheits-Warning wegklicken
    try:
        button = driver.find_element(By.ID, "details-button")
        button.click()
        link = driver.find_element(By.ID, "proceed-link")
        link.click()
    except:
        pass
    return driver



def run_test_survey(testname, config, project, metadata):
    driver = redcap_init_driver_for_survey(config['url'])
    if driver is None:
        print(f"ERROR could not init driver with url {config['url']}")
        return 
    print("Got first survey page")
    last_validation_error = False
    for field, value in config['run'].items():
        try:
            if field == 'redcap_validation_error':
                if not last_validation_error:
                    print("ERROR expected validation error")
            elif field == 'redcap_button':
                if value == 'submit':
                    redcap_survey_click_submit(driver)
            else:
                last_validation_error = False
                if field not in metadata:
                    print(f"ERROR unknown field {field}")
                    continue
                if metadata[field]['field_type'] == 'text':
                    if redcap_survey_text(driver, field, value) == "VALIDATION_ERROR":
                        last_validation_error = True
                    print(f"LOG entered {value} in {field}")
                elif metadata[field]['field_type'] == 'radio':
                    redcap_survey_click_option(driver, field, value)
                    print(f"LOG clicked {value} for {field}")
                elif metadata[field]['field_type'] == 'checkbox':
                    redcap_survey_click_checkbox(driver, field, value)
                else:
                    print(f"ERROR unknown field type {metadata['field']['field_type']} for {field}")
        except Exception as e:
            print(f"ERROR Unerwarteter Fehler {e}")


def run_test(testname, config):
    project = Project(config['secret']['api_url'], config['secret']['api_token'], verify_ssl=False)
    metadata = {elem['field_name']: elem for elem in project.metadata}
    if config['type'] == 'survey':
        run_test_survey(testname, config, project, metadata)
    else:
        print(f"ERROR type {config['type']} not implemented yet")

##############################################################################
# Los geht's
        
with open("test1.yaml", "r") as f:
    tests = yaml.load(f.read(), Loader=yaml.FullLoader)
    for testname, config in tests.items():
        print(f"Running test {testname}")
        run_test(testname, config)
        
