import antlr4
from antlr4 import *
from JavaScriptLexer import JavaScriptLexer
from JavaScriptParser import JavaScriptParser

class TypeScriptTransCompiler:
    def __init__(self):
        self.type_check_functions = {}
        self.control_checks = None

    @staticmethod
    def generate_js_code(type_check_functions, control_checks, variables_info):
        result = ""
        # Aggiunta delle funzioni di controllo
        for type_name, check_func in type_check_functions.items():
            result += f"function {check_func}(value) {{\n"
            result += f"if (typeof value !== '{type_name}') {{\n"
            result += f"throw new TypeError('Expected {type_name}, got ' + typeof value);\n"
            result += "}\n"
            result += f"return value;\n"
            result += "};\n\n"

        # Aggiunta dei controlli di tipo per le variabili
        for variable_info in variables_info:
            var_name, var_type, var_control_check = variable_info
            if var_control_check is not None:
                result += f"{var_name} = {var_control_check}({var_name});\n"

        # Aggiunta dei controlli di tipo per le variabili inizializzate
        for var_name, var_type, var_control_check in control_checks.items():
            result += f"{var_name} = {var_control_check}({var_name});\n"

        return result

    def parse_file(self, file_path):
        with open(file_path) as f:
            input_stream = antlr4.InputStream(f.read())

        lexer = JavaScriptLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JavaScriptParser(stream)
        tree = parser.program()

        visitor = PrintVisitor(
            type_check_functions=self.type_check_functions, control_checks=self.control_checks)
        visitor.visit(tree)

        # Aggiungi controlli in output per tutte le variabili del file
        variables_info = []
        for variable in visitor.variables:
            var_name = variable[0]
            var_type = variable[1]
            var_control_check = variable[2]
            variables_info.append((var_name, var_type, var_control_check))

        return (visitor.result, self.type_check_functions, self.control_checks, variables_info)



class ControlChecks:
    @staticmethod
    def checkString(value):
        if isinstance(value, str):
            return value
        else:
            raise TypeError("Expected string, got %s" % type(value).__name__)

    @staticmethod
    def checkNumber(value):
        if isinstance(value, (int, float)):
            return value
        else:
            raise TypeError("Expected number, got %s" % type(value).__name__)

    @staticmethod
    def checkObject(value):
        if isinstance(value, dict):
            return value
        else:
            raise TypeError("Expected object, got %s" % type(value).__name__)

class PrintVisitor(JavaScriptParser.JavaScriptParserVisitor):
    def __init__(self, type_check_functions, control_checks):
        self.result = ""
        self.type_check_functions = type_check_functions
        self.control_checks = control_checks
        self.variables = []

    def visitFunctionDeclaration(self, ctx: JavaScriptParser.FunctionDeclarationContext):
        result = "function " + ctx.getChild(1).getText() + "("

        params = []
        for param in ctx.formalParameterList().formalParameter():
            name = self.visit(param.getChild(0))
            param_type = param.getChild(1)
            if param_type is not None:
                type_name = param_type.getText()
                param_type_check = f"check{type_name.capitalize()}"
                if type_name not in self.type_check_functions:
                    self.type_check_functions[type_name] = param_type_check
                params.append(f"{name}: {type_name}")
                self.variables.append((name, type_name.lower(), param_type_check))
            else:
                params.append(name)
                self.variables.append((name, "any", None))

        result += ", ".join(params) + ") {\n"
        result += self.visit(ctx.functionBody())
        result += "}\n"
        return result

    def visitVariableDeclaration(self, ctx: JavaScriptParser.VariableDeclarationContext):
        result = self.visit(ctx.getChild(0)) + " "
        declarations = []
        for declaration in ctx.variableDeclarationList().variableDeclaration():
            name = self.visit(declaration.getChild(0))
            # Controllo del tipo della variabile assegnata
            initializer = self.visit(declaration.getChild(2))
            if initializer is not None:
                # Controllo sui tipi della variabile assegnata
                type_name = type(initializer).__name__
                if type_name not in self.type_check_functions:
                    self.type_check_functions[type_name] = f"check{type_name.capitalize()}"

                if self.control_checks is not None and name in self.control_checks:
                    check_func = self.control_checks[name]
                    initializer = f"{check_func}({initializer})"
                # Controllo sul tipo della variabile dichiarata
                for variable in self.variables:
                    if variable[0] == name:
                        check_func = variable[2]
                        if check_func is not None:
                            initializer = f"{check_func}({initializer})"
                declarations.append(f"{name}: {type_name} = {initializer}")
                var_type = type_name.lower() if type_name != "NoneType" else "any"
                self.variables.append((name, var_type, check_func))
                # Aggiunta del controllo di tipo
                result += f"{name} = {self.type_check_functions[var_type]}({name});\n"
            else:
                declarations.append(name)
                self.variables.append((name, "any", None))
        result += ", ".join(declarations) + ";"
        return result
    
    def visitBinaryExpression(self, ctx: JavaScriptParser.BinaryExpressionContext):
        left = self.visit(ctx.getChild(0))
        operator = self.visit(ctx.getChild(1))
        right = self.visit(ctx.getChild(2))

        left_type = type(left).__name__
        right_type = type(right).__name__

        if left_type != right_type:
            raise TypeError(f"Cannot apply operator '{operator}' to types '{left_type}' and '{right_type}'")

        if left_type not in self.type_check_functions:
            self.type_check_functions[left_type] = f"check{left_type.capitalize()}"

        return f"{self.type_check_functions[left_type]}({left}) {operator} {self.type_check_functions[right_type]}({right})"


if __name__ == '__main__':
    t = TypeScriptTransCompiler()
    checks = ControlChecks()
    t.control_checks = checks
    result, type_check_functions, control_checks, variables_info = t.parse_file("test.ts")
    js_result = TypeScriptTransCompiler.generate_js_code(type_check_functions, control_checks, variables_info) + result
    print(js_result)
