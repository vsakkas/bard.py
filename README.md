# <img src="https://raw.githubusercontent.com/vsakkas/bard.py/master/images/logo.svg?token=GHSAT0AAAAAAB7MEK465TODCKRPHN3YQY54ZKGUN4Q" width="28px" /> Bard.py

[![Latest Release](https://img.shields.io/github/v/release/vsakkas/bard.py.svg)](https://github.com/vsakkas/bard.py/releases/tag/v0.2.2)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/vsakkas/bard.py/blob/master/LICENSE)

Python Client for Bard, a Chat Based AI tool by Google.

> [!NOTE]
> This is an **unofficial** client.

## Features

- Connect to Bard, Google's AI-powered personal assistant.
- Ask questions and have a continuous conversation.
- Use asyncio for efficient and non-blocking I/O operations.

## Requirements

- Python 3.10 or newer
- Google account with access to [Bard](https://bard.google.com/)

## Installation

To install Bard.py, run the following command:

```bash
pip install bard-py
```

or, if you use [poetry](https://python-poetry.org/):

```bash
poetry add bard-py
```

> [!TIP]
> Make sure you're using the latest version of Bard.py to ensure best compatibility with Bard.

## Usage

### Prerequisites

To use Bard.py you first need to extract the `__Secure-1PSID` and `__Secure-1PSIDTS` cookies from the Bard web page. These cookies are used to authenticate your requests to the Bard API.

To get the cookies, follow these steps on Chrome:
- Go to the [Bard web page](https://bard.google.com/).
- Write a message on the chat dialog that appears.
- Open the developer tools in your browser (usually by pressing `F12` or right-clicking on the chat dialog and selecting `Inspect`).
- Select the `Application` tab and click on the `Cookies` option to view all cookies associated with `https://bard.google.com`.
- Look for the `__Secure-1PSID` and `__Secure-1PSIDTS` cookies and click on them to expand their details.
- Copy the values of the cookies (they should look like a long string of letters and numbers).

Then, set them as environment variables in your shell:

```bash
export SECURE_1PSID=<your-cookie>
export SECURE_1PSIDTS=<your-other-cookie>
```

or, in your Python code:

```python
os.environ["SECURE_1PSID"] = "<your-cookie>"
os.environ["SECURE_1PSIDTS"] = "<your-other-cookie>"
```

### Example

You can use Bard.py to easily create a CLI client for Bard:

```python
import asyncio

from bard import BardClient


async def main() -> None:
    async with BardClient() as bard:
        while True:
            prompt = input("You: ")

            if prompt == "!reset":
                await bard.reset_conversation()
                continue
            elif prompt == "!exit":
                break

            response = await bard.ask(prompt)
            print(f"Bard: {response}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Bard Client

You can create a Bard Client and initialize a connection with Bard which starts a conversation:

```python
bard = BardClient()

await bard.start_conversation()

# Conversation

await bard.end_conversation()
```

Alternatively, you can use the `async with` statement to keep the code compact:

```python
async with BardClient() as bard:
    # Conversation
```

### Reset Conversation

You can reset the conversation in order to make the client forget the previous conversation:

```python
async with BardClient() as bard:
    # Conversation
    await bard.reset_conversation()
```

### Ask

You can ask Bard questions and get the results:

```python
async with BardClient() as bard:
    response = await bard.ask("When was Bard released?")
    print(response)
```

### Exceptions

When something goes wrong, Sydney.py might throw one of the following exceptions:

| Exception                     | Meaning                                   | Solution                 |
|-------------------------------|-------------------------------------------|--------------------------|
| `CreateConversationException` | Failed to create conversation             | Retry or use new cookies |
| `AskException`                | Failed to get response from Bard          | Retry or use new cookies |

*For more detailed documentation and options, please refer to the code docstrings.*

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vsakkas/bard.py/blob/master/LICENSE) file for details.
