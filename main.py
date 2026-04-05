from collections import defaultdict, deque
from graphviz import Digraph

state_id = 0


def new_state():
    global state_id
    s = state_id
    state_id += 1
    return s


def reset_states():
    global state_id
    state_id = 0


class NFA:
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions


# ---------------- REGEX VALIDATION ---------------- #

def validate_regex(regex):
    if not regex:
        return False, "Regex cannot be empty."

    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789|*+?().")

    for ch in regex:
        if ch not in allowed:
            return False, f"Invalid character detected: {ch}"

    stack = []
    for ch in regex:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return False, "Unbalanced parentheses."
            stack.pop()

    if stack:
        return False, "Unbalanced parentheses."

    if regex[0] in "|.":
        return False, "Expression cannot start with | or ."

    if regex[-1] in "|.":
        return False, "Expression cannot end with | or ."

    return True, "Valid"


# ---------------- REGEX PROCESSING ---------------- #

def add_concat(regex):
    result = ""
    for i in range(len(regex)):
        result += regex[i]
        if i + 1 < len(regex):
            if (regex[i].isalnum() or regex[i] in ")*+?") and \
               (regex[i + 1].isalnum() or regex[i + 1] == "("):
                result += "."
    return result


def precedence(op):
    if op in "*+?":
        return 3
    if op == ".":
        return 2
    if op == "|":
        return 1
    return 0


def infix_to_postfix(regex):
    stack = []
    output = ""

    for char in regex:
        if char.isalnum():
            output += char
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while stack and stack[-1] != "(":
                output += stack.pop()
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                output += stack.pop()
            stack.append(char)

    while stack:
        output += stack.pop()

    return output


# ---------------- THOMPSON NFA ---------------- #

def basic_nfa(symbol):
    start = new_state()
    accept = new_state()
    transitions = defaultdict(lambda: defaultdict(set))
    transitions[start][symbol].add(accept)
    return NFA(start, accept, transitions)


def thompson(postfix):
    stack = []

    for char in postfix:
        if char.isalnum():
            stack.append(basic_nfa(char))

        elif char == ".":
            n2 = stack.pop()
            n1 = stack.pop()
            n1.transitions[n1.accept]['ε'].add(n2.start)
            n1.transitions.update(n2.transitions)
            stack.append(NFA(n1.start, n2.accept, n1.transitions))

        elif char == "|":
            n2 = stack.pop()
            n1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = defaultdict(lambda: defaultdict(set))

            transitions[start]['ε'].update([n1.start, n2.start])
            transitions[n1.accept]['ε'].add(accept)
            transitions[n2.accept]['ε'].add(accept)

            transitions.update(n1.transitions)
            transitions.update(n2.transitions)

            stack.append(NFA(start, accept, transitions))

        elif char == "*":
            n = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = defaultdict(lambda: defaultdict(set))

            transitions[start]['ε'].update([n.start, accept])
            transitions[n.accept]['ε'].update([n.start, accept])

            transitions.update(n.transitions)
            stack.append(NFA(start, accept, transitions))

        elif char == "+":
            n = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = defaultdict(lambda: defaultdict(set))

            transitions[start]['ε'].add(n.start)
            transitions[n.accept]['ε'].update([n.start, accept])

            transitions.update(n.transitions)
            stack.append(NFA(start, accept, transitions))

        elif char == "?":
            n = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = defaultdict(lambda: defaultdict(set))

            transitions[start]['ε'].update([n.start, accept])
            transitions[n.accept]['ε'].add(accept)

            transitions.update(n.transitions)
            stack.append(NFA(start, accept, transitions))

    return stack.pop()


# ---------------- DRAW NFA ---------------- #

def draw_nfa(nfa):
    dot = Digraph(engine='neato')
    dot.attr(overlap='false')

    dot.node("start", shape="none")
    dot.edge("start", str(nfa.start))

    states = set()
    for s in nfa.transitions:
        states.add(s)
        for sym in nfa.transitions[s]:
            for d in nfa.transitions[s][sym]:
                states.add(d)

    for s in states:
        shape = "doublecircle" if s == nfa.accept else "circle"
        dot.node(str(s), shape=shape)

    for s in nfa.transitions:
        for sym in nfa.transitions[s]:
            for d in nfa.transitions[s][sym]:
                dot.edge(str(s), str(d), label=sym)

    dot.render("NFA", format="png", cleanup=True)


