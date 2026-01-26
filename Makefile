HERE=$(shell pwd)
all: deploy

deploy: package
	rm -f dangerousbot.zip	
	cd package; zip -r ../dangerousbot.zip *
	#aws s3 cp lambda_ebooks.zip s3://blah/blah/blah

package: serpapi mastodon *.py local_settings.py
	mkdir -p package
	cp -R mastodon/* ./package/
	cp -R python-twitter/* ./package/
	cp noun-10K.txt ./package/
	cp dangerousbot.py ./package/
	cp serpapi_image_search.py ./package/
	cp dangerous_generator.py ./package/
	cp local_settings.py ./package/
	cp dangerous.png ./package/
	cp Emulogic.ttf ./package/

serpapi:
	rm -rf serpapi
	mkdir -p serpapi
	echo '[install]' > ./serpapi/setup.cfg
	echo 'prefix=' >> ./serpapi/setup.cfg
	cd $(HERE)/serpapi ; pip3 install serpapi -t $(HERE)/mastodon

mastodon:
	rm -rf mastodon
	mkdir -p mastodon
	echo '[install]' > ./mastodon/setup.cfg
	echo 'prefix=' >> ./mastodon/setup.cfg
	cd $(HERE)/mastodon ; pip3 install mastodon.py -t $(HERE)/mastodon

clean:
	rm -rf package

distclean: clean
	rm -rf mastodon

