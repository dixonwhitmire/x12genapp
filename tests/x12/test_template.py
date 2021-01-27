from x12genapp.x12.template import (get_271_existing_member,
                                    get_271_member_not_found)
from typing import Dict


def test_get_271_existing_member(x12_270_fields: Dict,
                                 x12_271_member_with_coverage_message):
    actual_result = get_271_existing_member(x12_270_fields)
    assert x12_271_member_with_coverage_message == actual_result


def test_get_271_member_not_found(x12_270_fields: Dict,
                                  x12_271_member_not_found_message):
    actual_result = get_271_member_not_found(x12_270_fields)
    assert x12_271_member_not_found_message == actual_result
