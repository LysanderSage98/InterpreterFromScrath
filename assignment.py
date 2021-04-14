import pathlib
import threading
import re
import sys

MAX_INT = 1000
MAX_STACK = 100
mem = []
loop_stack = []
work = threading.Event()
work.set()


def own_exit(info):
	if info:
		raise RuntimeError(info)
	else:
		exit()

	
stat = {
	True: "full",
	False: "empty"
}

operators = {
	"a": (lambda val: mem.append(0) if len(mem) < MAX_STACK else own_exit(f"Stack is {stat[bool(mem)]}! Instruction {val}")),
	"b": (lambda val: 0 & mem.pop() if mem else own_exit(f"Stack is {stat[bool(mem)]}! Instruction {val}")),
	"c": (lambda val: mem.append(mem[-1] - mem[-2])),
	"d": (lambda val: mem.append(mem.pop() - 1) if mem else own_exit(f"Can't decrement! Stack is {stat[bool(mem)]}! Instruction {val}")),
	"e": (lambda val: mem.append(mem[-1] % mem[-2])),
	"f": (lambda val: print(chr(mem[-1]), end = "")),
	"g": (lambda val: mem.append(sum(mem[-2:]))),
	"h": (lambda val: mem.append(int(input("input any number:\n")))),
	"i": (lambda val: mem.append(mem.pop() + 1) if mem and mem[-1] < MAX_INT else own_exit(f"Can't increment! Stack is {stat[bool(mem)]} or value is {mem[-1]}! Instruction {val}")),
	"j": (lambda val: mem.append(ord(input("input any character:\n")))),
	"k": (lambda val: work.clear() if mem[-1] == 0 else None),
	"l": (lambda val: mem.insert(len(mem) - 2, mem.pop())),
	"m": (lambda val: mem.append(mem[-1] * mem[-2])),
	"n": (lambda val: mem.append(1) if mem[-1] == mem[-2] else mem.append(0)),
	"o": (lambda val: 0 & mem.pop(mem[-1])),
	"p": (lambda val: mem.append(mem[-1] // mem[-2])),
	"q": (lambda val: mem.append(mem[-1]) if mem and len(mem) < MAX_STACK else own_exit(f"Stack is {stat[bool(mem)]}! Instruction {val}")),
	"r": (lambda val: mem.append(len(mem))),
	"s": (lambda val: mem.insert(abs(len(mem) - 2), mem.pop(len(mem) - mem[-1] - 1)) or mem.insert(len(mem) - mem[-1] - 1, mem.pop())),
	"t": (lambda val: loop_stack[len(loop_stack) - loop_stack.index((i, "t")) - 1][0] if not mem[-1] else None),
	"u": (lambda val: loop_stack[abs(loop_stack.index((i, "u")) - len(loop_stack)) - 1][0] if mem[-1] else None),
	"v": (lambda val: mem.append(mem.pop()+5) if mem and mem[-1] < MAX_INT-5 else own_exit(f"Can't increment! Stack is full or value is too big! Instruction {val}")),
	"w": (lambda val: mem.append(mem.pop()-5) if mem and mem[-1] > 4 else own_exit("Can't decrement! Stack is empty or value is too small! Instruction {val}")),
	"x": (lambda val: print(mem[-1], end = "")),
	"y": (lambda val: mem.clear() if mem else own_exit(f"Stack is {stat[bool(mem)]}!")),
	"z": (lambda val: exit())
}


def clean(line, data: str):
	match = re.search("([a-z]*)(//|#|\\n)*", re.sub("\s", "", data.lower()))
	not_blank = match.group()
	if not_blank:
		found = match.group(1).strip()
		if len(res := re.search("[a-z]*", found).group()) == len(found):
			return res
		else:
			raise RuntimeError(f"Invalid token in '{found}' in line {line}!")
	else:
		return ""


if __name__ == '__main__':
	args = sys.argv[1:]
	if pathlib.Path(args[0]).exists():
		f = open(args[0])
		code = f.readlines()
		code = "".join(map(lambda x: clean(*x), enumerate(code)))
	else:
		code = clean(0, args[0])
	i = 0
	print(code)
	for char in enumerate(code):
		loop_stack.append(char) if char[1] in ["t", "u"] else None
	while i < len(code):
		char = code[i]
		if work.isSet():
			i = operators[char](i) or i
		else:
			work.set()
		i += 1
