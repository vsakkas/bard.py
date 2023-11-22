from enum import Enum


class ConversationTone(Enum):
    """
    Bard conversation tones. Supported options are:
    - `Default`
    - `Casual`
    - `Simple`
    - `Professional`
    """

    DEFAULT = 0
    CASUAL = 2
    SIMPLE = 4
    PROFESSIONAL = 5
