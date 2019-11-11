# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: thutech_protobuf/payload.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='thutech_protobuf/payload.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1ethutech_protobuf/payload.proto\"\xa0\x01\n\x12ProductInfoPayload\x12\n\n\x02Id\x18\x02 \x01(\t\x12\x0c\n\x04Name\x18\x03 \x01(\t\x12\x13\n\x0bProductCode\x18\x04 \x01(\t\x12\x32\n\nattributes\x18\x07 \x01(\x0b\x32\x1e.ProductInfoPayload.Attributes\x1a\'\n\nAttributes\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\tb\x06proto3')
)




_PRODUCTINFOPAYLOAD_ATTRIBUTES = _descriptor.Descriptor(
  name='Attributes',
  full_name='ProductInfoPayload.Attributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='ProductInfoPayload.Attributes.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url', full_name='ProductInfoPayload.Attributes.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=156,
  serialized_end=195,
)

_PRODUCTINFOPAYLOAD = _descriptor.Descriptor(
  name='ProductInfoPayload',
  full_name='ProductInfoPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Id', full_name='ProductInfoPayload.Id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Name', full_name='ProductInfoPayload.Name', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ProductCode', full_name='ProductInfoPayload.ProductCode', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attributes', full_name='ProductInfoPayload.attributes', index=3,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PRODUCTINFOPAYLOAD_ATTRIBUTES, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=195,
)

_PRODUCTINFOPAYLOAD_ATTRIBUTES.containing_type = _PRODUCTINFOPAYLOAD
_PRODUCTINFOPAYLOAD.fields_by_name['attributes'].message_type = _PRODUCTINFOPAYLOAD_ATTRIBUTES
DESCRIPTOR.message_types_by_name['ProductInfoPayload'] = _PRODUCTINFOPAYLOAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProductInfoPayload = _reflection.GeneratedProtocolMessageType('ProductInfoPayload', (_message.Message,), dict(

  Attributes = _reflection.GeneratedProtocolMessageType('Attributes', (_message.Message,), dict(
    DESCRIPTOR = _PRODUCTINFOPAYLOAD_ATTRIBUTES,
    __module__ = 'thutech_protobuf.payload_pb2'
    # @@protoc_insertion_point(class_scope:ProductInfoPayload.Attributes)
    ))
  ,
  DESCRIPTOR = _PRODUCTINFOPAYLOAD,
  __module__ = 'thutech_protobuf.payload_pb2'
  # @@protoc_insertion_point(class_scope:ProductInfoPayload)
  ))
_sym_db.RegisterMessage(ProductInfoPayload)
_sym_db.RegisterMessage(ProductInfoPayload.Attributes)


# @@protoc_insertion_point(module_scope)