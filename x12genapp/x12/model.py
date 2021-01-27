from dataclasses import (dataclass,
                         field)


@dataclass(unsafe_hash=True)
class X12Demographics:
    trace_number: str = field(default=None, compare=False)
    last_name: str = field(default=None, compare=True)
    first_name: str = field(default=None, compare=True)
    middle_name: str = field(default=None, compare=True)
    suffix: str = field(default=None, compare=False)
    identification_code_type: str = field(default=None, compare=False)
    identification_code: str = field(default=None, compare=False)
    group_number: str = field(default=None, compare=False)
    address_line_1: str = field(default=None, compare=False)
    address_line_2: str = field(default=None, compare=False)
    city: str = field(default=None, compare=False)
    state: str = field(default=None, compare=False)
    zip_code: str = field(default=None, compare=False)
    birth_date: str = field(default=None, compare=True)
    gender: str = field(default=None, compare=False)
    provenance_id: int = field(default=None, compare=False)
