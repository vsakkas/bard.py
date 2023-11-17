import pytest
from thefuzz import fuzz

from bard import BardClient


@pytest.mark.asyncio
async def test_ask() -> bool:
    expected_responses = [
        "Hello there! How can I help you today?",
        "Hello there! How can I help you today? [Image of Bard AI Chatbot]",
        "Hello there! How can I help you today? [Image of Bard, a large language model from Google AI]",
        "Hello there! How can I help you today? [Image of a friendly robot with a warm smile]",
    ]

    async with BardClient() as bard:
        response = await bard.ask("Hello, Bard!")

        score = 0
        for expected_response in expected_responses:
            score = fuzz.token_sort_ratio(response, expected_response)
            if score >= 80:
                return True

        assert False, f"Unexpected response: {response}, match score: {score}"


@pytest.mark.asyncio
async def test_ask_multiple_prompts() -> None:
    async with BardClient() as bard:
        _ = await bard.ask("Tell me a joke.")

        _ = await bard.ask("Tell me another one.")
