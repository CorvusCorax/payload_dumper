puffin/puffin:
	$(MAKE) -C puffin/ puffin

puffin: puffin/puffin


all: puffin
