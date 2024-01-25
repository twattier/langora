# Langora

**Web scraping for knowledge base system**

## Logic
- Define An agent (ex : "an expert in artificial intelligence consulting for businesses")
- The list Topics (ex : "Generative AI", "Large language model", ...)

Then :
1) The LLM (OpenAI or other) will recommend searches to submit to google (With Google API)
2) For each searches : reference the sources from the top responses (10 by default) 
3) For each source : 
    - Extract the text content (with APIFY)
    - Summarization with the LLM (OpenAI or other)

## Installation

### Set up local environement :
```
conda create -n langora python=3.9.18 nodejs
conda activate langora
pip install -r ./langora/requirements.txt
cd ./web
npm install
```

### Build and deploy containers : 
```
docker-compose build
docker-compose up -d
```
## Configuration
env var :...

## CLI Command

### Execute command :
```
python ./langora/cli.py <command> ...
```
OR
```
docker exec -it <langora_container_name> python /app/cli.py <command> ...
```

### Init Database and Knowledge Base :
see cli.py install -h
ex :
```
python cli.py install
    --agent "an expert in artificial intelligence consulting for businesses"
    --topics "Generative AI", "Large language model", "Generative AI business use cases", "Generative AI development methodology"
```
