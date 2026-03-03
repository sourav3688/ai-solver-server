import base64
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.2")


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def solve_question_from_image(image_path: str):

    base64_image = encode_image(image_path)
    data_url = f"data:image/jpeg;base64,{base64_image}"
    
    # # LLM Topics
    # - Understanding LLMs and LVMs
    # - Understanding of GPU Computing
    # - Designing Chatbots, Virtual Assistants and Dialog Systems
    # - Designing Advance RAG pipeline concepts
    # - Exploring finetuning of Model
    # - Risk Management: Privacy, Security and Compliance
    # - Tools and Frameworks for Evaluation: Rogue, Deepeval, Meteor, Blue
    # - Few-Shot Learning Techniques in Language Models
    # - Edge AI
    # - Ethical Considerations in AI Language Model Bias Detection and Mitigation

    response = client.responses.create(
        model=MODEL_NAME,
        temperature=0,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
                            Read and understand the test question carefully.

                            If the question contains multiple choice options,
                            extract them exactly as written.

                            Your gole is to provide the best answer(s) based on the question and the options if multiple options are correct then add them in your answer.

                            Topics covered in this Prompt Engineering assessment is mostly as below:
                            - Elements of a prompt
                            - Types of Prompts
                            - Nature of Prompts
                            - Properties of Prompts
                            - Prompt Designing
                            - Prompting Techniques
                            - Hard Prompt & Soft Prompts
                            - Deep Dive on Advanced Prompting
                            - Prompt Tuning
                            - Quality Standard & Guidelines
                            - Ethical Consideration
                            - Style & Keywords

                            Respond ONLY in valid JSON:

                            {
                                "question": "...",
                                "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                                "answer": "...",
                                "explanation": "..."
                            }
                        """
                    },
                    {
                        "type": "input_image",
                        "image_url": data_url,
                    },
                ],
            }
        ],
    )

    raw_output = response.output_text

    try:
        result = json.loads(raw_output)

        if "options" not in result:
            result["options"] = []

        return result

    except Exception:
        return {
            "question": "Parsing Error",
            "options": [],
            "answer": "Model did not return valid JSON",
            "explanation": raw_output
        }