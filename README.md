Generate word clouds for reflection responses

Set-up:

	- set-up venv (optional)
	- pip install -r requirements.txt
	- create ".env" file in root with the following keys:
		CANVAS_TOKEN=" {your token here} "
		CANVAS_URL="https://uncc.instructure.com"
		COURSE_ID="176637"    #fall 2022 datamining course id

	- python3 reflection_viz.py --name="reflection 1"
