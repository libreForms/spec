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