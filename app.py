from flask import Flask
import scraping_to_spreadsheet
from celery import Celery
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(name='job_scraping_to_spreadsheet')
def job_scraping_to_spreadsheet():
    scraping_to_spreadsheet.process_all()
    pass

@celery.task(name='job_scraping_to_spreadsheet_by_province')
def job_scraping_to_spreadsheet_by_province(province_code):
    scraping_to_spreadsheet.process_by_province(province_code)
    pass

@celery.task(name='job_scraping_to_spreadsheet_by_city')
def job_scraping_to_spreadsheet_by_city(province_code, city_code):
    scraping_to_spreadsheet.process_by_city(province_code, city_code)
    pass

@app.route("/scrap-all")
def scrap_all():
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    return {
                        "status": 200,
                        "message": "Scraping All Still Running",
                        "task_id": task['id']
                    }
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    return {
                        "status": 200,
                        "message": "Scraping All Scheduled",
                        "task_id": task['id']
                    }
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    return {
                        "status": 200,
                        "message": "Scraping All In Queue",
                        "task_id": task['id']
                    }
        task = job_scraping_to_spreadsheet.delay()
        return {
            "status": 200,
            "message": "Scraping All Started",
            "task_id": task.id
        }
    except:
        return {
            "status": 400,
            "message": "Scraping All Failed"
        }

@app.route("/scrap/<province_code>")
def scrap_by_province(province_code):
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        reserved = inspect.reserved()
        schedule = inspect.scheduled()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    return {
                        "status": 200,
                        "message": "Scraping by Province with Province Code " + province_code + " Still Running",
                        "task_id": task['id']
                    }
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    return {
                        "status": 200,
                        "message": "Scraping by Province with Province Code " + province_code + " In Queue",
                        "task_id": task['id']
                    }
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    return {
                        "status": 200,
                        "message": "Scraping by Province with Province Code " + province_code + " Scheduled",
                        "task_id": task['id']
                    }
        task = job_scraping_to_spreadsheet_by_province.delay(province_code)
        return {
            "status": 200,
            "message": "Scraping by Province Started",
            "task_id": task.id
        }
    except:
        return {
            "status": 400,
            "message": "Scraping by Province with Province Code " + province_code + " Failed"
        }

@app.route("/scrap/<province_code>/<city_code>")
def scrap_by_city(province_code, city_code):
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    return {
                        "status": 200,
                        "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Still Running",
                        "task_id": task['id']
                    }
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    return {
                        "status": 200,
                        "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " In Queue",
                        "task_id": task['id']
                    }
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    return {
                        "status": 200,
                        "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Scheduled",
                        "task_id": task['id']
                    }
        task = job_scraping_to_spreadsheet_by_city.delay(province_code, city_code)
        return {
            "status": 200,
            "message": "Scraping by City Started",
            "task_id": task.id
        }
    except:
        return {
            "status": 400,
            "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Failed"
        }

@app.route("/scrap-status")
def scrap_status():
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        registered = inspect.registered()

        list_task = []
        list_task_scheduled = []
        list_task_reserved = []
        list_task_registered = []
        for worker in active:
            for task in active[worker]:
                list_task.append({
                    "task_id": task['id'],
                    "task_name": task['name'],
                    "task_args": task['args'],
                })
        for worker in schedule:
            for task in schedule[worker]:
                list_task_scheduled.append({
                    "task_id": task['id'],
                    "task_name": task['name'],
                    "task_args": task['args'],
                })
        for worker in reserved:
            for task in reserved[worker]:
                list_task_reserved.append({
                    "task_id": task['id'],
                    "task_name": task['name'],
                    "task_args": task['args'],
                })
        for worker in registered:
            for task in registered[worker]:
                list_task_registered.append({
                    "task_id": task['id'],
                    "task_name": task['name'],
                    "task_args": task['args'],
                })

            
        return {
            "status": 200,
            "message": "Scraping Status",
            "result": {
                "active": list_task,
                "scheduled": list_task_scheduled,
                "reserved": list_task_reserved,
                "registered": list_task_registered,
            }
        }
    except:
        return {
            "status": 400,
            "message": "No Task Found"
        }

@app.route("/scrap-status/<task_id>")
def scrap_status_by_task_id(task_id):
    try:
        result = celery.AsyncResult(task_id)
        return {
            "status": 200,
            "message": "Scraping Status by Task ID",
            "result": {
                "task_id": result.id,
                "task_status": result.status,
            }
        }
    except:
        return {
            "status": 400,
            "message": "Task ID Not Found"
        }

@app.route("/scrap-terminate-all")
def scrap_terminate_all():
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
        return {
            "status": 200,
            "message": "Job Scrap-All Terminated"
        }
    except:
        return {
            "status": 400,
            "message": "No Job Scrap-All Found"
        }

@app.route("/scrap-terminate")
def scrap_terminate():
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_province':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_city':
                    celery.control.revoke(task['id'], terminate=True)
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_province':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_city':
                    celery.control.revoke(task['id'], terminate=True)
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_province':
                    celery.control.revoke(task['id'], terminate=True)
                if task['name'] == 'job_scraping_to_spreadsheet_by_city':
                    celery.control.revoke(task['id'], terminate=True)
        return {
            "status": 200,
            "message": "All Job Terminated"
        }
    except:
        return {
            "status": 400,
            "message": "No Job Found"
        }

@app.route("/scrap-terminate/<province_code>")
def scrap_terminate_by_province(province_code):
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    celery.control.revoke(task['id'], terminate=True)
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    celery.control.revoke(task['id'], terminate=True)
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_province' and task['args'][0] == province_code:
                    celery.control.revoke(task['id'], terminate=True)
        return {
            "status": 200,
            "message": "Scraping by Province with Province Code " + province_code + " Terminate"
        }
    except:
        return {
            "status": 400,
            "message": "Scraping by Province with Province Code " + province_code + " Not Found"
        }

@app.route("/scrap-terminate/<province_code>/<city_code>")
def scrap_terminate_by_city(province_code, city_code):
    try:
        inspect = celery.control.inspect()
        active = inspect.active()
        schedule = inspect.scheduled()
        reserved = inspect.reserved()
        for worker in active:
            for task in active[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    celery.control.revoke(task['id'], terminate=True)
        for worker in schedule:
            for task in schedule[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    celery.control.revoke(task['id'], terminate=True)
        for worker in reserved:
            for task in reserved[worker]:
                if task['name'] == 'job_scraping_to_spreadsheet_by_city' and task['args'][0] == province_code and task['args'][1] == city_code:
                    celery.control.revoke(task['id'], terminate=True)
        return {
            "status": 200,
            "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Terminated"
        }
    except:
        return {
            "status": 400,
            "message": "Scraping by City with Province Code " + province_code + " and City Code " + city_code + " Not Found"
        }

@app.route("/")
def hello():
    return "Scraping APP PEMILU 2024 vs Kawal Pemilu 2024 API"
