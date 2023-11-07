import pytest

from bard import BardClient


@pytest.mark.asyncio
async def test_ask() -> None:
    async with BardClient() as bard:
        _ = await bard.ask("Tell me a joke")


@pytest.mark.asyncio
async def test_ask_multiple_prompts() -> None:
    async with BardClient() as bard:
        _ = await bard.ask("Tell me a joke.")

        _ = await bard.ask("Tell me another one.")
