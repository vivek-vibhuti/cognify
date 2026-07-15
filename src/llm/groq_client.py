from langchain_groq import ChatGroq


from src.config.settings import  Settings
def get_groq_llm ():
    return ChatGroq(
        api_key = Settings.GROQ_API_KEY,
        model= Settings.MODEL_NAME,
        temperature= Settings.TEMPERATURE
    )
