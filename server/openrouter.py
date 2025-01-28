import json
import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
    model="deepseek/deepseek-r1-distill-llama-70b",
    messages=[
        {
            "role": "user",
            "content": "python: code only: def csvs_to_duck_db_table(csv_paths: List[str]) -> List[str] - new duck db file paths",
        }
    ],
    # include_reasoning=True, not working
)
print(completion)
print(json.dumps(completion, indent=4))
