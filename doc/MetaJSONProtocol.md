# Writing Meta JSON and Using Meta JSON

##1. define a type (common)

```
{
"name" : string,
"base-type" : string or array,
"description" : string,
}
```
* "name" and "base-type" are mandatory meta-data for all types.
* "description" is optional to understand what this property means.
* the value of "base-type" should be "boolean", "number", "string", "data", "date", "array", "object", "any" or a name of custom base-type.

##2. define string type

```
{
"name" : "myString",
"base-type" : "string",
"description" : string,
"regex" : regular expression string,
"maxLength" : positive integer or zero,
"minLength" : positive integer or zero
}
```
	
* "regex", "maxLength" and "minLength" are optional, to validate this type.
* "maxLength" should be always same or bigger than "minLength".
	
You can also use just one of those ("minLength" or "maxLength").


##3. define number type
	
```
{
	"name" : "myNumber",
	"base-type" : "number",
	"description" : string,
	"maxValue" : real number,
	"minValue" : real number
}
```
	
* "minValue" and "maxValue" are optional, to validate this type.
* "maxValue" should be always same or bigger than "minValue".
	
You can also use just one of those ("minValue" or "maxValue").


##4. define date type

```
{
	"name" : "myDate",
	"base-type" : "date",
	"description" : string
	"minValue" : UTC time interval since 1970
	"maxValue" : UTC time interval since 1970
}
```
	
* The value of myDate should be always UTC time interval since 1970.
* "minValue" and "maxValue" are optional, to validate this type.
* "maxValue" should be always same or later than "minValue".
	
You can also use just one of those ("minValue" or "maxValue").


##5. define boolean type

```
{
	"name" : "myBoolean",
	"base-type" : "boolean",
	"description" : string
}
```
	
##6. define data type

```
{
	"name" : "myData",
	"base-type" : "data",
	"description" : string,
	"maxLength" : positive integer or zero,
	"minLength" : positive integer or zero
}
```
	
* "maxLength" and "minLength" are optional, to validate this type.
* "maxLength" should be always same or bigger than "minLength".


##7. define array type

```
{
	"name" : "myArray",
	"base-type" : "array",
	"description" : string,
	"subType" : string,
	"maxCount" : positive integer or zero,
	"minCount" : positive integer or zero
}
```
	
* "maxCount" and "minCount" are optional, to validate this type.
* "maxCount" should be always same or bigger than "minCount".
* "subType" should be boolean, number, string, data, date, array, object and any or a name of custom base-type.


##8. define custom type
	
```
{
	"name" : "myCustom",
	"base-type" : "object",
	"description" : "description-value",
	"property" : [
		{
			"name" : "property1"
			"base-type" : "string",
			"required" : "boolean",
		},
		{
			"name" : "property2"
			"base-type" : "number",
			"required" : "boolean",
		},
			.
			.
			.
	]
}
```
	
To define custom type, you should write "property" (mandatory).
Property can have many different kind of types (boolean, number, string, data, date, array, object, any and/or custom object)
but "property" must have 1 or more types.


##9. define child type from custom type
	
```
{
	"name" : "myChild",
	"base-type" : "myCustom",
	"description" : string,
	"property" : [
		{
			"name" : "property3"
			"base-type" : "myString",
			"required" : boolean,
		},
			.
			.
			.
	]
}
```
	
If you want to define child type from other custom type, you just need to write parent type's name in "base-type" field.
And you can also define other additional properties, or override existing properties.
In this case, "property" is not mandatory.


##10. define multi-type

```
{
	"name" : "myMultiType",
	"base-type" : ["string", "number", "typeA", …],
	"required" : boolean,
	"description" : string
}
```	
	
And when the base-type is json-array type, code generator has to implement method which is looked like

```
	(JSONObject *)myMultiType;
	(JSONString *)myMultiTypeAsString;
	(JSONNumber *)myMultiTypeAsNumber;
	(TypeA *)myMultiTypeAsTypeA;
			.
			.
			.
```
	
