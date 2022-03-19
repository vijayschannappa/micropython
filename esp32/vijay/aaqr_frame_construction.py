from crc_calculation import crc_calculation
from initialization import *
import zero_padding

def password_generation(lsp):
    password_final = ''
    Password_Generation = lsp['PASSWD']
    for char in str(Password_Generation):
        password = hex(ord(char))
        password_final += password.replace('0x', '')
    hex_password = hex(
        int(len(password_final.replace(' ', '')) / 2)).replace('0x', '')
    length_password = zero_padding.zero_pad(hex_password, 2)
    return password_final, length_password


def frame_length_aarq_tag():
    length = hex((int(len(str(APPLICATION_CONTEXT_NAME + LENGTH_APPLICATION_CONTEXT_NAME + OBJECT_IDENTIFIER
                              + LENGTH_APPLICATION_CONTEXT_NAME_DEFAULT +
                              DEFAULT_COSEM_APPLICATION_CONTEXT_NAME
                              + IMPLICIT_ACSE_REQUIREMENT + LENGTH_UNUSED_BITS + NUMBER_UNUSED_BITS_IN_LAST_BYTES
                              + DATA_BYTE + IMPLICIT_MECHANISM_NAME + LENGTH_MECHANISM_NAME
                              + COSEM_MECHANISM_NAME_DEFAULT + MECHANISM_NAME_DEFAULT + LENGTH_PDU
                              + IMPLICIT_GRAPHICSTRING + LENGTH_PASSWORD + PASSWORD + AARQ_TAG_SECOND
                              + AARQ_TAG_SECOND_LENGTH + NUMBER_OCTET_STRING + AARQ_TAG_THIRD_LENGTH
                              + DLMS_INITIATE_REQUEST + DEDICATED_KEY + RESPONSE_ALLOWED + QUALITY_OF_SERVICE
                              + DLMS_VERSION_NUMBER + VERSION + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH
                              + NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST + CONFORMANCE_BLOCK
                              + MAX_RECEIVE_PDU_SIZE).replace(' ', '')) / 2))).replace('0x', '')
    aarq_tag_length = zero_padding.zero_pad(length, 2)
    return aarq_tag_length


def aarq_fourth_length():
    hex_string = hex((int(len(str(NUMBER_OF_UNUSED_BITS
                                  + INITIATE_REQUEST
                                  + CONFORMANCE_BLOCK).replace(' ', '')) / 2))).replace('0x', '')
    fourth_length = zero_padding.zero_pad(hex_string, 2)
    return fourth_length


def aarq_tag_third_length():
    hex_string = hex((int(len(str(DLMS_INITIATE_REQUEST + DEDICATED_KEY + RESPONSE_ALLOWED + QUALITY_OF_SERVICE
                                  + DLMS_VERSION_NUMBER + VERSION + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH
                                  + NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST + CONFORMANCE_BLOCK
                                  + MAX_RECEIVE_PDU_SIZE).replace(' ', '')) / 2))).replace('0x', '')
    third_length = zero_padding.zero_pad(hex_string, 2)
    return third_length


def aarq_tag_second_length():
    hex_string = hex((int(len(str(NUMBER_OCTET_STRING + AARQ_TAG_THIRD_LENGTH + DLMS_INITIATE_REQUEST + DEDICATED_KEY
                                  + RESPONSE_ALLOWED + QUALITY_OF_SERVICE + DLMS_VERSION_NUMBER + VERSION
                                  + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH +
                                  NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST
                                  + CONFORMANCE_BLOCK + MAX_RECEIVE_PDU_SIZE).replace(' ', '')) / 2))).replace('0x', '')

    third_length = zero_padding.zero_pad(hex_string, 2)
    return third_length


def length_of_pdu():
    length = hex(int(len(str(IMPLICIT_GRAPHICSTRING + LENGTH_PASSWORD
                             + PASSWORD).replace(' ', '')) / 2)).replace('0x', '')
    pdu_length = zero_padding.zero_pad(length, 2)
    return pdu_length


def frame_length():
    length = hex((int((len(str(FRAME_TYPE + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD + LLC + AARQ_TAG_FIRST
                               + FRAME_LENGTH_AARQ_TAG + APPLICATION_CONTEXT_NAME + LENGTH_APPLICATION_CONTEXT_NAME
                               + OBJECT_IDENTIFIER + LENGTH_APPLICATION_CONTEXT_NAME_DEFAULT
                               + DEFAULT_COSEM_APPLICATION_CONTEXT_NAME +
                               IMPLICIT_ACSE_REQUIREMENT + LENGTH_UNUSED_BITS
                               + NUMBER_UNUSED_BITS_IN_LAST_BYTES + DATA_BYTE + IMPLICIT_MECHANISM_NAME
                               + LENGTH_MECHANISM_NAME + COSEM_MECHANISM_NAME_DEFAULT + MECHANISM_NAME_DEFAULT
                               + LENGTH_PDU + IMPLICIT_GRAPHICSTRING +
                               LENGTH_PASSWORD + PASSWORD + AARQ_TAG_SECOND
                               + AARQ_TAG_SECOND_LENGTH + NUMBER_OCTET_STRING + AARQ_TAG_THIRD_LENGTH
                               + DLMS_INITIATE_REQUEST + DEDICATED_KEY + RESPONSE_ALLOWED + QUALITY_OF_SERVICE
                               + DLMS_VERSION_NUMBER + VERSION + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH
                               + NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST + CONFORMANCE_BLOCK
                               + MAX_RECEIVE_PDU_SIZE).replace(' ', '')) + 10) / 2))).replace('0x', '')
    aarq_frame_length = zero_padding.zero_pad(length, 2)
    return aarq_frame_length


