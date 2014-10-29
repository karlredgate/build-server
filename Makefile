
PWD := $(shell pwd)
PACKAGE = build-server
SERVER := lookout-micro

default: rpm

push: rpm
	scp rpm/RPMS/noarch/*$(PACKAGE)*.rpm $(SERVER):
	ssh $(SERVER) 'sudo yum update -y *$(PACKAGE)*.rpm'
	ssh $(SERVER) 'rm -f *$(PACKAGE)*.rpm'

repo: rpm
	rm -rf repo
	mkdir -p repo/Packages
	cp rpm/RPMS/*/*.rpm repo/Packages
	createrepo --quiet --unique-md-filenames repo

rpm: build
	rm -rf rpm
	mkdir -p rpm/BUILD rpm/RPMS rpm/BUILDROOT
	rpmbuild --quiet -bb --buildroot=$(PWD)/rpm/BUILDROOT $(PACKAGE).spec

build:
	@echo Nothing to build yet

clean:
	$(RM) -rf $(CLEANS)
	$(RM) -rf rpm exports repo

distclean: clean

