# MetaJSON

metaJSON provides a meta language to generate object models for several languages. The generated classes can easily be used for the client-server communication.

## Usage

1. Write your [JSON scheme](https://github.com/sinnerschrader-mobile/metaJSON/wiki/Protocol) according to the JSON spec of your backend
2. Run the script

```
# metajson -h
Options:
  -v, --version         shows version
  -h, --help            shows help
  -p, --prefix=         project prefix (default: S2M)
  -s, --suffix=         classname suffix (default: JSONObject). Use "-s false" for no suffix
  -i, --input=          meta-JSON file to read
  -o, --output=         ouput path of generated source codes (default: src)
      --template=       template directory to use to generate code
      --package=        name of the generated package (default: none)
```

A working sample call could look like that:
```
# metajson --p GitHub -i github-scheme.json -o com/example/project/android/json --template=metajson/templates/Android --package=com.example.project.android.json
```
The result of that call will be generated Java code in the folder "com". The java package structure and definition will be there, so you just need to copy the folder in your project structure. It is ready to be used.

## Documentation

See [Wiki](https://github.com/sinnerschrader-mobile/metaJSON/wiki)

## License
The project is published with the MIT License. Please read the LICENSE.txt for more details.
