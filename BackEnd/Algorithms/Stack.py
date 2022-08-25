class Stack:
    members = None
    weight_each = None
    height = None
    width = None
    length = None
    name = None
    area = None
    volume = None
    def __init__(self, parcel_members, weight_each, stack_height, stack_width, stack_length, stack_name):
        Stack.members = parcel_members
        Stack.weight_each = weight_each
        Stack.height = stack_height
        Stack.width = stack_width
        Stack.length = stack_length
        Stack.name = stack_name
        Stack.area = Stack.width * Stack.length
        Stack.volume = Stack.area * Stack.height