# payload dumper

## System requirement

- Python2, pip
- google protobuf for python `pip install protobuf`

## Guide

- clone repository recusrively
- use toplevel makefile to build bsdiff and puffdiff dependencies
- use payload_dumper.py to extract payload.bin from differential update
- checksums supplied in payload.bin are tested but not enforced (mismatches are printed to screen)

## Parameters

- diff -- apply differential update - abort if diff fails to apply
- fakediff -- apply differential update but ignore failing diffs and fill missing parts with 0xEF - extracts some useful information from payload without having original image

## TODO
- not yet tested with full updates

