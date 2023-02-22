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
        generate_tweet(user_input)
    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}"
        )


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generate_tweet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPEN_AI_API_KEY")
    enriched_prompt = f"Generate a tweet about: {prompt}"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text.
    twitter_text: str = response["choices"][0]["text"]

    # Strip whitespace.
    twitter_text = twitter_text.strip()

    # Add ... to truncated statements.
    last_char = twitter_text[-1]
    if last_char not in {".", "!", "?"}:
        twitter_text += "..."

    print(f"Snippet: {twitter_text}")
    return twitter_text


if __name__ == "__main__":
    main()

# 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