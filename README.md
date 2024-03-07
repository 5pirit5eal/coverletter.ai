# coverletter.ai
Generate a cover letter based on the url of the application text and your applicant profile consisting of CV, motivation and previous cover letters etc.

# Prerequisites
1. Docker
2. GCloud account with project set up


# How do i run it?
This tool uses the gcloud api. Therefore certain steps need to be taken before being able to use googles API.
This installation expects you to already have a Google Cloud account and project set up.
1. `gcloud init`
2. `gcloud auth application-default login`
3. [Setup a Service Account](https://cloud.google.com/iam/docs/service-accounts-create#python)
4. Enable VertexAI API on your project
5. Use `gcloud config set project PROJECT_ID`
6. Install the packages in requirements.txt
7. Run the streamlit app using `streamlit run app/main.py` or use the docker container `docker run coverletter`

# How do i develop it for my usecase?
Well this depends on what you want to do... But to get started i would suggest setting up the development environment:
1. `pip install pip poetry wheel setuptools -U`
3. `poetry install`

This will install poetry on your base python. If you do not want this, then 

# Notes
The structure of this app was inspired by https://github.com/markdouthwaite/streamlit-project/blob/master/app.py and https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/.
