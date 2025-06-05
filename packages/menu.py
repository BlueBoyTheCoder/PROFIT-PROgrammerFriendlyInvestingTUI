class Menu:
    def __init__(self):
        self.menu_parts = []
        self.components_parts = dict()
        self.components_parts_buttons = dict()
        self.current_component_loaded = None  # currently loaded component
        self.current_component_part_selected = dict()  # selected part of each component
        self.current_component_part_button_selected = dict()  # selected button of each component's part
        self.current_menu_part_selected = None  # currently selected menu part
        self.current_selection_state = None  # 0 - menu, 1 - actions

    def get_component_part_button(self, part):
        """
        Returns the name(button) of the selected part in the currently loaded component.
        """
        curr_comp = self.current_component_loaded
        curr_part_n = self.current_component_part_selected[curr_comp]
        curr_part = self.components_parts[curr_comp][curr_part_n]
        curr_part = part
        curr_butt_n = self.current_component_part_button_selected[curr_comp][curr_part]
        if curr_butt_n == -1:
            if type(self.components_parts_buttons[curr_comp][curr_part]) == str:
                return self.components_parts_buttons[curr_comp][curr_part]
            return self.components_parts_buttons[curr_comp][curr_part]
        return self.components_parts_buttons[curr_comp][curr_part][curr_butt_n]

    def menu_part_selected(self, part):
        """
        Checks if the given menu part is currently selected
        """
        return self.current_selection_state == 0 and self.menu_parts[self.current_menu_part_selected] == part

    def get_menu_part_selected(self):
        """
        Returns the currently selected menu part
        """
        return self.menu_parts[self.current_menu_part_selected]

    def get_component_part_buttons_number(self):
        """
        Returns the number of parts (buttons) in the currently loaded component
        """
        curr_comp = self.current_component_loaded
        return len(self.components_parts_buttons[curr_comp])

    def action_part_selected(self, part):
        """
        Checks if the given action part is currently selected
        """
        return self.current_selection_state == 1 and self.components_parts[self.current_component_loaded][self.current_component_part_selected[self.current_component_loaded]] == part

    def action_current_part_selected(self):
        """
        Returns the currently selected component part
        """
        return self.components_parts[self.current_component_loaded][self.current_component_part_selected[self.current_component_loaded]]

    def load_component(self):
        """
        Returns a component based on the currently selected menu part
        """
        self.current_component_loaded = self.menu_parts[self.current_menu_part_selected]
        return self.current_component_loaded

    def get_component_parts(self, name=None):
        """
        Returns parts (buttons) of the menu or menu component
        """
        if name == "MENU" or name is None:
            return self.menu_parts
        if name:
            return self.components_parts[name]
        else:
            return self.components_parts[self.get_part()]

    def get_current_component_parts_values(self):
        """
        Returns the currently selected button values of current component
        Needed for making an order
        """
        curr_comp = self.current_component_loaded
        result = []
        for key, val in self.current_component_part_button_selected[curr_comp].items():
            if val != -1:
                result += [self.components_parts_buttons[curr_comp][key][val]]
            else:
                result += [self.components_parts_buttons[curr_comp][key]]
        return result

    def get_current_component_part(self):
        """
        Returns the currently selected part of currently loaded component
        """
        return self.current_component_part_selected[self.current_component_loaded]

    def alter_state(self):
        """
        Toggles selection state between menu and action
        """
        self.current_selection_state = (self.current_selection_state + 1) % 2

    def next_part(self):
        """
        Moves to the next menu or component part, depending on the current state
        """
        if self.current_selection_state == 0:
            self.current_menu_part_selected = (self.current_menu_part_selected + 1) % len(self.menu_parts)
            self.load_component()
            return self.menu_parts[self.current_menu_part_selected]
        else:
            self.current_component_part_selected[self.current_component_loaded] = (self.current_component_part_selected[self.current_component_loaded] + 1) % len(self.components_parts[self.current_component_loaded])
            return self.components_parts[self.current_component_loaded][self.current_component_part_selected[self.current_component_loaded]]

    def prev_part(self):
        """
        Moves to the previous menu or component part, depending on the current state
        """
        if self.current_selection_state == 0:
            self.current_menu_part_selected = (self.current_menu_part_selected - 1 + len(self.menu_parts)) % len(self.menu_parts)
            self.load_component()
            return self.menu_parts[self.current_menu_part_selected]
        else:
            self.current_component_part_selected[self.current_component_loaded] = (self.current_component_part_selected[self.current_component_loaded] - 1 + len(self.components_parts[self.current_component_loaded])) % len(self.components_parts[self.current_component_loaded])
            return self.components_parts[self.current_component_loaded][self.current_component_part_selected[self.current_component_loaded]]

    def get_component(self):
        """
        Returns the name of the currently loaded component
        """
        return self.current_component_loaded

    def next_component(self):
        """
        Switches between menu and action mode
        """
        self.current_selection_state = (self.current_selection_state + 1) % 2

    def prev_component(self):
        """
        Switches between menu and action mode
        """
        self.current_selection_state = (self.current_selection_state + 1) % 2

    def next_button(self):
        """
        Selects the next button in the currently selected component part
        when user is in action menu part
        """
        if self.current_selection_state == 1:
            curr_comp = self.current_component_loaded
            curr_part_n = self.current_component_part_selected[curr_comp]
            curr_part = self.components_parts[curr_comp][curr_part_n]
            curr_butt_n = self.current_component_part_button_selected[curr_comp][curr_part]
            if curr_butt_n != -1:
                self.current_component_part_button_selected[curr_comp][curr_part] = (curr_butt_n + 1) % len(self.components_parts_buttons[curr_comp][curr_part])

    def set_button_text(self, text: str):
        """
        Sets the button text in the current component part
        """
        if self.current_selection_state == 1:
            curr_comp = self.current_component_loaded
            curr_part_n = self.current_component_part_selected[curr_comp]
            curr_part = self.components_parts[curr_comp][curr_part_n]
            curr_butt_n = self.current_component_part_button_selected[curr_comp][curr_part]
            if curr_butt_n == -1:
                self.components_parts_buttons[curr_comp][curr_part] = text

    def get_button_number(self):
        """
        Returns the index of the selected component part
        """
        if self.current_selection_state == 1:
            curr_comp = self.current_component_loaded
            curr_part_n = self.current_component_part_selected[curr_comp]
            return curr_part_n
        return -1

    def load_component_from_json(self, name: str, subparts: list[str], subparts_buttons: dict):
        """
        Loads a component into the menu
        """
        self.menu_parts.append(name)
        self.components_parts[name] = subparts
        self.components_parts_buttons[name] = subparts_buttons
        self.current_component_part_selected[name] = 0  # subparts[0]
        self.current_component_part_button_selected[name] = subparts_buttons.copy()
        for button in self.current_component_part_button_selected[name]:
            if type(self.current_component_part_button_selected[name][button]) == str:
                self.current_component_part_button_selected[name][button] = -1
            else:
                self.current_component_part_button_selected[name][button] = 0

    def load_menu_from_json(self, json: dict):
        """
        Loads the full menu from a JSON dictionary: menu parts, components, buttons
        """
        for part in json["menu"]["menu_parts"]:
            self.load_component_from_json(part, json["menu"]["menu_parts"][part], json["menu"]["menu_buttons"][part])
        self.current_menu_part_selected = 0
        self.current_selection_state = 0
        self.current_component_loaded = next(iter(json["menu"]["menu_parts"]))
