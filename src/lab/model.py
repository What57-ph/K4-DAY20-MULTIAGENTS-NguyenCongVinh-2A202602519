"""PROVIDED - do not edit. Builds the chat model from environment variables (see .env.example).

Two configurations are supported (the first that matches wins):

1. Azure OpenAI or an OpenAI-compatible gateway - set all three variables:
   AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_MODEL
   (optional: AZURE_OPENAI_API_VERSION, used only for real Azure endpoints).
2. Any LangChain provider - set LAB_MODEL="<provider>:<model>" (default "deepseek:deepseek-chat")
   and the key variable of that provider (for example DEEPSEEK_API_KEY).
"""
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def make_model():
    """Return a chat model configured from the environment."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_MODEL")
    configured_model = deployment or os.getenv("LAB_MODEL", "deepseek:deepseek-chat")

    # gpt-6-luna rejects temperature at the API boundary, including temperature=0.
    # Keep the lab's deterministic default for providers that accept the parameter.
    model_id = configured_model.rsplit(":", 1)[-1].lower()
    model_options = {}
    if not (model_id == "gpt-6-luna" or model_id.startswith("gpt-6-luna-")):
        model_options["temperature"] = float(os.getenv("LAB_TEMPERATURE", "0"))
    else:
        model_options["reasoning_effort"] = "none"

    if endpoint and key and deployment:
        if "openai.azure.com" in endpoint or "cognitiveservices.azure.com" in endpoint:
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_endpoint=endpoint, api_key=key, azure_deployment=deployment,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
                timeout=120, **model_options,
            )
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(base_url=endpoint, api_key=key, model=deployment, timeout=120, **model_options)
    return init_chat_model(configured_model, **model_options)
