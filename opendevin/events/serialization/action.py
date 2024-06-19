from opendevin.core.exceptions import LLMMalformedActionError
from opendevin.core.logger import opendevin_logger as logger
from opendevin.events.action.action import Action
from opendevin.events.action.agent import (
    AgentDelegateAction,
    AgentFinishAction,
    AgentRecallAction,
    AgentRejectAction,
    ChangeAgentStateAction,
)
from opendevin.events.action.browse import BrowseInteractiveAction, BrowseURLAction
from opendevin.events.action.commands import (
    CmdKillAction,
    CmdRunAction,
    IPythonRunCellAction,
)
from opendevin.events.action.empty import NullAction
from opendevin.events.action.files import FileReadAction, FileWriteAction
from opendevin.events.action.message import MessageAction
from opendevin.events.action.tasks import AddTaskAction, ModifyTaskAction
from opendevin.events.event import EventSource

actions = (
    NullAction,
    CmdKillAction,
    CmdRunAction,
    IPythonRunCellAction,
    BrowseURLAction,
    BrowseInteractiveAction,
    FileReadAction,
    FileWriteAction,
    AgentRecallAction,
    AgentFinishAction,
    AgentRejectAction,
    AgentDelegateAction,
    AddTaskAction,
    ModifyTaskAction,
    ChangeAgentStateAction,
    MessageAction,
)

ACTION_TYPE_TO_CLASS = {action_class.action: action_class for action_class in actions}  # type: ignore[attr-defined]


def action_from_dict(action: dict) -> Action:
    if not isinstance(action, dict):
        raise LLMMalformedActionError('action must be a dictionary')
    action = action.copy()
    if 'action' not in action:
        raise LLMMalformedActionError(f"'action' key is not found in {action=}")
    if not isinstance(action['action'], str):
        raise LLMMalformedActionError(
            f"'{action['action']=}' is not defined. Available actions: {ACTION_TYPE_TO_CLASS.keys()}"
        )
    action_class = ACTION_TYPE_TO_CLASS.get(action['action'])
    if action_class is None:
        raise LLMMalformedActionError(
            f"'{action['action']=}' is not defined. Available actions: {ACTION_TYPE_TO_CLASS.keys()}"
        )
    args = action.get('args', {})
    try:
        decoded_action = action_class(**args)
        decoded_action._source = action.get('source', EventSource.USER)
        logger.info(decoded_action, extra={'msg_type': 'ACTION'})
    except TypeError:
        raise LLMMalformedActionError(f'action={action} has the wrong arguments')
    return decoded_action
