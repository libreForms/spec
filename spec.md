# libreForms Specification

This document describes the libreForms API, a declarative form-manager abstraction layer that links frontend form fields and their corresponding backend data structures, both of which can be written in a language of the implementer's choice. 

At it's core, libreForms divides each form into fields, which are further defined based on their input and output, and configs, which are generally denoted in their name using some marker like leading underscores (see example below). Beyond these concepts, the implementer has significant flexibility to arbitrarily define the behavior of these components.

```
FORMS
|-> Form_A
|   |-> Field_A
|   |   |-> Input Specifications
|   |   |-> Output Specifications
|   |-> Field_B
|   |   |-> Input Specifications
|   |   |-> Output Specifications
|   |-> _Config_A
|   |-> _Config_B
|
|-> Form_B
...

```

### Principles

The libreForms API allows organizations to define every aspect of a form in a relatively straightforward manner. Legacy tools for managing institutional form data, like hand-signed and PDF documents, are incompatible with an institutional need to manage form data without significantly increasing adminsitrative burden. Likewise, ,most browser-based form managers give form administrators little control over form fields, the resulting data, or the underlying web application. Proprietary solutions seldom provide both self-hosting support and a viable licensing model.

With these problems in mind, the libreForms API is written to prioritize customization, ease of use, and control. It uses a declarative approach to define forms, and employs a relatively flat data structure to minimize the complexity of form configurations. It leaves significant freedom to implementers to allow arbitrary form customization and tight control over the resultant form data.

### Fields

These components correspond to the data that an end-user will submit along with the form.

### Configs

These components correspond to the metadata used to define behind-the-scenes form behavior.

### Example

Here is an example form implemented using python dictionaries, where configs are denoted using leading underscores.

```python
forms = {
    "sample-form": {
        "Text_Field": {
            "input_field": {"type": "text", "content": ["NA"]},
            "output_data": {"type": "str", "required": False, "validators": [lambda p: len(p) >= 6], 'description': "this is a text field"},
        },
        "Pass_Field": {
            "input_field": {"type": "password", "content": [""]},
            "output_data": {"type": "str", "required": False, "validators": [], 'description': "this is a password field"},
        },
        "Radio_Field": {
            "input_field": {"type": "radio", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "str", "required": False, "validators": [], 'description': "this is a radio field"},
        },
        "Select_Field": {
            "input_field": {"type": "select", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "str", "required": False, "validators": [], 'description': "this is a select / dropdown field"},
        },
        "Check_Field": {
            "input_field": {"type": "checkbox", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "list", "required": False, "validators": [], 'description': "this is a checkbox field"},
        },
        "Date_Field": {
            "input_field": {"type": "date", "content": []},
            "output_data": {"type": "str", "required": False, "validators": [], 'description': "this is a date field"},
        },
        "Hidden_Field": {
            "input_field": {"type": "hidden", "content": ["This field is hidden"]},
            "output_data": {"type": "str", "required": False, "validators": [], 'description': "this is a hidden field"},
        },
        "Float_Field": {
            "input_field": {"type": "number", "content": [0]},
            "output_data": {"type": "float", "required": False, "validators": [], 'description': "this is a float field"},
        }, 
        "Int_Field": {
            "input_field": {"type": "number", "content": [0]},
            "output_data": {"type": "int", "required": False, "validators": [], 'description': "this is an int field"},
        }, 
        "File_Field": {
            "input_field": {"type": "file", "content": [None]}, 
            "output_data": {"type": 'string', "validators": []},
        },
        "_dashboard": {                 
            "type": "scatter",           
            "fields": {                  
                "x": "Timestamp", 
                "y": "Int_Field",       
                "color": "Text_Field"
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