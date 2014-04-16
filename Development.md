# Tools to develop metaJSON

MetaJSON has now some dependencies to be developed, in particular to be tested. There are listed in a `requirements.txt`.

```
sudo easy_install pip
sudo pip install -r requirements.txt
```


## Run Tests

`nosetests` will all the tests at the root of repo.
`nosetests <filename>` run only this test file.
`nosetests -s` run tests with output
`nosetests ObjectiveCCodeGenerator_test:TestSampleTestClassCase.test_human_source_content` run only one single test
