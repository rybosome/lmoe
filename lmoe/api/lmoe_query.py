from dataclasses import dataclass
from string import Template
from typing import Optional


_PROMPT_TEMPLATE = Template(
    """
===stdin-context===
$stdin_context
===stdin-context===
===paste-context===
$paste_context
===paste-context===
===user-query===
$user_query
===user-query===
-response-
"""
)

@dataclass
class LmoeQuery:
    """A query plus the associated STDIN/paste context to be passed to an underlying lmoe model."""
    stdin_context: Optional[str]
    paste_context: Optional[str]
    user_query: str

    def render(self) -> str:
        """Render all context and the query into a form suitable for sending to an lmoe model."""
        return _PROMPT_TEMPLATE.substitute(
                stdin_context=self.stdin_context,
                paste_context=self.paste_context,
                user_query=self.user_query)
