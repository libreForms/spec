# libreForms Specification

## Contents
1. [Summary](#summary)
2. [Principles](#principles)
    - [Flat data](#flat-data)
    - [Future-proof](#future-proof)
    - [Strong defaults](#strong-defaults)
3. [Form Fields](#principles)
    - [Input](#input)
    - [Output](#output)
    - [Field Configs](#field-configs)
4. [Form Configs](#principles)
5. [Reserved characters](#reserved-characters)
6. [Example](#example)
    - [Python dictionaries](#python-dictionaries)
    - [YAML](#yaml)

## Summary

This document describes the libreForms API, a declarative form-manager abstraction linking frontend form fields with their corresponding backend data structures, both of which can be written in a language of the implementer's choice. 

At it's core, libreForms divides each form into (a) form fields, which are further specified based on their input, output, and field configs; and (b) form configs, which further define form behavior. Form and field configs are generally denoted in their name using some marker like leading underscores (see example below). Implementers have significant flexibility to arbitrarily define the behavior resulting from the above rules.

```
FORMS
|-> Form_A
|   |-> Form_Field_A
|   |   |-> Input_Specifications
|   |   |-> Output_Specifications
|   |   |-> Field_Config
|   |-> Form_Field_B
|   |   |-> Input_Specifications
|   |   |-> Output_Specifications
|   |   |-> Field_Config
|   |-> _Form_Config_A
|   |-> _Form_Config_B
|
|-> Form_B
    ...
```

### Principles

The libreForms API allows organizations to simply define every aspect of a form. Legacy tools for managing institutional form data, like hand-signed and PDF documents, are incompatible with the need to manage form data at scale without significantly increasing adminsitrative burden. Most browser-based form managers give form administrators little control over form fields, the resulting data, or the underlying web application. Proprietary solutions seldom provide both self-hosting support and a viable licensing model.

With these problems in mind, the libreForms API is written to prioritize customization, ease of use, and control. It uses a declarative approach to define forms, and employs a relatively flat data structure to minimize the complexity of form configurations. It leaves significant freedom to implementers to allow arbitrary form customization and tight control over the resultant form data. 


#### Flat data
This approach generally tries to avoid nesting data in an effort to reduce the complexity of the form templates that it produces. It accomplishes this through a judicious use of reserved characters, typically the underscore. At the same time, its declarative approach helps avoid repetition.

#### Future-proof
The flexibility of this approach goes a long way to generally making it future proof, with some exceptions. Form field inputs are rather tightly coupled with web-based forms. Further, form field outputs are generally structured to conform to most relational and document databases.

#### Strong defaults
This approach places a heavy emphasis on clearly-defined default behavior to serve as gap-fillers when form and field configs are left unspecified. This allows for predictable behavior and reduces the business of the form template, but increases the work of implementers to robustly define default behaviors.

### Form Fields

These components correspond to the data that an end-user will submit along with the form. Each form field should contain details about the input and output data, while optionally containing further field configuration details.

#### Input 

This component defines how the form field will appear to the client. For example, on web-based implementations, this will provide details about the HTML field that it will generate, including the input type, its description, whether its required, its default values, or a list of available options.

#### Output 

This component defines how the form data will be parsed by the server. For example, on web-based implementations, this will provide details on what type or structure the data should conform to and any conditions that the data should pass, like length or character requirements.

#### Field Configs

This component defines granular behavior for a given form field. For example, For example, on web-based implementations, this will provide details on whether only users with a certain role assignment be able to see a form field, whether the visibility or available options should depend on the values of another form field, whether to visually group this field with other fields, whether this form field should be used to trigger some other behavior in the underling implementation.

### Form Configs

These components correspond to the metadata used to define behind-the-scenes form behavior. For example, they might be used to define how form data can be visualized, what user groups or roles are able to submit forms or view others' submitted forms, and whether to route form submissions through an approval process.

### Reserved characters
As discussed above, this approach relies heavily upon the judicious use of reserved characters to denote aspects of the form that should not be made visible to end users but rather parsed in some other way. Typically, a leading undescore is used but can be replaced by implementers with a character better suited to their needs. This reserved character should be employed in form configs and field configs but never employed in form names or field names.

This approach allows implementers to build a few assumption into how they manage their forms. First, knowing that form field data will never contain the reserved character in the leading position allows the datastore to use that character for its own metadata, which may significantly overlap with or differ from the form and field configs. 

For example, let's say an implementer is employing a Document database to store form data. They want to store a nested metadata field, which they don't want to be treated like actual form data. They can add a field called `_metadata` during form post-processing with the confidence that this will not collide with any form fields. This is especially useful when you do not know the structure of the form data you are managing at the time of implementation.

In addition, since form names should never contained the reserved character in the leading position, implementers can use this to retire forms submissions or mark them for deletion without removing them from the datatore entirely (`move COLLECTION.SUBMISSION_ID to _COLLECTION`), removing it from the forms that will be parsed by the system. 

Field names should never include the reserved character in the leading position to ensure they are not incorrectly parsed as configs.

### Examples

Here are some example forms implemented with different approaches, where configs are denoted using leading underscores. Note `Pass_Field` has a field-specific configuration, which theoretically makes the field's appearance depend on a specific value in `Radio_Field`. Further, `Text_Field` includes a condition that the output data must be at least six characters long.

#### python dictionaries

```python
forms = {
    "sample-form": {
        "Text_Field": {
            "input_field": {"type": "text", "content": ["NA"], "required": False, '_description': "this is a text field"},
            "output_data": {"type": "str", "validators": [lambda p: len(p) >= 6],},
        },
        "Pass_Field": {
            "input_field": {"type": "password", "content": [""], "required": False, '_description': "this is a password field"},
            "output_data": {"type": "str", "validators": [],},
            "_depends_on": ("Radio_Field", "Option"),
        },
        "Radio_Field": {
            "input_field": {"type": "radio", "content": ["Pick", "An", "Option"], "required": False, '_description': "this is a radio field"},
            "output_data": {"type": "str", "validators": [],},
        },
        "Select_Field": {
            "input_field": {"type": "select", "content": ["Pick", "An", "Option"], "required": False, '_description': "this is a select / dropdown field"},
            "output_data": {"type": "str", "validators": [],},
        },
        "Check_Field": {
            "input_field": {"type": "checkbox", "content": ["Pick", "An", "Option"], "required": False, '_description': "this is a checkbox field"},
            "output_data": {"type": "list", "validators": [],},
        },
        "Date_Field": {
            "input_field": {"type": "date", "content": [], "required": False, '_description': "this is a date field"},
            "output_data": {"type": "str", "validators": [],},
        },
        "Hidden_Field": {
            "input_field": {"type": "hidden", "content": ["This field is hidden"], "required": False, '_description': "this is a hidden field"},
            "output_data": {"type": "str", "validators": [],},
        },
        "Float_Field": {
            "input_field": {"type": "number", "content": [0], "required": False,  '_description': "this is a float field"},
            "output_data": {"type": "float", "validators": [],}
        }, 
        "Int_Field": {
            "input_field": {"type": "number", "content": [0], "required": False, '_description': "this is an int field"},
            "output_data": {"type": "int", "validators": [],},
        }, 
        "File_Field": {
            "input_field": {"type": "file", "content": [None]}, 
            "output_data": {"type": 'string', "validators": [],},
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
      _description: this is a checkbox field
      content:
      - Pick
      - An
      - Option
      required: false
      type: checkbox
    output_data:
      type: list
      validators: []
  Date_Field:
    input_field:
      _description: this is a date field
      content: []
      required: false
      type: date
    output_data:
      type: str
      validators: []
  File_Field:
    input_field:
      content:
      - null
      type: file
    output_data:
      type: string
      validators: []
  Float_Field:
    input_field:
      _description: this is a float field
      content:
      - 0
      required: false
      type: number
    output_data:
      type: float
      validators: []
  Hidden_Field:
    input_field:
      _description: this is a hidden field
      content:
      - This field is hidden
      required: false
      type: hidden
    output_data:
      type: str
      validators: []
  Int_Field:
    input_field:
      _description: this is an int field
      content:
      - 0
      required: false
      type: number
    output_data:
      type: int
      validators: []
  Pass_Field:
    _depends_on: !!python/tuple
    - Radio_Field
    - Option
    input_field:
      _description: this is a password field
      content:
      - ''
      required: false
      type: password
    output_data:
      type: str
      validators: []
  Radio_Field:
    input_field:
      _description: this is a radio field
      content:
      - Pick
      - An
      - Option
      required: false
      type: radio
    output_data:
      type: str
      validators: []
  Select_Field:
    input_field:
      _description: this is a select / dropdown field
      content:
      - Pick
      - An
      - Option
      required: false
      type: select
    output_data:
      type: str
      validators: []
  Text_Field:
    input_field:
      _description: this is a text field
      content:
      - NA
      required: false
      type: text
    output_data:
      type: str
      validators:
      - min_length: 6
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
