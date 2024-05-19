from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_BASE_URL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

cached_colors = {}


def get_color_via_gpt(product_name: str) -> str:
    if product_name in cached_colors:
        return cached_colors[product_name]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be given a word, which could be a fruit or something else, and your task is to identify and return its color in one word, for example: Red. If you don't know the specific color, return unknown."
            },
            {
                "role": "user",
                "content": product_name
            }
        ],
        temperature=0.3,  # we don't need randomness here
        max_tokens=64)
    color = completion.choices[0].message.content

    cached_colors[product_name] = color

    return color