And if subType is "any", the code generator will make just a method which will return the original JSON subtree (ex : Objective-c method can return any basic JSON type).
	
```
	(JSONObject *) myMultiType;
```

##11. define multi-type array type
	
```
{
	"name" : "mtArray",
	"base-type" : "array",
	"description" : string,
	"sub-type" : ["string", "number", "typeB", …],
}
```
	
Code generator has to implement method which is looked like
	
```
	(JSONObject *)mtArrayObjectIndexAt:(NSUInteger)index;
	(JSONString *)mtArrayObjectAsStringIndexAt:(NSUInteger)index;
	(JSONNumber *)myArrayObjectAsNumberIndexAt:(NSUInteger)index;
	(TypeB *)mtArrayObjectAsTypeBIndexAt:(NSUInteger)index;
			.
			.
			.
```
	
And if subType is "any", the code generator will make just a method which will return the original JSON subtree (ex : Objective-c method can return any basic JSON type).
	
```
	(JSONObject *)mtArrayObjectIndexAt:(NSUInteger)index;
```


##12. several ways to define type and use

Top-level Meta-JSON is an array where each element is one of "string", "array", "number", "boolean", ..., "object" and child type of custom type.
	
###12.1. basic definition and usage
	
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20
	},
	{
		"name" : "sessionExpirationDate",
		"base-type" : "date",
		"description" : "Expire date of session",
		"maxValue" : 183759284
	},
	{
		"name" : "mySession",
		"base-type" : "object",
		"description" : "session has session id and session expire date.",
		"property" : 
		[
			{
				"name" : "sessionID",
				"base-type" : "sessionString",
				"required" : 1
			},
			{
				"name" : "expirationDate",
				"base-type" : "sessionExpirationDate",
				"required" : 1
			}
		]
	},
	{
		"name" : "user",
		"base-type" : "object",
		"description" : "test description of user type.",
		"property" :
		[
			{
				"name" : "session",
				"base-type" : "mySession",
				"required" : 1
			},
			{
				"name" : "userName",
				"base-type" : "string",
				"required" : 1
			}
		]
	}
]
```
	
###12.2. define type in "base-type"
* the type named "person" is always accessible and reusable in other types.
* in this case, "user" type is a child type from "person" type.
	   
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20
	},
	{
		"name" : "sessionExpirationDate",
		"base-type" : "date",
		"description" : "Expire date of session",
		"maxValue" : 183759284
	},
	{
		"name" : "mySession",
		"base-type" : "object",
		"description" : "session has session id and session expire date.",
		"property" : 
		[
			{
				"name" : "sessionID",
				"base-type" : "sessionString",
				"required" : 1
			},
			{
				"name" : "expirationDate",
				"base-type" : "sessionExpirationDate",
				"required" : 1
			}
		]
	},
	{
		"name" : "user",
		"base-type" :
		{
			"name" : "person",
			"base-type" : "object",
			"description" : ".",
			"property" : 
			[
				{
					"name" : "email",
					"base-type" : "string",
					"required" : 1
				},
				{
					"name" : "birthday",
					"base-type" : "date",
					"required" : 1
				}
			]
		},
		"description" : "test description of user type.",
		"property" : 
		[
			{
				"name" : "userName",
				"base-type" : "string",
				"required" : 1
			},
			{
				"name" : "userSession",
				"base-type" : "mySession",
				"required" : 1
			}
		]
	}
]
```
			
