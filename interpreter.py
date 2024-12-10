"""
Emoji cheat sheet:


Math: ➕ ➖ ✖ ➗
Data Types: int 🔢 String 📜 char 🔤 bool ⚡
Print: 🖨
Logic: if = 🔍/end🔍, else = ↩️, for = 🧭/ end🧭, while = 🔄/end🔄
Array: 🟦
Method: ✨/end✨
Errors: 🤡


"""


import re




# Global variable and method stores
var_store = {}
method_store = {}






# The base class for all exceptions in the Emoji++ interpreter.
# Inherits from Python's exception class
# A specific error type will derive from this class
class EmojiPPException(Exception):
  pass




# Takes a single parameter "expression". Expression represents an expression in Emoji++
# Processes expressions, replaces variables with their values, and evaluates them.
def evaluate_expression(expression):




   #Evaluate mathematical and literal expressions with Emoji++ types.
   emoji_to_python = {'➕': '+', '➖': '-', '✖': '*', '➗': '/'}


   # Loop replaces python operators with Emoji++ operators
   for emoji, op in emoji_to_python.items():
       expression = expression.replace(emoji, op)




   # Handle array indexing
   array_access_match = re.match(r"(\w+)\[(\d+)\]", expression)
   if array_access_match:
       array_name, index = array_access_match.groups()
       index = int(index)
       if array_name in var_store and isinstance(var_store[array_name], list):
           return var_store[array_name][index]
       else:
           raise EmojiPPException(f"🤡 UNDEFINED VARIABLE ERROR: '{array_name}[{index}]' is not defined or is not an array.")


   # Go through var_store and replace them in the expression with their values
   # Regex ensures only whole variable names are replaced to avoid partial substitutions
   for var in var_store:
       if var in expression:
           value = var_store[var]
           if isinstance(value, str):
               expression = re.sub(rf'\b{var}\b', f'"{value}"', expression)
           elif isinstance(value, bool):
               expression = re.sub(rf'\b{var}\b', str(value).lower(), expression)
           elif isinstance(value, int) or isinstance(value, list):  # Include arrays
               expression = re.sub(rf'\b{var}\b', str(value), expression)


   try:
    # After replacing all parts with Emoji++ , returns final expression
       return eval(expression)
   except NameError:
       raise EmojiPPException(f"🤡 UNDEFINED VARIABLE ERROR: '{expression}' contains an undefined variable.")
   except SyntaxError:
       raise EmojiPPException(f"🤡 SYNTAX ERROR: Invalid syntax in expression '{expression}'.")
   except Exception as error:
       raise EmojiPPException(f"🤡 ERROR: {error}")










# Takes in 1 parameter which represents a print statement in Emoji++ Source Code
def handle_print(statement):


   # 🖨 emoji is the print command
   # [1:] removes the 🖨 and trims extra space
  expr = statement[1:].strip()


   # Evaluate expression
  value = evaluate_expression(expr)
  print("😫" if isinstance(value, int) and value == 69 else value)






# Accepts name, parameters and the methods body (list of lines that make up body)
def handle_method_definition(name, params, body):


   # Storing into global method dictionary
  method_store[name] = {'params': params.split(',') if params else [], 'body': body}






def handle_method_invocation(name, args):


   # Check if name exists in dictionary
  if name not in method_store:
      raise EmojiPPException(f"Method '{name}' is not defined.")


   # Get method details
  method = method_store[name]
  params = method['params']
  body = method['body']


   # Removes whitespace from each argument
  args = [arg.strip() for arg in args if arg.strip()] if args else []


   # Removes empty strings
  if len(params) != len(args):
      raise EmojiPPException(f"Method '{name}' expects {len(params)} arguments, but got {len(args)}.")


  global var_store
   # Save current state of var_store
  original_var_store = var_store.copy()


   # Binds provided argument into methods parameters
  for param, arg in zip(params, args):
      var_store[param.strip()] = evaluate_expression(arg)
  try:
      # Execute method body
      run_block(body)
  finally:


      # Restore original var_store after to avoid affecting global variables
      var_store = original_var_store






