# libreForms Specification

## Contents
1. [Summary](#summary)
2. [Definitions](#definitions)
3. [Principles](#principles)
    - [Flat data](#flat-data)
    - [Future-proof](#future-proof)
    - [Default values](#default-values)
4. [Form Fields](#form-fields)
    - [Input](#input)
    - [Output](#output)
    - [Field Configs](#field-configs)
5. [Form Configs](#form-configs)
6. [Reserved characters](#reserved-characters)
7. [Examples](#examples)
    - [Python dictionaries](#python-dictionaries)
    - [YAML](#yaml)

## Summary

This document describes the libreForms API, a declarative abstraction optimized for managing institutional forms over a network. At its core, the API divides each form into (a) form fields, which are further specified based on their input, output, and field configs; and (b) form configs, which further define form behavior. Form and field configs are generally denoted in their name using some [reserved character](#reserved-characters), like a leading underscore. Implementers have significant flexibility to arbitrarily define the behavior resulting from the above rules.

```
FORMS
|-> Form_A
|   |-> Form_Field_A
|   |   |-> Input_Specifications
|   |   |-> Output_Specifications
|   |   |-> _Field_Config
|   |-> Form_Field_B
|   |   |-> Input_Specifications
|   |   |-> Output_Specifications
|   |   |-> _Field_Config
|   |-> _Form_Config_A
|   |-> _Form_Config_B
|
|-> Form_B
    ...
```

The API is well-suited to a RESTful or distributed approach, where various clients might manage a different forms and employ different access controls, but store form data using a remote server accessed by API token. The use of reserved characters is especially useful in helping implementers build assumptions about the form data they will receive over the network: namely, that no data passed to the server that contains the reserved character in its name is form data, but instead can be treated as form metadata. This approach has the added benefit of decoupling the frontend form fields from the resultant backend data structures. 

![example RESTful architecture](assets/RESTful_libreForms_Architecture.drawio.svg)

The API works just as effectively in an all-in-one application where the submission and processing of form data occur within the same application context, espcially when administrators have a strong grasp of their form structure at the time of deployment. However, such situations seldom require the use of reserved characters to diffrentiate between form data and metadata, so the API design and its use of reserved characters may seem redundant in such environments.

![example single application architecture](assets/Single_App_libreForms_Architecture.drawio.svg)

## Definitions

This document extensively employs the key terminology defined below.  

#### Form configuration

This term is used to refer to configuration files containing form-building data, as shown in the [examples](#examples) below. Unfortunately, this term may appear confusing when used alongside terms like [form configs](#form-configs), which refer to specific configurations applied on a form-by-form basis and employ [reserved characters](#reserved-characters) to set themselves apart from [form fields](#form-fields).

#### Networked

This term is used, often alongside similar terms like 'distributed' or 'RESTful', to describe environments where form data is transferred over a network, for example using HTTP methods like `GET` and `POST`.

#### Declarative 

This term is used to describe a type of [form configuration](#form-configuration) that describes how forms should look and behave, without actually needing to write the logic that achieves that end state.

### Principles

The libreForms API is a generalization that allows organizations to define every aspect of their forms. Legacy tools for managing institutional form data, like hand-signed and PDF documents, are incompatible with the modern need to manage form data at scale without significantly increasing adminsitrative burden. Most browser-based form managers give form administrators little control over form fields, the resulting data, or the underlying web application. Proprietary solutions seldom provide self-hosting support, access to the source code, and a viable licensing model.

The libreForms API is written to prioritize customization, ease of use, and control. It uses a declarative approach to define forms and employs a relatively flat data structure to minimize the complexity, and maximize the readability, of form configurations. It leaves significant freedom to implementers to allow arbitrary form customization and tight control over the resultant form data, while encouraging implementers to make extensive use of default values to reduce boilerplate.

#### Flat data
This approach generally tries to avoid nesting data in an effort to reduce the complexity of the form configurations that it produces. It accomplishes this through a judicious use of reserved characters, typically the underscore. At the same time, its declarative approach helps avoid repetition. This simplicity and predictability may also have the added benefit of improving the human-readability of form configurations. 

#### Future-proof
The flexibility and abstractness of this approach goes a long way to making it future proof. However, there are some limits to this approach: first, form field inputs are rather tightly coupled with web-based forms; second, form field outputs are generally structured to conform to most relational and document databases; third, the use of reserved characters is most effective when data is being transferred over a network using approaches like REST, while it might not be as well-optimized for other environments.

#### Default values
This approach places a heavy emphasis on clearly-defined default behavior to serve as gap-fillers when form and field configs are left unspecified. This allows for predictable behavior and reduces boilerplate and general verbosity in the form configuration, but increases the work of implementers to robustly define default behavior for end users.

### Form Fields

These components define the structure of the form data generated from user input. Each form field should contain details about the input and output data, while optionally including more granular field config details.

#### Input 

This component defines how the form field will appear to the client. For example, on web-based implementations, this will provide details about the HTML field that it will generate, including the input type, its description, whether it's required, its default values, or a list of available options.

#### Output 

This component defines how the form data will be parsed by the server. For example, on web-based implementations, this will provide details on what type or structure the data should conform to and any conditions that the data should pass, like length or character requirements.

#### Field Configs

This component defines granular behavior for a given form field. For example, on web-based implementations, this could provide details on which user groups are able to see a form field, whether the visibility or available options should depend on the values of another form field, whether to visually group this field with other fields, and whether this form field should be used to trigger some other behavior in the underlying implementation.

### Form Configs

These components define form behavior at the client and application level, but are not generally made visible to users. For example, they might be used to define how form data can be visualized, what user groups or roles are able to submit forms or view others' submitted forms, or whether to route form submissions through an approval process.

### Reserved characters

As discussed above, this approach relies heavily upon the judicious use of reserved characters to denote aspects of the form that should not be made visible to end users but rather parsed in some other way. Typically, a leading underscore is used but can be replaced by implementers with a character better suited to their needs. This reserved character should be employed in form configs and field configs but never employed in form names or field names.

This approach allows implementers to build a few assumption into how they manage their forms. First, knowing that form field data will never contain the reserved character in the leading position allows the datastore to use that character for its own metadata, which may significantly overlap with or differ from the form and field configs. 

For example, let's say an implementer is employing a Document database to store form data. They want to store a nested metadata field, which they don't want to be treated like actual form data. They can add some arbitrary field containing additional metadata, maybe called `_metadata`, during form post-processing with the confidence that this will not collide with any form fields. This is especially useful when you do not know the structure of the form data you are managing at the time of implementation.

In addition, since form names should never contain the reserved character in the leading position, implementers can use this to retire forms submissions or mark them for deletion without removing them from the datastore entirely (`move COLLECTION.SUBMISSION_ID to _COLLECTION`), removing it from the forms that will be parsed by the system. 

Field names should never include the reserved character in the leading position to ensure they are not incorrectly parsed as configs.

### Examples

Here are some example forms implemented with different approaches, where configs are denoted using leading underscores. Note `Pass_Field` has a field-specific configs, which theoretically makes the field's appearance depend on a specific value in `Radio_Field`. Further, `Text_Field` includes a condition that the output data must be at least six characters long.

#### python dictionaries

```python
forms = {
    "sample-form": {
        "Text_Field": {
            "input_field": {"type": "text", "content": ["NA"], "required": False,},
            "output_data": {"type": "str", "validators": [lambda p: len(p) >= 6],},
            '_description': "this is a text field",
        },
        "Pass_Field": {
            "input_field": {"type": "password", "content": [""], "required": False,},
            "output_data": {"type": "str", "validators": [],},
            "_depends_on": ("Radio_Field", "Option"),
            '_description':  "this is a password field",
        },
        "Radio_Field": {
            "input_field": {"type": "radio", "content": ["Pick", "An", "Option"], "required": False,},
            "output_data": {"type": "str", "validators": [],},
            '_description': "this is a radio field",
        },
        "Select_Field": {
            "input_field": {"type": "select", "content": ["Pick", "An", "Option"], "required": False,},
            "output_data": {"type": "str", "validators": [],},
            '_description': "this is a select / dropdown field",
        },
        "Check_Field": {
            "input_field": {"type": "checkbox", "content": ["Pick", "An", "Option"], "required": False,},
            "output_data": {"type": "list", "validators": [],},
            '_description': "this is a checkbox field",
        },
        "Date_Field": {
            "input_field": {"type": "date", "content": [], "required": False,},
            "output_data": {"type": "str", "validators": [],},
            '_description': "this is a date field",
        },
        "Hidden_Field": {
            "input_field": {"type": "hidden", "content": ["This field is hidden"], "required": False,},
            "output_data": {"type": "str", "validators": [],},
            '_description': "this is a hidden field",
        },
        "Float_Field": {
            "input_field": {"type": "number", "content": [0], "required": False,},
            "output_data": {"type": "float", "validators": [],},
            '_description': "this is a float field"
        }, 
        "Int_Field": {
            "input_field": {"type": "number", "content": [0], "required": False,},
            "output_data": {"type": "int", "validators": [],},
            '_description': "this is an int field",
        }, 
        "File_Field": {
            "input_field": {"type": "file", "content": [None]}, 
            "output_data": {"type": 'string', "validators": [],},
            '_description': "this is a file upload field"
        },
        "_dashboard": {                 
            "type": "scatter",           
            "fields": {                  
                "x": "Timestamp", 
                "y": "Int_Field",       
                "color": "Text_Field"
            },
        },
        "_allow_repeat": False, 
        "_description": "This is an example form.", 
        "_allow_anonymous_access": False, 
        "_allow_uploads": True, 
        "_allow_csv_templates": True, 
        "_suppress_default_values": False, 
    },
}
```

#### YAML

```yaml
sample-form:
  Check_Field:
    input_field:
      content:
      - Pick
      - An
      - Option
      required: false
      type: checkbox
    output_data:
      type: list
    _description: this is a checkbox field
  Date_Field:
    input_field:
      content: 
      - ''
      required: false
      type: date
    output_data:
      type: str
    _description: this is a date field
  File_Field:
    input_field:
      content:
      - null
      type: file
    output_data:
      type: string
    _description: this is a file upload field
  Float_Field:
    input_field:
      content:
      - 0
      required: false
      type: number
    output_data:
      type: float
    _description: this is a float field
  Hidden_Field:
    input_field:
      content:
      - This field is hidden
      required: false
      type: hidden
    output_data:
      type: str
    _description: this is a hidden field
  Int_Field:
    input_field:
      content:
      - 0
      required: false
      type: number
    output_data:
      type: int
    _description: this is an int field
  Pass_Field:
    _depends_on:
      Radio_Field: Option
    _description: this is a password field
    input_field:
      content:
      - ''
      required: false
      type: password
    output_data:
      type: str
  Radio_Field:
    input_field:
      content:
      - Pick
      - An
      - Option
      required: false
      type: radio
    output_data:
      type: str
    _description: this is a radio field
  Select_Field:
    input_field:
      content:
      - Pick
      - An
      - Option
      required: false
      type: select
    output_data:
      type: str
    _description: this is a select / dropdown field
  Text_Field:
    input_field:
      content:
      - NA
      required: false
      type: text
    output_data:
      type: str
      validators:
      - min_length: 6
    _description: this is a text field
  _dashboard:
    fields:
      color: Text_Field
      x: Timestamp
      y: Int_Field
    type: scatter
  _allow_anonymous_access: false
  _allow_csv_templates: true
  _allow_repeat: false
  _allow_uploads: true
  _description: This is an example form.
  _suppress_default_values: false
```
