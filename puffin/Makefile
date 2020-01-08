# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

PUFFIN_SOURCES = \
	puffin.pb.cc \
	bit_reader.cc \
	bit_writer.cc \
	extent_stream.cc \
	file_stream.cc \
	huffer.cc \
	huffman_table.cc \
	memory_stream.cc \
	puffer.cc \
	puff_reader.cc \
	puff_writer.cc \
	puffin_stream.cc \
	puffdiff.cc \
	puffpatch.cc \
	main.cc \
	utils.cc

BSDIF_OBJECTFILES = \
	brotli_compressor.o \
	brotli_decompressor.o \
	bsdiff_arguments.o \
	bsdiff.o \
	bspatch.o \
	buffer_file.o \
	bz2_compressor.o \
	bz2_decompressor.o \
	compressor_buffer.o \
	decompressor_interface.o \
	diff_encoder.o \
	endsley_patch_writer.o \
	extents_file.o \
	extents.o \
	file.o \
	logging.o \
	memory_file.o \
	patch_reader.o \
	patch_writer_factory.o \
	patch_writer.o \
	sink_file.o \
	split_patch_writer.o \
	suffix_array_index.o \
	utils.o

OBJDIR = obj
SRCDIR = ../puffin_repo/src
BSDIFDIR = ../bsdiff
PUFFIN_OBJECTS += $(addprefix $(OBJDIR)/, $(PUFFIN_SOURCES:.cc=.o))
BSDIF_OBJECTS = $(addprefix $(BSDIFDIR)/, $(BSDIF_OBJECTFILES))

CXXFLAGS ?= -O3 -ggdb
INCLUDES += -Iorig_include -Iorig_include/bsdiff/include -Iorig_include/puffin/src/include
CXXFLAGS += $(INCLUDES) -Wall -fPIC -std=c++17
CPPFLAGS += $(INCLUDES)
LDLIBS = -lgflags -lglog -lprotobuf-lite -lpthread -lbrotlidec -lbrotlienc -lbz2 -ldivsufsort -ldivsufsort64

VPATH = $(SRCDIR)

all: puffin

$(OBJDIR):
	mkdir -p $@

protocompilation:
	protoc --proto_path=$(SRCDIR) $(SRCDIR)/puffin.proto --cpp_out $(SRCDIR)

$(PUFFIN_OBJECTS): | $(OBJDIR) protocompilation

$(BSDIF_OBJECTS):
	$(MAKE) -C $(BSDIFDIR)

puffin: $(PUFFIN_OBJECTS) $(BSDIF_OBJECTS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@ $(LDLIBS)

clean:
	rm -rf $(OBJDIR) puffin; \
	$(MAKE) -C $(BSDIFDIR) clean



$(OBJDIR)/%.o: %.cc
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

.PHONY: all clean test
