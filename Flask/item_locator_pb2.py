# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: item_locator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12item_locator.proto\x12\x0bitemlocator\"\x17\n\x07Request\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x14\n\x05Reply\x12\x0b\n\x03res\x18\x01 \x01(\t2G\n\x0bItemLocator\x12\x38\n\nSearchItem\x12\x14.itemlocator.Request\x1a\x12.itemlocator.Reply\"\x00\x62\x06proto3')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_REPLY = DESCRIPTOR.message_types_by_name['Reply']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'item_locator_pb2'
  # @@protoc_insertion_point(class_scope:itemlocator.Request)
  })
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'item_locator_pb2'
  # @@protoc_insertion_point(class_scope:itemlocator.Reply)
  })
_sym_db.RegisterMessage(Reply)

_ITEMLOCATOR = DESCRIPTOR.services_by_name['ItemLocator']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=35
  _REQUEST._serialized_end=58
  _REPLY._serialized_start=60
  _REPLY._serialized_end=80
  _ITEMLOCATOR._serialized_start=82
  _ITEMLOCATOR._serialized_end=153
# @@protoc_insertion_point(module_scope)
