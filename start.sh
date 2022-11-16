#!/bin/sh
locust --config=app/locust.conf -f=app/locustfiles/locustfile_first_stage.py --csv=alemira_first_stage --html=alemira_first_stage_report.html --logfile=alemira_first_stage.log
locust --config=app/locust.conf -f=app/locustfiles/locustfile_second_stage.py --csv=alemira_second_stage --html=alemira_second_stage_report.html --logfile=alemira_second_stage.log