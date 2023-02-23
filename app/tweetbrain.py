import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 32


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)
    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}"
        )


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generate_keywords(prompt: str) -> List[str]:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related hashtags for {prompt}: "
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text.
    keywords_text: str = response["choices"][0]["text"]

    # Strip whitespace.
    keywords_text = keywords_text.strip()
    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")
    return keywords_array


def generate_branding_snippet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"generate me a tweet about {prompt} without hashtags"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text.
    tweet: str = response["choices"][0]["text"]

    # Strip whitespace.
    tweet = tweet.strip()

    # Add ... to truncated statements.
    last_char = tweet[-1]
    if last_char not in {".", "!", "?"}:
        tweet += "..."

    print(f"Snippet: {tweet}")
    return tweet


if __name__ == "__main__":
    main()