import os
from typing import get_type_hints, Union
from dotenv import load_dotenv

load_dotenv()

class AppConfigError(Exception):
    pass

def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136 
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']

def _get_secrets(file:str)->dict:
    in_docker = os.environ.get('IN_DOCKER', False)
    path =  f'/run/secrets/{file}' if in_docker else f'../../{file}.txt'
    dict = {}
    with open(path) as fs:
        for line in fs.readlines():
            if line.strip()=="":
                continue
            parts = line.split("=")
            dict[parts[0].strip()] = parts[1].replace('"', '').replace("'", "").strip()
    return dict


# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values
class AppConfig:
    ENV:str = 'production'
    DEBUG:bool = False

    USE_OPENAI:bool = True
    USE_APIFY:bool = False

    OPENAI_API_KEY:str = ""

    GOOGLE_API_KEY:str=''
    GOOGLE_CSE_ID:str=''

    APIFY_API_TOKEN:str = ""

    HUGGINGFACE_CACHE:str = "/storage/huggingface"
    MODEL_TOKEN:str = "mistralai/Mistral-7B-Instruct-v0.1"
    MODEL_GEN:str = "mistralai/Mistral-7B-Instruct-v0.1"
    MODEL_EMBEDDINGS:str = "sentence-transformers/all-mpnet-base-v2"
    
    POSTGRES_HOST:str = "db"
    POSTGRES_PORT:str = "5432"
    POSTGRES_DB:str = "vectordb"
    POSTGRES_USER:str = "vectoruser"
    POSTGRES_PASSWORD:str = "vectorpwd"

    REDIS_URL:str = "redis://redis:6379"
    REDIS_QUEUE:str = "langora-task"
    REDIS_CHANNEL:str = "langora-msg"

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """
    def __init__(self, env):
        secrets = _get_secrets("api_secrets")
        for field in self.__annotations__:
            if not field.isupper():
                continue
            
            default_value = getattr(self, field, None)
            
            #Fill will secret if available
            secret = secrets.get(field)
            if secret :                
                self.__setattr__(field, secret)
                os.environ[field] = secret
                continue

            # Raise AppConfigError if required field not supplied
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )
            )        

    def __repr__(self):
        return str(self.__dict__)

# Expose Config object for app to import
Config = AppConfig(os.environ)
# Force for local dev
in_docker = os.environ.get('IN_DOCKER', False)
if not in_docker:
    Config.HUGGINGFACE_CACHE = "../../storage/huggingface"
    Config.POSTGRES_HOST = "localhost"
    Config.REDIS_URL = "redis://localhost:6379"