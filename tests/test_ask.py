import pytest

from bard import BardClient


@pytest.mark.asyncio
async def test_ask() -> None:
    async with BardClient() as bard:
        _ = await bard.ask("Tell me a joke")
