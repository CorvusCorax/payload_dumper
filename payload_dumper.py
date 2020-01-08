#!/usr/bin/env python
import struct
import hashlib
import bz2
import sys
import os
import argparse
import io
import subprocess

try:
    import lzma
except ImportError:
    from backports import lzma

from update_payload import update_metadata_pb2 as um
from update_payload import applier

class MyPayload(object):
    def __init__(self,payload_file,block_size,data_offset):
        self.payload_file = payload_file
        self.block_size = block_size
        self.data_offset = data_offset

    def ReadDataBlob(self, offset, length):
        self.payload_file.seek(self.data_offset + offset)
        return self.payload_file.read(length)

class MyApplier(applier.PayloadApplier):
    def __init__(self,payload):
        self.payload = payload
        self.block_size = self.payload.block_size
        self.minor_version = None
        self.bsdiff_in_place = None
        self.bspatch_path = "bsdiff/bspatch"
        self.puffpatch_path = "puffin/puffin"
        if not os.path.exists(self.bspatch_path):
            raise Exception("File not found: %s"%self.bspatch_path)
        if not os.path.exists(self.puffpatch_path):
            raise Exception("File not found: %s"%self.puffpatch_path)
        self.truncate_to_expected_size = True

def u32(x):
    return struct.unpack('>I', x)[0]

def u64(x):
    return struct.unpack('>Q', x)[0]



def dump_part(apobj,part):
    
    sys.stdout.write("Processing %s partition" % part.partition_name)
    sys.stdout.flush()

    out_file = open('%s/%s.img' % (args.out, part.partition_name), 'wb')
    h = hashlib.sha256()

    if args.diff:
        old_file = open('%s/%s.img' % (args.old, part.partition_name), 'rb')
    elif args.fakediff:
        try:
            old_file = open('%s/%s.img' % (args.old, part.partition_name), 'rb')
        except:
            old_file = False
    else:
        old_file = None

    try:
        apobj._ApplyOperations(part.operations, part.partition_name, old_file,
                              out_file, 999999999999999)
    finally:
        out_file.close()
        if not (old_file is None) and not (type(old_file) is bool):
            old_file.close()
        print("Done")


parser = argparse.ArgumentParser(description='OTA payload dumper')
parser.add_argument('payloadfile', type=argparse.FileType('rb'), 
                    help='payload file name')
parser.add_argument('--out', default='output',
                    help='output directory (defaul: output)')
parser.add_argument('--diff',action='store_true',
                    help='extract differential OTA, you need put original images to old dir')
parser.add_argument('--fakediff',action='store_true',
                    help='assume old files are all zeroes since we don\'t have them')
parser.add_argument('--old', default='old',
                    help='directory with original images for differential OTA (defaul: old)')
args = parser.parse_args()

magic = args.payloadfile.read(4)
assert magic == b'CrAU'

file_format_version = u64(args.payloadfile.read(8))
assert file_format_version == 2

manifest_size = u64(args.payloadfile.read(8))

metadata_signature_size = 0

if file_format_version > 1:
    metadata_signature_size = u32(args.payloadfile.read(4))

manifest = args.payloadfile.read(manifest_size)
metadata_signature = args.payloadfile.read(metadata_signature_size)

data_offset = args.payloadfile.tell()

dam = um.DeltaArchiveManifest()
dam.ParseFromString(manifest)
block_size = dam.block_size
plobj = MyPayload(args.payloadfile,block_size,data_offset)
apobj = MyApplier(plobj)

for part in dam.partitions:
    # for op in part.operations:
    #     assert op.type in (op.REPLACE, op.REPLACE_BZ, op.REPLACE_XZ), \
    #             'unsupported op'

    # extents = flatten([op.dst_extents for op in part.operations])
    # assert verify_contiguous(extents), 'operations do not span full image'

    dump_part(apobj,part)
