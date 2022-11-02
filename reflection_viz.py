import dotenv
import os
import requests 
import click
import pandas as pd
import matplotlib.pyplot as plt
from requests.structures import CaseInsensitiveDict
from canvasapi import Canvas 
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path

#load env variables
dotenv.load_dotenv()

CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN") #canvas api token
CANVAS_URL = os.environ.get("CANVAS_URL") 
COURSE_ID = os.environ.get("COURSE_ID")

stopwords = set(STOPWORDS)

@click.command()
@click.option("--name", default = None, help = "Which reflection to pull. ie. 'reflection 1'")
def main(name: str):
	
	def create_wordcloud(column):

		path = Path("wordclouds/" + str(name + " " + column[9:].split('?')[0]).replace('.', '').replace('/', ''))
		print(path)

		# combine all responses into single string
		resp = ""
		for i in report_df.index:
		    resp = resp + str(report_df[column].iloc[i])


		wordcloud = WordCloud(width = 800, height = 800,
	                background_color ='white',
	                stopwords = stopwords,
	                min_font_size = 10).generate(resp)
	                     
		plt.figure(figsize = (8, 8), facecolor = None)
		plt.imshow(wordcloud)
		plt.axis("off")
		plt.tight_layout(pad = 0)
		 
		plt.savefig( path ) 

	
	if name is None:
		raise ValueError('Please provide a reflection to be pulled using --name option. Example: python3 reflection_viz --name="reflection 1"')

	canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

	course = canvas.get_course(COURSE_ID)

	quizzes = course.get_quizzes()

	for q in quizzes:
		if name.lower() in str(q.title).lower():
			reflection = q
			break

	report_resp = reflection.create_report(report_type = 'student_analysis')

	report_df = pd.read_csv(report_resp.file['url']) 

	report_df.to_csv(f'{name}.csv') 

	with open('questions.txt') as f:
		questions = f.read().splitlines()

	cols_of_interest = []
	for col in report_df.columns:
		for q in questions:
			if q in col:
				cols_of_interest.append(col)

	for question in cols_of_interest:
		create_wordcloud(question)

if __name__ == "__main__":
	main()
