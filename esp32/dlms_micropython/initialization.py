Start_Time_Path = '/home/pi/DATA/Start_Time/'

PASS_WORD = 'ABCD0001'

MAC_ADDRESS = "00010"

START_END_FLAG = '7E'
FRAME_TYPE = 'A0'
# FRAME_LENGTH = '40'  # need to calculate except start and end flag

DESTINATION_ADDRESS = '03'
SOURCE_ADDRESS = '41'  # 41'
MODE = '93'  # for SNMR calculation
CONTROL_FIELD = '10'  # frame type I frame
LLC = 'E6 E6 00'
AARQ_TAG_FIRST = '60'  # Implicit sequence

# FRAME_LENGTH_AARQ_TAG = '32'  # Frame_Length_from_AARQ_tag Need to calculate

APPLICATION_CONTEXT_NAME = 'A1'
LENGTH_APPLICATION_CONTEXT_NAME = '09'  # need to calculate
OBJECT_IDENTIFIER = '06'
LENGTH_APPLICATION_CONTEXT_NAME_DEFAULT = '07'
DEFAULT_COSEM_APPLICATION_CONTEXT_NAME = '60 85 74 05 08 01 01'
IMPLICIT_ACSE_REQUIREMENT = '8A'
LENGTH_UNUSED_BITS = '02'
NUMBER_UNUSED_BITS_IN_LAST_BYTES = '07'
DATA_BYTE = '80'  # data byte(bit0 in MSB, Bit0=1 -> Authentional functional unit requested
IMPLICIT_MECHANISM_NAME = '8B'  # Implicit Mechanism name=object identifier
LENGTH_MECHANISM_NAME = '07'

COSEM_MECHANISM_NAME_DEFAULT = '60 85 74 05 08 02 01'  # last 01 for low security 02 for high security  # Default
# COSEM -Mechanism Name-first octet
MECHANISM_NAME_DEFAULT = 'AC'  # Default COSEM -Mechanism Name-first octet::=choice
# LENGTH_PDU = '06'  # from here length of frame
IMPLICIT_GRAPHICSTRING = '80'

# LENGTH_PASSWORD = '04'  # need to calculate 08

PASSWORD = ''  # '6C 6E 74 31'

AARQ_TAG_SECOND = 'BE'  # Implicit application association(user information)

AARQ_TAG_SECOND_LENGTH = '10'

NUMBER_OCTET_STRING = '04'

AARQ_TAG_THIRD_LENGTH = '0E'

DLMS_INITIATE_REQUEST = '01'  # DLMS initiate request([1] implicit sequence)
DEDICATED_KEY = '00'  # optional
RESPONSE_ALLOWED = '00'
QUALITY_OF_SERVICE = '00'
DLMS_VERSION_NUMBER = '06'
VERSION = '5F'  # Unsigned8 -version
PROPOSED_CONFORMANCE = '1F'  # Proposed conformance-Implicit bit string

AARQ_FOURTH_LENGTH = '04'  # need to calculate

NUMBER_OF_UNUSED_BITS = '00'
INITIATE_REQUEST = '00'
CONFORMANCE_BLOCK = '1E 1D'  # '10 14'  # 1D 1E'  # Conformance Block(LN) - (Read,Write,Action)Multiple references

MAX_RECEIVE_PDU_SIZE = 'FF FF'

CONTROL_FIELD_FRAME = '32'  # frame type I frame

# LLC = 'E6 E6 00'
READ_REQUEST = 'C0'  # Implicit sequence
REQUEST_NUMBER = '01'
INVOKE_ID = 'C1'  # 81
OBIS_CLASS = '00'

ATTRIBUTE_1 = '02'
ATTRIBUTE_2 = '00'

MODE_DISCONNECTION = '53'

STARTING_FRAME = "A04C0341765B02E6E600C001C100"
LOAD_PROFILE_IP = "070100630100FF"

THIRD_FRAME = "0201010204020412000809060000010000FF0F02120000090C"
START_END_SEPARATOR = "FF"
FIRST_FRAME_LENGTH = "FFFEB600090C"
SECOND_FRAME_LENGTH = "FFFEB6000100"

Load_Profile_IP_1 = "7EA0190341323ABDE6E600C001C100070100630100FF01003CA37E"
Load_Profile_IP_2 = "7EA0190341540ABBE6E600C001C100070100630100FF05005CC47E"


Disconnect = "7EA00703415356A27E"
