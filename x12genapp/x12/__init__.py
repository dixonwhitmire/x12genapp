ELIGIBILITY_TRANSACTION_CODE = '270'
SUPPORTED_TRANSACTION_CODES = [ELIGIBILITY_TRANSACTION_CODE]


class UnsupportedTransactionException(Exception):
    """
    Indicates that a X12 Transaction Type is not currently supported
    """
    pass


class InvalidControlSegment(Exception):
    """
    Raised when a X12 message as an invalid control segment (ISA, GS, GE, or IEA)
    """
    pass
