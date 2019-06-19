import yaml

document = """
  a: 1
  b:
    c: 3
    d: 4
"""

def Handler():
    print("HEllo World")
    return yaml.dump(yaml.load(document), default_flow_style=None)
