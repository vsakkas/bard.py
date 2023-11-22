import json
import re
from os import environ

from aiohttp import ClientSession

from bard.constants import BARD_STREAM_GENERATE_URL, BARD_URL, BARD_VERSION, HEADERS
from bard.enums import ConversationTone
from bard.exceptions import (
    AskException,
    CreateConversationException,
    NoResponseException,
)
from bard.utils import double_json_stringify, random_digit_as_string


class BardClient:
    def __init__(
        self, secure_1psid: str | None = None, secure_1psidts: str | None = None
    ) -> None:
        """
        Client for Bard.
        """
        self.secure_1psid = secure_1psid if secure_1psid else environ["SECURE_1PSID"]
        self.secure_1psidts = (
            secure_1psidts if secure_1psidts else environ["SECURE_1PSIDTS"]
        )
        self.conversation_id: str | None = None
        self.response_id: str | None = None
        self.choice_id: str | None = None
        self.session: ClientSession | None = None

    async def __aenter__(self) -> "BardClient":
        await self.start_conversation()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close_conversation()

    async def _get_session(self, force_close: bool = False) -> ClientSession:
        # Use cookies to create a conversation.
        cookies = {
            "__Secure-1PSID": self.secure_1psid,
            "__Secure-1PSIDTS": self.secure_1psidts,
        }

        if self.session and not self.session.closed and force_close:
            await self.session.close()
            self.session = None

        if not self.session:
            self.session = ClientSession(
                headers=HEADERS,
                cookies=cookies,
            )

        return self.session

    def _build_ask_parameters(self) -> dict:
        return {
            "bl": BARD_VERSION,
            "_reqid": random_digit_as_string(7),
            "rt": "c",
        }

    def _build_ask_arguments(self, prompt: str, tone: str | None) -> dict:
        conversation_arguments = None
        if tone:
            tone_value = getattr(ConversationTone, tone.upper()).value
            conversation_arguments = [0, [tone_value], None, None, None, None, []]

        request_data = [
            [prompt, 0, None, [], None, None, 0],
            [""],  # TODO: Support language codes, like "en"
            [
                self.conversation_id if self.conversation_id else "",
                "",
                "",
                self.response_id if self.response_id else None,
                self.choice_id if self.choice_id else None,
                [],
            ],
            "",  # TODO: Find what this is
            "",  # TODO: Find what this is
            conversation_arguments,
            [1],
            1,
            [],
            [],
            1,
            0,
        ]

        return {
            "f.req": double_json_stringify(request_data),
            "at": self.snlm0e,
        }

    async def _ask(self, prompt: str, tone: str | None = None) -> str | None:
        parameters = self._build_ask_parameters()
        arguments = self._build_ask_arguments(prompt, tone)

        session = await self._get_session()

        async with session.post(
            BARD_STREAM_GENERATE_URL, params=parameters, data=arguments
        ) as response:
            if response.status != 200:
                raise AskException(
                    f"Failed to get response, received status: {response.status}"
                )

            response_text = await response.text()
            response_data = json.loads(response_text.splitlines()[3])
            # No actual response in the returned data.
            if not response_data or not response_data[0][2]:
                return None

            message = json.loads(response_data[0][2])

            self.conversation_id = message[1][0]
            self.response_id = message[1][1]
            self.choice_id = message[4][0][0]

            return message[4][0][1][0]

    async def start_conversation(self) -> None:
        """
        Connect to Bard and create a new conversation.
        """
        session = await self._get_session(force_close=True)

        async with session.get(BARD_URL) as response:
            if response.status != 200:
                raise CreateConversationException(
                    f"Failed to create conversation, received status: {response.status}"
                )

            response_text = await response.text()

            snlm0e_dict = re.search(r"\"SNlM0e\":\"(?P<value>.*?)\"", response_text)

            if not snlm0e_dict:
                raise CreateConversationException(
                    "Failed to create conversation, SNlM0e value was not found."
                )

            self.snlm0e = snlm0e_dict.group("value")

    async def ask(self, prompt: str, tone: str | None = None) -> str:
        """
        Send a prompt to Bard and return the answer.

        Parameters
        ----------
        prompt: str
            The prompt that needs to be sent to Bard.
        tone: str
            The tone that Bard will use in the next response. If no value is
            given, it will use a default tone.

        Returns
        -------
        str
            The response from Bard.
        """
        response = await self._ask(prompt=prompt, tone=tone)
        if not response:
            raise NoResponseException("No response was returned")

        return response

    async def reset_conversation(self) -> None:
        """
        Clear current conversation information and connection and start new ones.
        """
        await self.close_conversation()
        await self.start_conversation()

    async def close_conversation(self) -> None:
        """
        Close all connections to Bard. Clear conversation information.
        """
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

        self.conversation_id = None
        self.response_id = None
        self.choice_id = None
