# LenfestWritingAgent
Prototype to explore a writing agent to assist journalists with creating news articles

## Setup
You will first need to create an Azure AI language service resource at https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics, using the default features, and update the .env file with its endpoint and key.  

Then, create a Bing search resource at https://portal.azure.com/?feature.customportal=false#create/Microsoft.BingSearch and update the .env file with its endpoint and key.  You are also welcome to modify the number of search results returned from a Bing search.  

Finally, use the following commands in a python environment (such as an Anaconda prompt window) to set up your environment. This creates and activates an environment and installs the required packages. For subsequent runs after the initial install, you will only need to activate the environment and then run the python script.

### First run
```
conda create --name writer -y
conda activate writer

pip install -r requirements.txt
python writer.py
```

### Subsequent runs
```
conda activate writer
python writer.py
```
