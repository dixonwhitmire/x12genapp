from x12genapp.x12 import (InvalidControlSegment,
                           SUPPORTED_TRANSACTION_CODES,
                           UnsupportedTransactionException)
from typing import List


class X12MessageDelimiters:
    """
    Provides access to the delimiters used in a X12 Message
    """
    ISA_SEGMENT_LENGTH = 106
    ISA_ELEMENT_SEPARATOR = 3
    ISA_REPETITION_SEPARATOR = 82
    ISA_SEGMENT_TERMINATOR = 105

    def parse_isa_segment(self, x12_message: str):
        """
        Parses the ISA "control" segment and sets the delimiters used in the x12 message.
        :param x12_message: The x12 message/payload
        """
        isa_segment = x12_message[0:self.ISA_SEGMENT_LENGTH]

        if len(isa_segment) != self.ISA_SEGMENT_LENGTH:
            raise InvalidControlSegment(f'ISA Segment Length {len(isa_segment)} is not valid')

        self.element_separator = isa_segment[self.ISA_ELEMENT_SEPARATOR]
        self.repetition_separator = isa_segment[self.ISA_REPETITION_SEPARATOR]
        self.segment_terminator = isa_segment[self.ISA_SEGMENT_TERMINATOR]

    def __init__(self, x12_message: str):
        """
        Creates an instance of X12MessageDelimiters
        :param x12_message: the incoming x12 message
        """
        self.element_separator = None
        self.repetition_separator = None
        self.segment_terminator = None
        self.parse_isa_segment(x12_message)


class X12Reader:
    """
    Reads segments from a X12 Message Stream
    """
    def __init__(self, x12_message: str):
        x12_input = x12_message.replace('\n', '')
        self.x12_delimiters = X12MessageDelimiters(x12_input)
        self.x12_data = [s for s in x12_input.split(self.x12_delimiters.segment_terminator) if s != '']
        self.transaction_code = self.parse_transaction_code()

        if self.transaction_code not in SUPPORTED_TRANSACTION_CODES:
            raise UnsupportedTransactionException(f'transaction {self.transaction_code} is not supported')

    def parse_transaction_code(self) -> str:
        """
        Parses the X12 transaction code from the X12 message stream
        :return: the transaction code
        """
        transaction_segment = self.x12_data[2]
        segment_fields = transaction_segment.split(self.x12_delimiters.element_separator)
        return segment_fields[1]

    def read_segment(self) -> List:
        """
        :return: the tokens for the current X12 segment
        """
        for x12_segment in self.x12_data:
            yield x12_segment.split(self.x12_delimiters.element_separator)
