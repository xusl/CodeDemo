from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

data = """
$.ajax({
    type: "POST",
    url: 'http://www.example.com',
    data: {
        email: 'abc@g.com',
        phone: '9999999999',
        name: 'XYZ'
    }
});
"""

parser = Parser()
tree = parser.parse(data)
fields = {getattr(node.left, 'value', ''): getattr(node.right, 'value', '')
          for node in nodevisitor.visit(tree)
          if isinstance(node, ast.Assign)}

print fields
