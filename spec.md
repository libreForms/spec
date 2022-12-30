# libreForms Specification

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

### Form Fields

These components correspond to the data that an end-user will submit along with the form. Each form field should contain details about the input and output data, while optionally containing further field configuration details.

#### Input 

This component defines how the form field will appear to the client. For example, on web-based implementations, this will provide details about the HTML field that it will generate, including the input type, its description, whether its required, its default values, or a list of available options.

#### Output 

This component defines how the form data will be parsed by the server. For example, on web-based implementations, this will provide details on what type or structure the data should conform to and any conditions that the data should pass, like length or character requirements.

#### Field Configs

This component defines granular behavior for a given form field. For example, For example, on web-based implementations, this will provide details on whether only users with a certain role assignment be able to see a form field, whether the visibility or available options should depend on the values of another form field, or whether this form field should be used to trigger some other behavior in the underling implementation.

### Form Configs

These components correspond to the metadata used to define behind-the-scenes form behavior. For example, they might be used to define how form data can be visualized, what user groups or roles are able to submit forms or view others' submitted forms, and whether to route form submissions through an approval process.

### Example

Here is an example form implemented using python dictionaries, where configs are denoted using leading underscores. Note `Pass_Field` has a field-specific configuration, which theoretically makes the field's appearance depend on a specific value in `Radio_Field`.

```python
forms = {
    "sample-form": {
        "Text_Field": {
            "input_field": {"type": "text", "content": ["NA"]},
            "output_data": {"type": "str", "required": False, "validators": [lambda p: len(p) >= 6], '_description': "this is a text field"},
        },
        "Pass_Field": {
            "input_field": {"type": "password", "content": [""]},
            "output_data": {"type": "str", "required": False, "validators": [], '_description': "this is a password field"},
            "_depends_on": ("Radio_Field", "Option"),
        },
        "Radio_Field": {
            "input_field": {"type": "radio", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "str", "required": False, "validators": [], '_description': "this is a radio field"},
        },
        "Select_Field": {
            "input_field": {"type": "select", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "str", "required": False, "validators": [], '_description': "this is a select / dropdown field"},
        },
        "Check_Field": {
            "input_field": {"type": "checkbox", "content": ["Pick", "An", "Option"]},
            "output_data": {"type": "list", "required": False, "validators": [], '_description': "this is a checkbox field"},
        },
        "Date_Field": {
            "input_field": {"type": "date", "content": []},
            "output_data": {"type": "str", "required": False, "validators": [], '_description': "this is a date field"},
        },
        "Hidden_Field": {
            "input_field": {"type": "hidden", "content": ["This field is hidden"]},
            "output_data": {"type": "str", "required": False, "validators": [], '_description': "this is a hidden field"},
        },
        "Float_Field": {
            "input_field": {"type": "number", "content": [0]},
            "output_data": {"type": "float", "required": False, "validators": [], '_description': "this is a float field"},
        }, 
        "Int_Field": {
            "input_field": {"type": "number", "content": [0]},
            "output_data": {"type": "int", "required": False, "validators": [], '_description': "this is an int field"},
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