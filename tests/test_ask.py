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
async def test_ask_casual() -> bool:
    expected_responses = [
        "Hey there! What's up?",
        "Hey there! What's up? What can I do for you today?",
        "Hey! What's up?",
        "Hey! What's up? How can I be of assistance today?",
        "Hey! What's up? What can I do for you today?",
    ]

    async with BardClient() as bard:
        _ = await bard.ask("Hello, Bard!")

        response = await bard.ask("Hello, Bard!", tone="Casual")

        score = 0
        for expected_response in expected_responses:
            score = fuzz.token_sort_ratio(response, expected_response)
            if score >= 80:
                return True

        assert False, f"Unexpected response: {response}, match score: {score}"


@pytest.mark.asyncio
async def test_ask_professional() -> bool:
    expected_responses = [
        "Good day. How may I assist you today?",
        "Greetings and salutations! I am at your service. How may I be of assistance today?",
        "Greetings! How can I be of assistance to you today?",
        "Greetings! I am at your service, ready to assist with your inquiries and requests. Please feel free to ask me anything.",
        "Greetings! I am at your service. Please let me know how I can assist you today.",
        "Greetings! I am at your service. Please let me know how I can be of assistance.",
        "Greetings! Please let me know how I can assist you today.",
        "Greetings, and how may I assist you today?",
        "Greetings, esteemed user. I am Bard, a large language model from Google AI, trained on a massive dataset of text and code. I am at your service",
        "Greetings, esteemed user. I am at your service. Please let me know how I can assist you today.",
        "Greetings, how can I assist you today?",
        "Greetings. How can I be of assistance today?",
        "Greetings. How may I be of assistance today?",
        "Greetings. I am Bard, a large language model from Google AI. How may I be of assistance today?",
        "Greetings. I am at your service. How may I assist you today?",
        "Greetings. I am at your service. Please let me know how I can assist you today.",
        "Greetings. I am at your service. Please let me know how I can be of assistance today.",
        "Greetings. Please let me know how I can assist you today.",
        "Greetings. Please let me know how I can be of assistance to you today.",
        "Greetings. Please let me know how I can be of assistance.",
    ]

    async with BardClient() as bard:
        _ = await bard.ask("Hello, Bard!")

        response = await bard.ask("Hello, Bard!", tone="Professional")

        score = 0
        for expected_response in expected_responses:
            score = fuzz.token_sort_ratio(response, expected_response)
            if score >= 80:
                return True

        assert False, f"Unexpected response: {response}, match score: {score}"


@pytest.mark.asyncio
async def tesk_ask_short() -> bool:
    expected_responses = [
        "4.",
        "You have 1 apple left today.",
        "You have 4 apples left.",
        "You have 4 apples today.",
        "You still have 4 apples.",
    ]

    async with BardClient() as bard:
        _ = await bard.ask(
            "I have 4 apples today. I ate 3 apples yesterday. How many apples do I have today?"
        )

        response = await bard.ask(
            "I have 4 apples today. I ate 3 apples yesterday. How many apples do I have today?",
            length="Short",
        )

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
