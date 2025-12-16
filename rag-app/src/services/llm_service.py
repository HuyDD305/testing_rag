from langchain_openai import ChatOpenAI
from ..config.settings import settings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.api_key,
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            base_url=settings.base_url
        )

        self.llm_json = ChatOpenAI(
            api_key=settings.api_key,
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            base_url=settings.base_url,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

        self.llm_thinking = ChatOpenAI(
            api_key=settings.api_key,
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            base_url=settings.base_url,
            extra_body={
                "reasoning": {
                    "enabled": True,
                }
            }
        )

        
    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
        
    def generate_json(self, prompt: str) -> dict:
        response = self.llm_json.invoke(prompt)
        return response.content
    
    def geneerate_messages(self, messages: list) -> str:
        response = self.llm.invoke(messages)
        return response.content



llm_service = LLMService()

messages = [
    SystemMessage(content="You're a helpful programming assistant"),
    HumanMessage(content="Write a Python function to calculate factorial")
]
response = llm_service.geneerate_messages(messages)

# print("Settings API key:", settings.api_key)
# print("Settings base_url:", settings.base_url)
# # response  = llm_service.generate("Hello, how are you?")
# another_response = llm_service.llm.invoke("Hello, how are you?")
# json_response = llm_service.generate_json('Hello, how are you?')
# print(response)
# print(another_response.content)
# print("JSON Response:", json_response)

print("Setting Model Name:", settings.LLM_MODEL)

template = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced programmer and mathematical analyst."),
    ("user", "{problem}")
])

# thinking_mode = llm_service.llm_thinking

# chain = template | thinking_mode

# problem = """Design an algorithm to find the kth largest element in an unsorted array
# with the optimal time complexity. Analyze the time and space complexity
# of your solution and explain why it's optimal."""

# response = chain.invoke({"problem": problem})
# print(response.content)



# another_template = ChatPromptTemplate.from_messages([
#     ("system", "You are an English to French translator."),
#     ("user", "Translate the following sentence to French: '{sentence}'")
# ])

# print(another_template)

# another_chain = another_template | llm_service.llm

# another_response = another_chain.invoke({"sentence": "Hello, how are you?"})
# print(another_response.content)

# prompt = PromptTemplate.from_template("""
# Summarize the following text in one sentence. 

# Respond using ONLY valid JSON: {{"summary": "your one sentence summary"}}

# Text: {text}
# """)

# chain = prompt | llm_service.llm_json | JsonOutputParser()
# result = chain.invoke({"text": "LangChain is a framework for developing applications powered by language models. It enables developers to build applications that can interact with users, process data, and perform complex tasks using natural language."})
# print(result)


from typing_extensions import TypedDict


class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str


    
story_prompt = PromptTemplate.from_template("Write a short story about {topic} in less than 50 words.")

story_chain = story_prompt | llm_service.llm | StrOutputParser()

analysis_prompt = PromptTemplate.from_template("Analyze the following story and provide a brief critique: {story}")

analysis_chain = analysis_prompt | llm_service.llm | StrOutputParser()

enhanced_chain = RunnablePassthrough.assign(story=story_chain).assign(analysis=analysis_chain)

result = enhanced_chain.invoke({"topic": "a brave little toaster"})

print(result)
print("Story:", result["story"])
print("Analysis:", result["analysis"])


print(result.keys())
