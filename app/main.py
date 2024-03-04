from vertexai.language_models import TextGenerationModel
from bs4 import BeautifulSoup
import requests
import argparse

def main():
    model = TextGenerationModel.from_pretrained("text-bison@002")
    
    # https://www.jcchouinard.com/web-scraping-with-beautifulsoup-in-python/
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # text = soup.get_text()

    # load job description from folder
    with open('private/job_description.txt', 'r') as file:
        text = file.read()
    
    prompt = "Generate a cover letter for the following application: \n" + text

    # load cv from folder
    with open('private/cv.md', 'r') as file:
        cv = file.read()
    
    prompt += "\n Based on the following CV: \n" + cv
    prompt += "\n It is crucial to not hallucinate skills that are not present in the CV. Try to make the cover letter as relevant as possible. \n"
    
    response = model.predict(prompt, max_output_tokens=1024)
    for candidate in response.candidates:
        print(candidate)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("url", help="URL of the website")
    # args = parser.parse_args()
    # main(args.url)
    main()
