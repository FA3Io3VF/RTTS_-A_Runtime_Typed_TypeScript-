"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import antlr4
from JavaScriptLexer import JavaScriptLexer
from JavaScriptParser import JavaScriptParser

class JavaScriptTypeChecker(JavaScriptParserVisitor):
    def __init__(self):
        self.variables = {}
        self.type_checkers = {
            "number": self.check_number,
            "string": self.check_string,
            "boolean": self.check_boolean,
            "array": self.check_array,
            "object": self.check_object
        }
    
    def check_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
          
    """TODO: scrivere altri metodi di verifica per gli altri tipi"""
    
    def check_string(self, value):
        return isinstance(value, str)
    
    def check_boolean(self, value):
        return isinstance(value, bool)
    
 

    def enterVariableDeclaration(self, ctx):
        if ctx.getChild(0).getText() == "let":
            var_name = ctx.getChild(1).getText()
            comment = self.get_comment(ctx.start.line)
            if comment is not None and comment.startswith("@type"):
                type_name = comment[5:].strip()
                type_checker = self.type_checkers.get(type_name)
                if type_checker is not None:
                    self.variables[var_name] = type_checker
                    #Aggiungiamo il controllo di tipo all'assegnamento
                    assignment = ctx.getChild(2).getChild(0)
                    new_assignment = antlr4.CommonToken(JavaScriptLexer.Identifier, var_name)
                    new_code = self.build_type_check_code(var_name, assignment.getText(), type_name)
                    new_assignment.text = f"{new_assignment.text} = {new_code};"
                    assignment.parentCtx.removeLastChild()
                    assignment.parentCtx.addChild(new_assignment)
    
    def build_type_check_code(self, var_name, value, type_name):
        type_checker = self.type_checkers.get(type_name)
        if type_checker is not None:
            return f"self.check_type('{var_name}', {value}, '{type_name}')"
        else:
            return value
    
    def check_type(self, var_name, value, type_name):
        type_checker = self.type_checkers.get(type_name)
        if type_checker is not None and not type_checker(value):
            raise TypeError(f"Variable {var_name} should be of type {type_name}")
        return value
      
""" HOW TO USE """

type_checker = JavaScriptTypeChecker()

from antlr4 import InputStream, CommonTokenStream
from JavaScriptLexer import JavaScriptLexer
from JavaScriptParser import JavaScriptParser

javascript_code = """ My incredible Code Here """

input_stream = InputStream(javascript_code)
lexer = JavaScriptLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = JavaScriptParser(stream)

tree = parser.program()
type_checker.visit(tree)


"""

Example:

let x = 10; // @type number
let y = "hello"; // @type string
let z = true; // @type boolean

"""
