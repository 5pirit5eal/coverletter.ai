from vertexai.language_models import TextGenerationModel
from bs4 import BeautifulSoup
import requests
import argparse
from coverletter.db import Resume, ResumeItem, Prompt, JobPosting, CoverLetter, Config, Base
from sqlalchemy import create_engine, insert

engine = create_engine("sqlite+pysqlite:///app.db", echo=True, future=True)
Base.metadata.create_all(engine, checkfirst=True)


def get_text(url: str | None = None) -> str:
    """Gets the text for a job posting.

    This function checks the database if the job posting is already stored.
    If not, it scrapes the text from the website and stores it in the database.
    If None is passed, the function returns a default job posting from the database.

    Args:
        url (str, optional): URL of the job posting. Defaults to None.

    Returns:
        str: The text of the job posting.
    """


def get_cv() -> str:
    with open("private/cv.md", "r") as file:
        cv = file.read()
    return cv


def create_prompt(url: str | None = None) -> Prompt:
    text = get_text(url)
    cv = get_cv()
    prompt = "Generate a cover letter for the following application: \n" + text
    prompt += "\n Based on the following CV: \n" + cv
    prompt += "\n It is crucial to not hallucinate skills that are not present in the CV. Try to make the cover letter as relevant as possible. \n"
    return Prompt(text=prompt)


def main():
    model = TextGenerationModel.from_pretrained("text-bison@002")

    # https://www.jcchouinard.com/web-scraping-with-beautifulsoup-in-python/
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # text = soup.get_text()

    # load job description from folder
    with open("private/job_description.txt", "r") as file:
        text = file.read()

    prompt = "Generate a cover letter for the following application: \n" + text

    # load cv from folder
    with open("private/cv.md", "r") as file:
        cv = file.read()

    prompt += "\n Based on the following CV: \n" + cv
    prompt += "\n It is crucial to not hallucinate skills that are not present in the CV. Try to make the cover letter as relevant as possible. \n"

    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()
    prompt = translate_client.translate(prompt, target_language="de")

    response = model.predict(prompt, max_output_tokens=1024)
    for candidate in response.candidates:
        print(candidate)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("url", help="URL of the website")
    # args = parser.parse_args()
    # main(args.url)
    main()
