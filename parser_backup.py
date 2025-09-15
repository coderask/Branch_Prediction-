
'''TAKE A PIECE OF CODE AND GENERATE A TRACE OF THE BRANCH TAKEN FOR A CORESSSPONDING ADRESS'''

import ast
import itertools

address_counter = itertools.count(start=1000)

# --- Branch extraction using line numbers ---
def extract_branches(node, branches_map=None):
    if branches_map is None:
        branches_map = {}

    if isinstance(node, ast.If):
        line_no = node.lineno
        if line_no not in branches_map:
            branches_map[line_no] = next(address_counter)

        # Recurse into 'if' body
        for stmt in node.body:
            extract_branches(stmt, branches_map)

        # Recurse into 'else' or 'elif'
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                extract_branches(node.orelse[0], branches_map)
            else:
                for stmt in node.orelse:
                    extract_branches(stmt, branches_map)

    for child in ast.iter_child_nodes(node):
        extract_branches(child, branches_map)

    return branches_map

# --- Synthetic function with loops and branches ---
code = """
def simulate_scores():
    scores = [45, 52, 63, 78, 82, 91, 100, 67, 88, 49]
    for _ in range(5):  # repeat loop to generate history
        for score in scores:
            if score >= 90:
                grade = "A"
                if score == 100:
                    comment = "Perfect!"
                else:
                    comment = "Excellent"
            elif score >= 75:
                grade = "B"
                if score >= 85:
                    comment = "Good job"
                else:
                    comment = "Well done"
            elif score >= 60:
                grade = "C"
                comment = "Needs improvement"
            else:
                grade = "F"
                if score < 50:
                    comment = "Failing badly"
                else:
                    comment = "Barely passing"
            if score % 2 == 0:
                even_comment = "Even score"
            else:
                even_comment = "Odd score"
"""

tree = ast.parse(code)
branches_map = extract_branches(tree)

# --- Generate repeated branch trace ---
trace = []

scores = [45, 52, 63, 78, 82, 91, 100, 67, 88, 49]
for _ in range(5):  # repeat loop
    for score in scores:
        for line_no, addr in branches_map.items():
            # Find the node corresponding to this line number
            # Evaluate condition if possible
            node = None
            for n in ast.walk(tree):
                if isinstance(n, ast.If) and n.lineno == line_no:
                    node = n
                    break

            if node is None:
                continue  # safety
            # Compile and evaluate the condition
            cond_expr = compile(ast.Expression(node.test), filename="<ast>", mode="eval")
            taken = int(eval(cond_expr, {'score': score}))
            trace.append((addr, taken))

# --- Output ---
print("Addresses:", list(branches_map.values()))
print("Trace (address, taken):")
for t in trace:
    print(t)