def handle_assignment(statement):


   # Using "regular" expression to match assignments with Emoji++
   match = re.match(r"(🔢|📜|🔤|⚡|🟦)\s+(\w+)\s*=\s*(.+)", statement)
   if match:


       # Captures emoji data type, variable name value being assigned
       type_emoji, var_name, expr = match.groups()
       if type_emoji == "🔢":  # Integer
           value = evaluate_expression(expr.strip())
           if not isinstance(value, int):
               raise EmojiPPException(f"🤡 TYPE ERROR: Expected an integer for {var_name}, but got {type(value).__name__}.")
       elif type_emoji == "📜":  # String
           if not (expr.startswith('"') and expr.endswith('"')):
               raise EmojiPPException(f"🤡 TYPE ERROR: Invalid string format for {var_name}.")


           # Remove surrounding quotes
           value = expr[1:-1]




       elif type_emoji == "🔤":  # Character
           if not (expr.startswith("'") and expr.endswith("'") and len(expr[1:-1]) == 1):
               raise EmojiPPException(f"🤡 TYPE ERROR: Invalid char format for {var_name}.")


           # Remove surrounding quotes
           value = expr[1:-1]




       elif type_emoji == "⚡":  # Boolean


           # Converting ⚡ to true or false
           value = expr.strip().lower() == "true"




       elif type_emoji == "🟦":  # Array


           # makes sure data is carried into Emoji array
           value = eval(expr.strip())


           #Store the variable
       var_store[var_name] = value




   else:


       # If the statement does not include a type declaration it is reassigned
       match = re.match(r"(\w+)\s*=\s*(.+)", statement)
       if match:


           # Validating reassignment
           # Used for for loop variable i
           var_name, expr = match.groups()
           value = evaluate_expression(expr.strip())
           var_store[var_name] = value


       else:
           raise EmojiPPException(f"🤡 SYNTAX ERROR: Invalid assignment syntax: '{statement}'.")






# Must have a variable, start and ending expression along with lines representing loops body
def handle_for_loop(var, start_expr, end_expr, loop_lines):
   try:


       # Converts start and end into their integer values
       # Example:
       # For 🧭 i = 1 to 5:
       # start_expr = "1" → start = 1
       # end_expr = "5" → end = 5
       start = evaluate_expression(start_expr)
       end = evaluate_expression(end_expr)


       # Checks if start and end are integers
       if not isinstance(start, int) or not isinstance(end, int):
           raise EmojiPPException("🤡 FOR LOOP ERROR: Loop range must be integers.")


       # Iterates over range: start end
       # Executes loop body by calling run_block
       for value in range(start, end + 1):
           var_store[var] = value  # Assign the loop variable
           run_block(loop_lines)  # Execute the block for each iteration




   except EmojiPPException as e:
       raise EmojiPPException(f"🤡 FOR LOOP ERROR: {e}")
   except Exception as e:
       raise EmojiPPException(f"🤡 UNEXPECTED ERROR in FOR LOOP: {e}")






#Execute a block of code.
def run_block(block_lines):
  run_source(block_lines)




#  Execute a single Emoji++ statement.
def execute_statement(statement):
  statement = statement.strip()




  # Ignore comments and empty lines
  if not statement or statement.startswith('#'):
      return




  # Handle print statements
  if statement.startswith('🖨'):
      handle_print(statement)


  # Handle variable assignments
  elif '=' in statement:
      handle_assignment(statement)
  else:
      raise EmojiPPException(f"Unknown statement: '{statement}'")




# Takes in condition and the body of the while loop as a list of strings
def handle_while_loop(condition, loop_lines):


   try:


       # Substitutes condition with the value found in var_store
       # Uses pythons eval() function
       while evaluate_expression(condition):
           run_block(loop_lines)
   except EmojiPPException as e:
       raise EmojiPPException(f"🤡 WHILE LOOP ERROR: {e}")
   except Exception as e:
       raise EmojiPPException(f"🤡 UNEXPECTED ERROR in WHILE LOOP: {e}")






