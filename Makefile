GEMFURY_AUTH_TOKEN := ${GEMFURY_AUTH_TOKEN}

# distribution details
VERSION := $(shell awk '$$1 == "__version__" {print $$NF}' ./quartic_sdk/_version.py)
OS := none
CPU_ARCH = any

help:
	@echo "QuarticSDK Help:\n"\
	"clean:  Remove all cache and wheel packages.\n"\
	"build:  Build QuarticSDK wheel package via setup.py.\n"\
	"version:  Show current QuarticSDK version.\n"\
	"publish:  Upload the package in dist directory that matches current QuarticSDK version.\n"\
	" VERSION Specify another version to upload (If there is one available). "

clean-dist:
	rm -r ./dist 2>/dev/null || true

clean-cache:
	rm -r *.egg-info || true
	python setup.py clean --all || true

clean: clean-dist clean-cache

test:
	 pytest -s && aloe

build: clean
	python setup.py sdist bdist_wheel

version:
	@echo $(VERSION)

publish: override VERSION := $(if $(VERSION),$(VERSION),)
publish: WHEEL_FILENAME := quartic_sdk-$(VERSION)-py3-$(OS)-$(CPU_ARCH).whl
publish:
	curl -F package=@dist/$(WHEEL_FILENAME) https://$(GEMFURY_AUTH_TOKEN)@push.fury.io/quartic-ai/
