# Test guidelines

## Unit tests 
Unit tests are all contained within automated_unit_tests folder. 
All unit tests can be run in one go with:

`python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/`

It is recommded that you use the arguments: 

`--show-capture=no`

`--disable-pytest-warnings`

to clean up the output, but it is not necessary. 

### Dependencies

`python -m pip install pytest`

`python -m pip install mock`


### Test coverage
To get a coverage report, you will need to install the coverage module:

`python -m pip install coverage`

docs here: https://coverage.readthedocs.io/en/7.2.7/

Run the tests with coverage: 

`coverage run -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/`

The `.coveragerc` file configures the source folder to look in, and any files that should be excluded. 

- Note that the specified source is `src/` - this tells coverage where it needs to look.
- Note that screens, widgets, and popups are currently excluded.

To generate a report:

`coverage html`

Which you can view using your browser at: 

`\<path\>/htmlcov/index.html`

All in one line: 

`coverage run -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/ && coverage html && open htmlcov/index.html`