all:
	yarnpkg
	cp node_modules/bootstrap/dist/css/bootstrap.min.css reporting/static/css/.
	cp node_modules/bootstrap/dist/css/bootstrap.min.css.map reporting/static/css/.
	cp node_modules/bootstrap/dist/js/bootstrap.min.js reporting/static/js/.
	cp node_modules/bootstrap/dist/js/bootstrap.min.js.map reporting/static/js/.
	rm -rf node_modules/