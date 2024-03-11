# coverletter.ai
Generate a cover letter based on the url of the application text and your applicant profile consisting of CV, motivation and previous cover letters etc.

# Prerequisites
1. Docker
2. GCloud account with project set up
3. pipx installed with hatch

# How do i run it?
This tool uses the gcloud api. Therefore certain steps need to be taken before being able to use googles API.
This installation expects you to already have a Google Cloud account and project set up.
1. `gcloud init`
2. `gcloud auth application-default login`
3. [Setup a Service Account](https://cloud.google.com/iam/docs/service-accounts-create#python)
4. Enable VertexAI API on your project
5. Use `gcloud config set project PROJECT_ID`
6. Install the packages using hatch `hatch shell`
7. Run the flask app using `flask run` or use the docker container `docker run coverletter`

# How do i develop it for my usecase?
Install the development environment using hatch: `hatch -e dev shell`
Afterwards you can think about other things. 

# Notes
The structure of this app was inspired by https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/ and https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world.