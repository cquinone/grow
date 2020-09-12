
class thing():
    def __init__(self,name,used=True):
        self.name = name
        self.used = used


trunk_list = []
trunk_list.append(thing("yo"))

print trunk_list[0].used
yo = trunk_list[0]
yo.used = False
print trunk_list[0].used
