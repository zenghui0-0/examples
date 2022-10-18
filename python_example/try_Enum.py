from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)
print(Color(1))
for i in Color:
    print(i.name, i.value)