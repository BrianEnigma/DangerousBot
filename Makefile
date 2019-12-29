HERE=$(shell pwd)
all: deploy

deploy: package
	rm -f dangerousbot.zip	
	cd package; zip -r ../dangerousbot.zip *
	#aws s3 cp lambda_ebooks.zip s3://blah/blah/blah

package: python-twitter mastodon *.py local_settings.py
	mkdir -p package
	cp -R mastodon/* ./package/
	cp -R python-twitter/* ./package/
	cp noun-10K.txt ./package/
	cp dangerousbot.py ./package/
	cp bing_image_search.py ./package/
	cp dangerous_generator.py ./package/
	cp local_settings.py ./package/
	cp dangerous.png ./package/
	cp Emulogic.ttf ./package/

python-twitter:
	rm -rf python-twitter
	mkdir -p python-twitter
	echo '[install]' > ./python-twitter/setup.cfg
	echo 'prefix=' >> ./python-twitter/setup.cfg
	cd $(HERE)/python-twitter ; pip3 install python-twitter -t $(HERE)/python-twitter

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

