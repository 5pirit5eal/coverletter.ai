from vertexai.language_models import TextGenerationModel

model = TextGenerationModel.from_pretrained("text-bison@002")

response = model.predict(
    "Complete this sentence: A catchy tagline for a flower shop that sells bouquets of dried flowers is Dried flowers that",
    # The following are optional parameters:
    #max_output_tokens=128,
    #temperature=0,
    #top_p=1,
    #top_k=5,
)

for candidate in response.candidates:
    print(candidate)

