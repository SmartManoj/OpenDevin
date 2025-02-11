import re

from openhands.core.exceptions import (
    InvalidSummaryResponseError,
    LLMMalformedActionError,
    LLMResponseError,
)
from openhands.core.logger import openhands_logger as logger
from openhands.core.utils import json
from openhands.events.action.agent import AgentSummarizeAction
from openhands.events.event import EventSource
from openhands.events.serialization.action import action_from_dict

WORD_LIMIT = 200
MESSAGE_SUMMARY_WARNING_FRAC = 0.75

SUMMARY_PROMPT_SYSTEM = """
Your job is to summarize a history of previous messages in a conversation between an AI persona and a human. The conversation you are given is a from a fixed context window and may not be complete. Keep your summary less than 200 words, do NOT exceed this word limit.
Only output the summary, do NOT include anything else in your output.
Given the following actions and observations, create a JSON response like this:
{
    "action": "summarize",
    "args": {
        "summarized_actions": "A precise sentence summarizing all the provided actions, written in the first person.",
        "summarized_observations": "A few precise sentences summarizing all the provided observations, written in the third person."
    }
}
Make sure to include in observations any relevant information that the agent needs to remember.
"""


def parse_summary_response(response: str) -> AgentSummarizeAction:
    """
    Parses a JSON summary of events.

    Parameters:
    - response: The response string to be parsed
    Returns:
    - The summary action output by the model
    """
    try:
        try:
            action_dict = json.loads(response)
        except LLMResponseError:
            pattern = r'(?<=Action:\s).+?(?=\s*Observation:)|(?<=Observation:\s).+'
            matches = re.findall(pattern, response.replace('**', ''), re.DOTALL)
            action_summary = matches[0].strip() if matches else None
            observation_summary = matches[1].strip() if len(matches) > 1 else None
            action_dict = {
                'action': 'summarize',
                'args': {
                    'summarized_actions': action_summary,
                    'summarized_observations': observation_summary,
                },
            }

        action = action_from_dict(action_dict)
        if action is None or not isinstance(action, AgentSummarizeAction):
            error_message = f'Expected a summarize action, but the response got {str(type(action)) if action else None}'
            logger.error(error_message)
            raise InvalidSummaryResponseError(error_message)
        action._source = EventSource.AGENT  # type: ignore
    except (LLMResponseError, LLMMalformedActionError) as e:
        logger.error(f'Failed to parse summary response: {str(e)}')
        raise InvalidSummaryResponseError(
            f'Failed to parse the response: {str(e)}'
        ) from e
    return action