###12.3. define type in "property"
	
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20,
	},
	{
		"name" : "sessionExpirationDate",
		"base-type" : "date",
		"description" : "Expire date of session"
		"maxValue" : 183759284
	},
	{
		"name" : "user",
		"base-type" : "object",
		"description" : "test description of user type.",
		"property" :
		[
			{
				"name" : "session"
				"base-type" : {
					"name" : "mySession",
					"base-type" : "object",
					"description" : "session has session id and session expire date.",
					"property" : 
					[
						{
							"name" : "sessionID"
							"base-type" : "sessionString",
							"required" : 1,
						},
						{
							"name" : "expirationDate"
							"base-type" : "sessionExpirationDate",
							"required" : 1,
						}
					]
				},
				"required" : 1,
			},
			{
				"name" : "userName"
				"base-type" : "string",
				"required" : 1,
			}
		]
	}
]
```
	
###12.4. define type in "subType" of array
* "userSession" property can have "sessionID" type and "expirationDate".
* (it's not a good example……)
	
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20,
	},
	{
		"name" : "sessionExpirationDate",
		"base-type" : "date",
		"description" : "Expire date of session"
		"maxValue" : 183759284
	},
	{
		"name" : "mySession",
		"base-type" : "array",
		"description" : "session has session-ids and session expire dates.",
		"subType" : 
		[
			{
				"name" : "sessionID"
				"base-type" : "string",
				"description" : "session string after login",
				"maxLength" : 50,
				"minLength" : 20,
			},
			{
				"name" : "expirationDate",
				"base-type" : "date",
				"description" : "Expire date of session"
				"maxValue" : 183759284
			}
		]
	},
	{
		"name" : "user",
		"base-type" : "object",
		"description" : "test description of user type.",
		"property" : 
		[
			{
				"name" : "userName"
				"base-type" : "string",
				"required" : 1,
			},
			{
				"name" : "userSession"
				"base-type" : "mySession",
				"required" : 1,
			}
		]
	}
]
```
	
###12.5. override the value of predefined keys in predefine type.
* I just overrides the maxLength value of "sessionString".
	
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20,
	},
	{
		"name" : "mySession",
		"base-type" : "object",
		"description" : "session has session id and session expire date.",
		"property" : 
		[
			{
				"name" : "sessionID",
				"base-type" : "sessionString",
				"description" : "session string after login",
				"maxLength" : 30,
			},
			{
				"name" : "expirationDate"
				"base-type" : "sessionExpirationDate",
				"required" : 1,
			}
		]
	},
	{
		"name" : "user",
		"base-type" : "object",
		"description" : "test description of user type.",
		"property" : 
		[
			{
				"name" : "session"
				"base-type" : "mySession",
				"required" : 1,
			},
			{
				"name" : "userName"
				"base-type" : "string",
				"required" : 1,
			}
		]
	}
]
```
	
###12.6. override the properties of predefined types.
- user type is a child type of person.
- redefine the property named "email" with new "regex" key.
	
```
[
	{
		"name" : "sessionString",
		"base-type" : "string",
		"description" : "session string after login",
		"maxLength" : 50,
		"minLength" : 20,
	},
	{
		"name" : "sessionExpirationDate",
		"base-type" : "date",
		"description" : "Expire date of session"
		"maxValue" : 183759284
	},
	{
		"name" : "mySession",
		"base-type" : "object",
		"description" : "session has session id and session expire date.",
		"property" : 
		[
			{
				"name" : "sessionID"
				"base-type" : "sessionString",
				"required" : 1,
			},
			{
				"name" : "expirationDate"
				"base-type" : "sessionExpirationDate",
				"required" : 1,
			}
		]
	},
	{
		"name" : "person",
		"base-type" : "object",
		"description" : ".",
		"property" : 
		[
			{
				"name" : "email"
				"base-type" : "string",
				"required" : 1,
			},
			{
				"name" : "birthday"
				"base-type" : "date",
				"required" : 1,
			}
		]
	},
	{
		"name" : "user",
		"base-type" : "person"
		"description" : "test description of user type.",
		"property" : 
		[
			{
				"name" : "email"
				"base-type" : "string",
				"regex" : "[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}"
				"required" : 1,
			},
	
			{
				"name" : "session"
				"base-type" : "mySession",
				"required" : 1,
			},
			{
				"name" : "userName"
				"base-type" : "string",
				"required" : 1,
			}
		]
	}
]
```
	
	
