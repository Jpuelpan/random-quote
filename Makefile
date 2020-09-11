build:
	pipenv lock -r | pip install --target ./build -r /dev/stdin
	cp -r ./app.py ./build
	cp -r ./Inria_Serif ./build
	cp -r ./jpuelpan.github.io/quotes/quotes.json ./build

clean:
	rm -rf ./build

package:
	cp -r ./app.py ./build
	cp -r ./Inria_Serif ./build
	cp -r ./jpuelpan.github.io/quotes/quotes.json ./build
	aws cloudformation package \
		--template ./cloudformation.yml \
		--s3-bucket cf-templates-1c5ezxk7c7rv6-us-west-2 \
		--output-template packaged.yml \
		--region us-west-2

deploy:
	aws cloudformation deploy \
		--template-file packaged.yml \
		--stack-name QuotesImageService \
		--capabilities CAPABILITY_IAM \
		--region us-west-2

.PHONY: build clean package deploy

