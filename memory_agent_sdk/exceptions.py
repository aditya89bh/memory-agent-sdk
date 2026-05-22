class MemoryAgentSDKError(Exception):
    """Base exception for Memory Agent SDK errors."""


class MemoryNotFoundError(MemoryAgentSDKError):
    """Raised when a requested memory record cannot be found."""


class MemoryInputError(MemoryAgentSDKError):
    """Raised when a memory operation receives invalid input."""
