puffin/puffin:
	$(MAKE) -C puffin/ puffin

puffin: puffin/puffin


all: puffin

clean:
	$(MAKE) -C puffin/ clean
