import os
import requests
import gradio as gr
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Load the endpoints and keys from the environment variables.
load_dotenv()
azure_language_endpoint = os.environ.get("AZURE_LANGUAGE_ENDPOINT")
azure_language_api_key = os.environ.get("AZURE_LANGUAGE_API_KEY")
bing_endpoint = os.environ.get("BING_ENDPOINT")
bing_api_key = os.environ.get("BING_API_KEY")
search_results_count = os.environ.get("SEARCH_RESULTS_COUNT")



def get_entities(text: str) -> list:
    text_analytics_client = TextAnalyticsClient(endpoint=azure_language_endpoint, credential=AzureKeyCredential(azure_language_api_key))

    # TODO: split into sentences here?  See https://learn.microsoft.com/en-us/answers/questions/1149065/does-azure-have-an-api-for-separating-sentences-wi
    document = [text]  
    result = text_analytics_client.recognize_entities(document)
    # TODO: need better error handling here
    
    print("ENTITIES 2: ")
    print(result)
    # Example:
    #[RecognizeEntitiesResult(id=0, entities=[CategorizedEntity(text=Jennifer Marsman, category=Person, subcategory=None, length=16, offset=0, confidence_score=1.0), CategorizedEntity(text=William, category=Person, subcategory=None, length=7, offset=39, confidence_score=0.99), CategorizedEntity(text=yesterday, category=DateTime, subcategory=Date, length=9, offset=70, confidence_score=1.0), CategorizedEntity(text=nuptuals, category=Event, subcategory=None, length=8, offset=86, confidence_score=0.93), CategorizedEntity(text=Westminster Abbey, category=Location, subcategory=None, length=17, offset=108, confidence_score=0.98), CategorizedEntity(text=London, category=Location, subcategory=City, length=6, offset=129, confidence_score=1.0)], warnings=[], statistics=None, is_error=False, kind=EntityRecognition)]

    # Quick scan for debugging only
    for entity in result[0].entities:
        print(f"Text: {entity.text}, Category: {entity.category}")

    return result[0].entities


# Perform a web search using the Bing Web Search API.  
def get_bing_snippet(query: str) -> str:
    # Set the parameters for the API request.
    count = search_results_count       # Number of search results to return
    params = {
        'q': query,
        'count': count,
    }

    # Set the headers for the API request, including the subscription key.
    headers = {
        'Ocp-Apim-Subscription-Key': bing_api_key,
    }

    # Make the API request.
    response = requests.get(bing_endpoint, params=params, headers=headers)
    print("BING: ")
    print(response.json())
    
    # Check if the request was successful (HTTP status code 200).
    if response.status_code == 200:
        search_results = response.json()
        # Extract and structure the search results.
        results_list = []
        for result in search_results['webPages']['value']:
            result_tuple = (result['name'], result['snippet'], result['url'])
            results_list.append(result_tuple)
        return tuple(results_list)
    else:
        error = f"Error: {response.status_code} - {response.text}"
        print(error)
        return error


def assist(inputText):
    output = "Here are some news snippets related to the entities in your text:\n"
    
    # Parse the input text and extract the entities
    entities = get_entities(inputText)
    
    # Call Bing API to get news articles on the entities
    for entity in entities:
        print(entity)
        print(entity.text)
        print(entity.category)
        # TODO: exclude certain entity categories?  
        news_snippets = get_bing_snippet(entity.text)
        print("NEWS SNIPPETS: ")
        print(news_snippets)
        output += f"\n{entity.text}:  ({entity.category})\n"
        for webpage in news_snippets:
            output += f"* News snippet from {webpage[2]}: {webpage[1]} \n"

    return output


demo = gr.Interface(
    fn=assist,
    inputs=[gr.Textbox(label="Craft your compelling news article", lines=30)],
    outputs=[gr.Textbox(label="Sidebar", lines=30)],
    # TODO: consider https://github.com/gradio-app/gradio/issues/2303 for RichTextBox
)


demo.launch()