def fsc_calculation_string():
    fsc = str(FRAME_TYPE + FRAME_LENGTH + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD + HCS + LLC
              + AARQ_TAG_FIRST + FRAME_LENGTH_AARQ_TAG +
              APPLICATION_CONTEXT_NAME + LENGTH_APPLICATION_CONTEXT_NAME
              + OBJECT_IDENTIFIER + LENGTH_APPLICATION_CONTEXT_NAME_DEFAULT +
              DEFAULT_COSEM_APPLICATION_CONTEXT_NAME
              + IMPLICIT_ACSE_REQUIREMENT + LENGTH_UNUSED_BITS +
              NUMBER_UNUSED_BITS_IN_LAST_BYTES + DATA_BYTE
              + IMPLICIT_MECHANISM_NAME + LENGTH_MECHANISM_NAME +
              COSEM_MECHANISM_NAME_DEFAULT + MECHANISM_NAME_DEFAULT
              + LENGTH_PDU + IMPLICIT_GRAPHICSTRING +
              LENGTH_PASSWORD + PASSWORD + AARQ_TAG_SECOND
              + AARQ_TAG_SECOND_LENGTH + NUMBER_OCTET_STRING +
              AARQ_TAG_THIRD_LENGTH + DLMS_INITIATE_REQUEST
              + DEDICATED_KEY + RESPONSE_ALLOWED +
              QUALITY_OF_SERVICE + DLMS_VERSION_NUMBER + VERSION
              + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH +
              NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST + CONFORMANCE_BLOCK
              + MAX_RECEIVE_PDU_SIZE).replace(' ', '')
    return fsc


def aarq_frame_generation(lsp):
    global PASSWORD,LENGTH_PASSWORD,LENGTH_PDU,FRAME_LENGTH_AARQ_TAG,FRAME_LENGTH,HCS,FSC
    PASSWORD = password_generation(lsp)[0]
    LENGTH_PASSWORD = password_generation(lsp)[1]
    LENGTH_PDU = length_of_pdu()
    FRAME_LENGTH_AARQ_TAG = frame_length_aarq_tag()
    FRAME_LENGTH = frame_length()
    HCS = crc_calculation(str(FRAME_TYPE + FRAME_LENGTH +
                          DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD))
    FSC = crc_calculation(fsc_calculation_string())
    aarq_frame = str(START_END_FLAG + FRAME_TYPE + FRAME_LENGTH + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD
                     + HCS + LLC + AARQ_TAG_FIRST + FRAME_LENGTH_AARQ_TAG + APPLICATION_CONTEXT_NAME
                     + LENGTH_APPLICATION_CONTEXT_NAME + OBJECT_IDENTIFIER +
                     LENGTH_APPLICATION_CONTEXT_NAME_DEFAULT
                     + DEFAULT_COSEM_APPLICATION_CONTEXT_NAME +
                     IMPLICIT_ACSE_REQUIREMENT + LENGTH_UNUSED_BITS
                     + NUMBER_UNUSED_BITS_IN_LAST_BYTES + DATA_BYTE +
                     IMPLICIT_MECHANISM_NAME + LENGTH_MECHANISM_NAME
                     + COSEM_MECHANISM_NAME_DEFAULT + MECHANISM_NAME_DEFAULT +
                     LENGTH_PDU + IMPLICIT_GRAPHICSTRING
                     + LENGTH_PASSWORD + PASSWORD + AARQ_TAG_SECOND +
                     AARQ_TAG_SECOND_LENGTH + NUMBER_OCTET_STRING
                     + AARQ_TAG_THIRD_LENGTH + DLMS_INITIATE_REQUEST + DEDICATED_KEY + RESPONSE_ALLOWED
                     + QUALITY_OF_SERVICE + DLMS_VERSION_NUMBER +
                     VERSION + PROPOSED_CONFORMANCE + AARQ_FOURTH_LENGTH
                     + NUMBER_OF_UNUSED_BITS + INITIATE_REQUEST +
                     CONFORMANCE_BLOCK + MAX_RECEIVE_PDU_SIZE + FSC
                     + START_END_FLAG).replace(' ', '')
    return aarq_frame





if __name__ == '__main__':
    aarq_frame_generation()
