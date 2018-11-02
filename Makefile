setup:
	gem install bundler jekyll
	cd blog && bundle install

run:
	cd blog && bundle exec jekyll serve