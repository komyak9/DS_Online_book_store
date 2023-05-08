# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: book_store.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x62ook_store.proto\"H\n\x18\x43reateLocalStoresRequest\x12\x18\n\x10processes_number\x18\x01 \x01(\x05\x12\x12\n\nip_address\x18\x02 \x01(\t\"g\n\x19\x43reateLocalStoresResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\tclient_id\x18\x03 \x01(\t\x12\x15\n\rprocesses_ids\x18\x04 \x03(\t\"\'\n\x12\x43reateChainRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"\xdf\x02\n\x13\x43reateChainResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12J\n\x14processes_sucs_preds\x18\x03 \x03(\x0b\x32,.CreateChainResponse.ProcessesSucsPredsEntry\x12I\n\x13processes_addresses\x18\x04 \x03(\x0b\x32,.CreateChainResponse.ProcessesAddressesEntry\x12\x19\n\x11head_node_address\x18\x05 \x01(\t\x1a\x39\n\x17ProcessesSucsPredsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x39\n\x17ProcessesAddressesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"&\n\x11\x43heckChainRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"\xd4\x02\n\x12\x43heckChainResponse\x12\x18\n\x10is_chain_created\x18\x01 \x01(\x08\x12I\n\x14processes_sucs_preds\x18\x02 \x03(\x0b\x32+.CheckChainResponse.ProcessesSucsPredsEntry\x12H\n\x13processes_addresses\x18\x03 \x03(\x0b\x32+.CheckChainResponse.ProcessesAddressesEntry\x12\x19\n\x11head_node_address\x18\x04 \x01(\t\x1a\x39\n\x17ProcessesSucsPredsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x39\n\x17ProcessesAddressesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x12\n\x10ListChainRequest\"$\n\x11ListChainResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"-\n\x18ReadFromDataStoreRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\"=\n\x19ReadFromDataStoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"@\n\x17WriteToDataStoreRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\x12\x12\n\nbook_price\x18\x02 \x01(\x02\"<\n\x18WriteToDataStoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"D\n\x1b\x43ommonWriteOperationRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\x12\x12\n\nbook_price\x18\x02 \x01(\x02\"@\n\x1c\x43ommonWriteOperationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x12\n\x10ListBooksRequest\"5\n\x11ListBooksResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x84\x02\n\tBookStore\x12L\n\x11\x43reateLocalStores\x12\x19.CreateLocalStoresRequest\x1a\x1a.CreateLocalStoresResponse\"\x00\x12:\n\x0b\x43reateChain\x12\x13.CreateChainRequest\x1a\x14.CreateChainResponse\"\x00\x12\x37\n\nCheckChain\x12\x12.CheckChainRequest\x1a\x13.CheckChainResponse\"\x00\x12\x34\n\tListChain\x12\x11.ListChainRequest\x1a\x12.ListChainResponse\"\x00\x32\xb3\x02\n\x0b\x44\x61taStorage\x12L\n\x11ReadFromDataStore\x12\x19.ReadFromDataStoreRequest\x1a\x1a.ReadFromDataStoreResponse\"\x00\x12I\n\x10WriteToDataStore\x12\x18.WriteToDataStoreRequest\x1a\x19.WriteToDataStoreResponse\"\x00\x12U\n\x14\x43ommonWriteOperation\x12\x1c.CommonWriteOperationRequest\x1a\x1d.CommonWriteOperationResponse\"\x00\x12\x34\n\tListBooks\x12\x11.ListBooksRequest\x1a\x12.ListBooksResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'book_store_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATECHAINRESPONSE_PROCESSESSUCSPREDSENTRY._options = None
  _CREATECHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_options = b'8\001'
  _CREATECHAINRESPONSE_PROCESSESADDRESSESENTRY._options = None
  _CREATECHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_options = b'8\001'
  _CHECKCHAINRESPONSE_PROCESSESSUCSPREDSENTRY._options = None
  _CHECKCHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_options = b'8\001'
  _CHECKCHAINRESPONSE_PROCESSESADDRESSESENTRY._options = None
  _CHECKCHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_options = b'8\001'
  _REMOVEHEADRESPONSE_PROCESSESSUCSPREDSENTRY._options = None
  _REMOVEHEADRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_options = b'8\001'
  _REMOVEHEADRESPONSE_PROCESSESADDRESSESENTRY._options = None
  _REMOVEHEADRESPONSE_PROCESSESADDRESSESENTRY._serialized_options = b'8\001'
  _CREATELOCALSTORESREQUEST._serialized_start=20
  _CREATELOCALSTORESREQUEST._serialized_end=92
  _CREATELOCALSTORESRESPONSE._serialized_start=94
  _CREATELOCALSTORESRESPONSE._serialized_end=197
  _CREATECHAINREQUEST._serialized_start=199
  _CREATECHAINREQUEST._serialized_end=238
  _CREATECHAINRESPONSE._serialized_start=241
  _CREATECHAINRESPONSE._serialized_end=592
  _CREATECHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_start=476
  _CREATECHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_end=533
  _CREATECHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_start=535
  _CREATECHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_end=592
  _CHECKCHAINREQUEST._serialized_start=594
  _CHECKCHAINREQUEST._serialized_end=632
  _CHECKCHAINRESPONSE._serialized_start=635
  _CHECKCHAINRESPONSE._serialized_end=975
  _CHECKCHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_start=476
  _CHECKCHAINRESPONSE_PROCESSESSUCSPREDSENTRY._serialized_end=533
  _CHECKCHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_start=535
  _CHECKCHAINRESPONSE_PROCESSESADDRESSESENTRY._serialized_end=592
  _LISTCHAINREQUEST._serialized_start=977
  _LISTCHAINREQUEST._serialized_end=995
  _LISTCHAINRESPONSE._serialized_start=997
  _LISTCHAINRESPONSE._serialized_end=1033
  _READFROMDATASTOREREQUEST._serialized_start=1035
  _READFROMDATASTOREREQUEST._serialized_end=1080
  _READFROMDATASTORERESPONSE._serialized_start=1082
  _READFROMDATASTORERESPONSE._serialized_end=1143
  _WRITETODATASTOREREQUEST._serialized_start=1145
  _WRITETODATASTOREREQUEST._serialized_end=1209
  _WRITETODATASTORERESPONSE._serialized_start=1211
  _WRITETODATASTORERESPONSE._serialized_end=1271
  _COMMONWRITEOPERATIONREQUEST._serialized_start=1273
  _COMMONWRITEOPERATIONREQUEST._serialized_end=1341
  _COMMONWRITEOPERATIONRESPONSE._serialized_start=1343
  _COMMONWRITEOPERATIONRESPONSE._serialized_end=1407
  _LISTBOOKSREQUEST._serialized_start=1409
  _LISTBOOKSREQUEST._serialized_end=1427
  _LISTBOOKSRESPONSE._serialized_start=1429
  _LISTBOOKSRESPONSE._serialized_end=1482
  _BOOKSTORE._serialized_start=1485
  _BOOKSTORE._serialized_end=1745
  _DATASTORAGE._serialized_start=1748
  _DATASTORAGE._serialized_end=2055
# @@protoc_insertion_point(module_scope)
