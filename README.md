# MetaJSON

metaJSON provides a meta language to generate object models for several languages. The generated classes can easily be used for the client-server communication.

## Usage

1. Write your JSON scheme according to the JSON spec of your backend (for yaml, please see details below)
2. Run the script

```
# python readJSON.py -h

readJSON.py [ -p | -t | -o | -s ] [-i]
Options:
  -h, --help            shows help
  -p, --prefix=        project prefix (default: S2M)
  -s, --suffix=        classname suffix (default: JSONObject). Use "-s false" for no suffix
  -t, --target=        target platform iOS or Android (default: iOS)
  -i, --input=         meta-JSON file to read
  -o, --output=      ouput path of generated source codes
```

A working sample call could look like that:
```
# python readJSON.py --p GitHub -t Android -i github-scheme.json -o com/example/project/android/json
```
The result of that call will be generated Java code in the folder "com". The java package structure and definition will be there, so you just need to copy the folder in your project structure. It is ready to be used.

<!--
## Yaml

if you prefer to use yaml as a description language, you will need to install the converter via npm:

```
npm install -g yamljs
```

#### Converting YAML to JSON

Example:

```
yaml2json --pretty --indentation 6 test.yaml > test.json
```

#### Converting JSON to YAML

Example:

```
json2yaml -d 5 test.json > test.yaml
```
-->

## Documentation

See MetaJSONProtocol.md file in the doc folder.

## Known issues
Please check the issue tracker and/or refer to the known_issues.md file in the doc folder.

## License
The project is published with the MIT License. Please read the LICENSE.txt for more details.