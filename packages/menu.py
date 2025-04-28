class Menu:
    def __init__(self):
        self.menu_parts = []
        self.current_menu_part_number = None
        self.current_menu_component_part_number = None
        self.current_part_loaded=None
        self.menu_parts_components = dict()


    def get_part(self):
        return self.menu_parts[self.current_menu_part_number]


    def get_part_components(self, name=None):
        if name:
            return self.menu_parts_components[name]
        else:
            return self.menu_parts_components[self.get_part()]


    def next_part(self):
        self.current_menu_part_number = (self.current_menu_part_number + 1) % len(self.menu_parts)
        self.current_menu_component_part_number = 0
        return self.get_part()


    def prev_part(self):
        self.current_menu_part_number = (self.current_menu_part_number + len(self.menu_parts) - 1) % len(self.menu_parts)
        self.current_menu_component_part_number = 0
        return self.get_part()


    def get_component(self):
        return self.menu_parts_components[self.get_part()][self.current_menu_component_part_number]


    def next_component(self):
        self.current_menu_component_part_number = (self.current_menu_component_part_number + 1) % len(self.menu_parts_components[self.get_part()])
        return self.get_component()


    def prev_component(self):
        self.current_menu_component_part_number = (self.current_menu_component_part_number
            + len(self.menu_parts_components[self.get_part()]) - 1) % len(self.menu_parts_components[self.get_part()])
        return self.get_component()


    def load_component(self, name: str, subparts: list[str]):
        self.menu_parts.append(name)
        self.menu_parts_components[name] = subparts
        if self.current_menu_component_part_number == None:
            self.current_menu_component_part_number = 0
        if self.current_menu_part_number == None:
            self.current_menu_part_number = 0
        if self.current_part_loaded == None:
            self.current_part_loaded = 0


    def load_menu_from_json(self, json: dict):
        for part in json['menu']:
            self.load_component(part, json['menu'][part])




# class Menu:
#     def __init__(self):
#         self.menu_parts = []
#         self.current_menu_part_number = None
#         self.current_menu_component_part_number = None
#         self.menu_parts_components = dict()


#     def get_part(self):
#         return self.menu_parts[self.current_menu_part_number]


#     def get_part_components(self, name=None):
#         if name:
#             return self.menu_parts_components[name]
#         else:
#             return self.menu_parts_components[self.get_part()]


#     def next_part(self):
#         self.current_menu_part_number = (self.current_menu_part_number + 1) % len(self.menu_parts)
#         self.current_menu_component_part_number = 0
#         return self.get_part()


#     def prev_part(self):
#         self.current_menu_part_number = (self.current_menu_part_number + len(self.menu_parts) - 1) % len(self.menu_parts)
#         self.current_menu_component_part_number = 0
#         return self.get_part()


#     def get_component(self):
#         return self.menu_parts_components[self.get_part()][self.current_menu_component_part_number]


#     def next_component(self):
#         self.current_menu_component_part_number = (self.current_menu_component_part_number + 1) % len(self.menu_parts_components[self.get_part()])
#         return self.get_component()


#     def prev_component(self):
#         self.current_menu_component_part_number = (self.current_menu_component_part_number
#             + len(self.menu_parts_components[self.get_part()]) - 1) % len(self.menu_parts_components[self.get_part()])
#         return self.get_component()


#     def load_component(self, name: str, subparts: list[str]):
#         self.menu_parts.append(name)
#         self.menu_parts_components[name] = subparts
#         if self.current_menu_component_part_number == None:
#             self.current_menu_component_part_number = 0
#         if self.current_menu_part_number == None:
#             self.current_menu_part_number = 0


#     def load_menu_from_json(self, json: dict):
#         for part in json['menu']:
#             self.load_component(part, json['menu'][part])