# ---------------- NFA TO DFA ---------------- #

def epsilon_closure(states, transitions):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for nxt in transitions[state].get('ε', []):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions[state].get(symbol, []))
    return result


def nfa_to_dfa(nfa):
    symbols = set()
    for s in nfa.transitions:
        for sym in nfa.transitions[s]:
            if sym != 'ε':
                symbols.add(sym)

    start = frozenset(epsilon_closure({nfa.start}, nfa.transitions))
    dfa_map = {start: 0}
    dfa_trans = {}
    queue = deque([start])
    accept_states = set()
    state_count = 1

    while queue:
        current = queue.popleft()
        dfa_trans[dfa_map[current]] = {}

        if nfa.accept in current:
            accept_states.add(dfa_map[current])

        for sym in symbols:
            nxt = frozenset(
                epsilon_closure(move(current, sym, nfa.transitions), nfa.transitions)
            )
            if nxt not in dfa_map:
                dfa_map[nxt] = state_count
                state_count += 1
                queue.append(nxt)
            dfa_trans[dfa_map[current]][sym] = dfa_map[nxt]

    return dfa_trans, accept_states


# ---------------- DFA MINIMIZATION ---------------- #

def minimize_dfa(transitions, accept_states):
    states = set(transitions.keys())
    non_accept = states - accept_states

    partitions = [accept_states, non_accept]

    changed = True
    while changed:
        changed = False
        new_partitions = []
        for group in partitions:
            grouped = {}
            for state in group:
                key = tuple((sym, next(
                    i for i, g in enumerate(partitions)
                    if transitions[state].get(sym) in g
                )) for sym in sorted(transitions[state]))
                grouped.setdefault(key, set()).add(state)
            if len(grouped) > 1:
                changed = True
            new_partitions.extend(grouped.values())
        partitions = new_partitions

    mapping = {}
    for i, group in enumerate(partitions):
        for state in group:
            mapping[state] = i

    min_trans = {}
    min_accept = set()

    for state in transitions:
        new_state = mapping[state]
        min_trans.setdefault(new_state, {})
        for sym in transitions[state]:
            min_trans[new_state][sym] = mapping[transitions[state][sym]]
        if state in accept_states:
            min_accept.add(new_state)

    return min_trans, min_accept


# ---------------- DRAW DFA ---------------- #

def draw_dfa(transitions, accept_states, name):
    dot = Digraph(engine='neato')
    dot.attr(overlap='false')

    dot.node("start", shape="none")
    dot.edge("start", "0")

    for s in transitions:
        shape = "doublecircle" if s in accept_states else "circle"
        dot.node(str(s), shape=shape)

    edge_labels = defaultdict(list)
    for s in transitions:
        for sym in transitions[s]:
            d = transitions[s][sym]
            edge_labels[(s, d)].append(sym)

    for (s, d), syms in edge_labels.items():
        dot.edge(str(s), str(d), label=",".join(syms))

    dot.render(name, format="png", cleanup=True)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    reset_states()

    regex = input("Enter regex: ").strip()
    valid, msg = validate_regex(regex)

    if not valid:
        print("Error:", msg)
        exit()

    print("1. NFA\n2. DFA\n3. Minimized DFA\n4. All")
    choice = input("Choose option: ").strip()

    regex = add_concat(regex)
    postfix = infix_to_postfix(regex)
    nfa = thompson(postfix)

    if choice == "1":
        draw_nfa(nfa)
        print("NFA generated!")

    elif choice == "2":
        dfa_trans, accept_states = nfa_to_dfa(nfa)
        draw_dfa(dfa_trans, accept_states, "DFA")
        print("DFA generated!")

    elif choice == "3":
        dfa_trans, accept_states = nfa_to_dfa(nfa)
        min_trans, min_accept = minimize_dfa(dfa_trans, accept_states)
        draw_dfa(min_trans, min_accept, "Minimized_DFA")
        print("Minimized DFA generated!")

    elif choice == "4":
        draw_nfa(nfa)
        dfa_trans, accept_states = nfa_to_dfa(nfa)
        draw_dfa(dfa_trans, accept_states, "DFA")
        min_trans, min_accept = minimize_dfa(dfa_trans, accept_states)
        draw_dfa(min_trans, min_accept, "Minimized_DFA")
        print("All generated!")