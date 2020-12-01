import collections

X12DemographicFields = [
    'is_subscriber'
    'trace_number'
    'last_name',
    'first_name',
    'middle_name',
    'suffix',
    'identification_code_type',
    'identification_code',
    'group_number',
    'address_line_1',
    'address_line_2',
    'city',
    'state',
    'zip_code',
    'birth_date'
]

X12Demographics = collections.namedtuple('X12Demographics', X12DemographicFields)
