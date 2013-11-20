#Currently known issues

###Predefined primitive type

A definition like below which might be referenced as sub or base type is not yet supported by the java code generator. Using that will result in valid Objective-C code but will lead to invalid code for Java. It can be used but manual "reparation" of the generated code is required.

```
{
    "name" : "titleString",
    "base-type" : "string",
    "description" : "the title of product",
    "minLength" : 10,
    "maxLength" : 20,
    "regex" : "[a-z0-9]:10",
    "required" : 1
}
```

###Documentation Topic 4
java code generator doesn't support "subType" for "date" type yet.

###Documentation Topic 12
The complete topic 12 is not yet fully supported and/or tested. Some parts might already work but there is no intentionally support implemented yet.

We highly appreciate any contribution to this work-in-progress project.