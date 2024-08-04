import os

from browsergym.utils.obs import flatten_axtree_to_str

from opendevin.core.exceptions import BrowserUnavailableException
from opendevin.core.schema import ActionType
from opendevin.events.action import BrowseInteractiveAction, BrowseURLAction
from opendevin.events.observation import BrowserOutputObservation
from opendevin.runtime.browser.browser_env import BrowserEnv

from opendevin.core.logger import opendevin_logger as logger

async def browse(
    action: BrowseURLAction | BrowseInteractiveAction, browser: BrowserEnv | None
) -> BrowserOutputObservation:
    if browser is None:
        raise BrowserUnavailableException()

    if isinstance(action, BrowseURLAction):
        # legacy BrowseURLAction
        asked_url = action.url
        if not asked_url.startswith('http'):
            asked_url = os.path.abspath(os.curdir) + action.url
        action_str = f'goto("{asked_url}")'

    elif isinstance(action, BrowseInteractiveAction):
        # new BrowseInteractiveAction, supports full featured BrowserGym actions
        # action in BrowserGym: see https://github.com/ServiceNow/BrowserGym/blob/main/core/src/browsergym/core/action/functions.py
        action_str = action.browser_actions
    else:
        raise ValueError(f'Invalid action type: {action.action}')

    try:
        # obs provided by BrowserGym: see https://github.com/ServiceNow/BrowserGym/blob/main/core/src/browsergym/core/env.py#L396
        obs = browser.step(action_str)
        try:
            axtree_txt = flatten_axtree_to_str(
                obs['axtree_object'],  # accessibility tree object
                extra_properties=obs[
                    'extra_element_properties'
                ],  # extra element properties
                with_clickable=True,
                filter_visible_only=True,
            )
        except Exception as e:
            logger.error(
                f'Error when trying to process the accessibility tree: {e}, obs: {obs}'
            )
            axtree_txt = f'AX Error: {e}'
        return BrowserOutputObservation(
            content=obs['text_content'],  # text content of the page
            open_pages_urls=obs['open_pages_urls'],  # list of open pages
            active_page_index=obs['active_page_index'],  # index of the active page
            axtree_txt=axtree_txt,  # accessibility tree text
            last_browser_action=obs['last_action'],  # last browser env action performed
            focused_element_bid=obs['focused_element_bid'],  # focused element bid
            screenshot=obs['screenshot'],  # base64-encoded screenshot, png
            url=obs['url'],  # URL of the page
            error=True if obs['last_action_error'] else False,  # error flag
            last_browser_action_error=obs[
                'last_action_error'
            ],  # last browser env action error
        )
    except Exception as e:
        return BrowserOutputObservation(
            content=str(e),
            screenshot='',
            error=True,
            last_browser_action_error=str(e),
            url=asked_url if action.action == ActionType.BROWSE else '',
        )
