from vertexai.language_models import TextGenerationModel

model = TextGenerationModel.from_pretrained("text-bison@002")

print(model.predict(
    "What is the best recipe for banana bread? Recipe:",
    # The following are optional parameters:
    #max_output_tokens=128,
    #temperature=0,
    #top_p=1,
    #top_k=5,
))