# Process Source Code and execute line by line
def run_source(source_code):
   index = 0


   # Go through each line of source code
   while index < len(source_code):


       # Remove leading and trailing whitespace
       line = source_code[index].strip()


       # Ignore blank lines and comments
       if not line or line.startswith('#'):
           index += 1
           continue


       # Use regex to extract method name and parameters
       if line.startswith("✨"):
           # Method definition
           match = re.match(r"✨\s+(\w+)\s*\((.*?)\)", line)
           if match:
               method_name, params = match.groups()
               index += 1
               method_body = []


               # Collects method body until reaches end✨
               while index < len(source_code) and not source_code[index].strip().startswith("end✨"):
                   method_body.append(source_code[index].strip())
                   index += 1


                   # Store method details
               handle_method_definition(method_name, params, method_body)
           index += 1


       # Looking at for loops
       elif line.startswith("🧭"):


           # Use regex to extract 🧭, start and end
           match = re.match(r"🧭\s+(\w+)\s*=\s*(.+?)\s*to\s*(.+)", line)
           if match:
               var, start_expr, end_expr = match.groups()
               index += 1
               loop_block = []


               # Stops when reaches "end🧭"
               while index < len(source_code) and not source_code[index].strip().startswith("end🧭"):
                   loop_block.append(source_code[index].strip())
                   index += 1
               if index < len(source_code) and source_code[index].strip().startswith("end🧭"):
                   handle_for_loop(var, start_expr, end_expr, loop_block)
               index += 1




           # While loop handling
       elif line.startswith("🔄"):


           # Looks for 🔄 and then the argument after it
           # Example: 🔄 counter < 5
           # it is looking at "counter < 5"
           match = re.match(r"🔄\s+(.+)", line)
           if match:
               condition = match.group(1)


               # Moving through interpreter
               index += 1


               # Create empy list to store lines that make up body of while loop
               loop_block = []


               # Collect lines in loop body
               while index < len(source_code) and not source_code[index].strip().startswith("end🔄"):
                   loop_block.append(source_code[index].strip())
                   index += 1


                   # Calls handle_while_loop and passes the condition
               if index < len(source_code) and source_code[index].strip().startswith("end🔄"):
                   handle_while_loop(condition, loop_block)


                # Skip the 'end🔄' line
               index += 1


       # If statement
       elif line.startswith("🔍"):
           match = re.match(r"🔍\s+(.+)\s+🖨\s+(.+)", line)  # Single-line if


           # Interpreter only needs to check for a condition and execute a single command on same line
           # Nice and simple
           if match:
               condition, output = match.groups()
               if evaluate_expression(condition):
                   handle_print(f"🖨 {output}")
               index += 1
               continue




           # Multi-line if
           match = re.match(r"🔍\s+(.+)", line)

           # First indentify condition and gather block of commands
           # Stop at end🔍
           # Having multiple end🔍  can be redundant
           if match:
               condition = match.group(1)
               index += 1
               block_lines = []
               while index < len(source_code) and not source_code[index].strip().startswith("end🔍"):
                   block_lines.append(source_code[index].strip())
                   index += 1
               if evaluate_expression(condition):
                   run_block(block_lines)




               # Skip the 'end🔍' line
               index += 1


       elif '(' in line and line.endswith(')'):


           # Method invocation
           match = re.match(r"(\w+)\((.*)\)", line)
           if match:
               method_name, args = match.groups()
               handle_method_invocation(method_name, args.split(',') if args.strip() else [])
           index += 1


       else:


           # Lines that dont match pattern get passes to execute_statement
           execute_statement(line)
           index += 1


def main():


  source_file = "program3.emojiPP"
  try:
      with open(source_file, "r") as file:
          source_lines = file.readlines()


   # Passes the pre-read source code to be run
      run_source(source_lines)
  except FileNotFoundError:
      print(f"Error: File '{source_file}' not found.")
  except EmojiPPException as e:
      print(f"Interpreter Error: {e}")
  except Exception as e:
      print(f"Unexpected Error: {e}")



if __name__ == "__main__":
  main()
