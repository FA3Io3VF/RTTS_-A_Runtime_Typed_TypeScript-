"""
This file is part of FullSeq.

FullSeq is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of the License.

FullSeq is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import subprocess
import antlr4
from JavaScriptLexer import JavaScriptLexer
from JavaScriptParser import JavaScriptParser
from JavaScriptTypeChecker import JavaScriptTypeChecker

class PrintVisitor(JavaScriptParser.JavaScriptParserVisitor):
    def __init__(self, output_file):
        self.output_file = output_file
        self.result = ""

    def visitProgram(self, ctx:JavaScriptParser.ProgramContext):
        for child in ctx.children:
            self.result += self.visit(child)

    def visitStatement(self, ctx:JavaScriptParser.StatementContext):
        result = self.visit(ctx.getChild(0))
        if result is not None:
            self.result += result + "\n"
        return ""

    def visitFunctionDeclaration(self, ctx:JavaScriptParser.FunctionDeclarationContext):
        result = self.visit(ctx.getChild(0)) + "("
        params = []
        for param in ctx.formalParameterList().formalParameter():
            params.append(self.visit(param))
        result += ", ".join(params) + ") {\n"
        result += self.visit(ctx.functionBody())
        result += "}\n"
        return result

    def visitVariableDeclaration(self, ctx:JavaScriptParser.VariableDeclarationContext):
        result = self.visit(ctx.getChild(0)) + " "
        declarations = []
        for declaration in ctx.variableDeclarationList().variableDeclaration():
            name = self.visit(declaration.getChild(0))
            if declaration.getChildCount() == 1:
                declarations.append(name)
            else:
                initializer = self.visit(declaration.getChild(2))
                declarations.append(f"{name} = {initializer}")
        result += ", ".join(declarations) + ";"
        return result

    def visitIdentifierExpression(self, ctx:JavaScriptParser.IdentifierExpressionContext):
        return ctx.getText()

    def visitLiteralExpression(self, ctx:JavaScriptParser.LiteralExpressionContext):
        return ctx.getText()

    def visitParenthesizedExpression(self, ctx:JavaScriptParser.ParenthesizedExpressionContext):
        return f"({self.visit(ctx.expression())})"

    def visitAdditiveExpression(self, ctx:JavaScriptParser.AdditiveExpressionContext):
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        operator = ctx.getChild(1).getText()
        return f"{left} {operator} {right}"

#Compila il file TypeScript in JavaScript
ts_file = "path/to/typescript/file.ts"
js_file = "path/to/javascript/file.js"
subprocess.run(["npx", "tsc", "--outFile", js_file, ts_file], check=True)

#Creare un'istanza della classe JavaScriptTypeChecker
type_checker = JavaScriptTypeChecker()

#Analizza il codice JavaScript utilizzando la grammatica ANTLR
input_stream = antlr4.FileStream(js_file)
lexer = JavaScriptLexer(input_stream)
stream = antlr4.CommonTokenStream(lexer)
parser = JavaScriptParser(stream)
tree = parser.program()

#Visita l'albero di sintassi generato con la classe JavaScriptTypeChecker
type_checker.visit(tree)

#Definisce il percorso del file di output
output_file = "path/to/javascript/file_with_type_checks.js"

#Utilizza PrintVisitor per generare il nuovo file JS con i controlli di tipo aggiunti
visitor = PrintVisitor(output_file)
visitor.visit(tree)

#Scrive il risultato nel file di output
with open(output_file, "w") as f:
    f.write(visitor.result)

print(f"File generato: {output_file}")
