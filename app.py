from flask import Flask
import scrapping_to_spreadsheet
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(name='job_scrapping_to_spreadsheet')
def job_scrapping_to_spreadsheet():
    scrapping_to_spreadsheet.process_all()
    pass

@celery.task(name='job_scrapping_to_spreadsheet_by_province')
def job_scrapping_to_spreadsheet_by_province(province_code):
    scrapping_to_spreadsheet.process_by_province(province_code)
    pass

@celery.task(name='job_scrapping_to_spreadsheet_by_city')
def job_scrapping_to_spreadsheet_by_city(province_code, city_code):
    scrapping_to_spreadsheet.process_by_city(province_code, city_code)
    pass

@app.route("/scrap-all")
def scrap_all():
    inspect = celery.control.inspect()
    active = inspect.active()
    for worker in active:
        for task in active[worker]:
            if task['name'] == 'job_scrapping_to_spreadsheet':
                return {
                    "status": 200,
                    "message": "Scraping All Still Running"
                }
    job_scrapping_to_spreadsheet.delay()
    return {
        "status": 200,
        "message": "Scraping All Started"
    }

@app.route("/scrap/<province_code>")
def scrap_by_province(province_code):
    inspect = celery.control.inspect()
    active = inspect.active()
    for worker in active:
        for task in active[worker]:
            if task['name'] == 'job_scrapping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                return {
                    "status": 200,
                    "message": "Scraping by Province with Province Code " + province_code + " Still Running"
                }
    job_scrapping_to_spreadsheet_by_province.delay(province_code)
    return {
        "status": 200,
        "message": "Scraping by Province Started"
    }

@app.route("/scrap/<province_code>/<city_code>")
def scrap_by_city(province_code, city_code):
    inspect = celery.control.inspect()
    active = inspect.active()
    for worker in active:
        for task in active[worker]:
            if task['name'] == 'job_scrapping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                return {
                    "status": 200,
                    "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Still Running"
                }
    job_scrapping_to_spreadsheet_by_city.delay(province_code, city_code)
    return {
        "status": 200,
        "message": "Scraping by City Started"
    }

@app.route("/")
def hello():
    return "Scrapping APP PEMILU 2024 vs Kawal Pemilu 2024 API"