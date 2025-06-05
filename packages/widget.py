from client import Client


class Widget:
    def __init__(self, instruments_uuid=None):
        self.client = Client()
        self.pending_instruments = None
        if instruments_uuid:
            if type(instruments_uuid) == str:
                self.instruments = dict([(instruments_uuid, None)])
            elif type(instruments_uuid) == list:
                self.instruments = dict([(inst, None) for inst in instruments_uuid])
        else:
            self.instruments = dict()

    def add_instrument(self, instruments_uuid: str | list):
        """
        Adds new instrument or instruments (if list used)
        to the Widget
        """
        if type(instruments_uuid) == str:
            if self.client.uuid_exists(instruments_uuid):
                self.instruments[instruments_uuid] = None
        elif type(instruments_uuid) == list:
            for inst in instruments_uuid:
                if self.client.uuid_exists(inst):
                    self.instruments[inst] = None

    def pop_instrument(self, instruments_uuid: str | list):
        """
        Delete instrument or instruments (if list used)
        from the Widget
        """
        if type(instruments_uuid) == str:
            self.instruments.pop(instruments_uuid)
        elif type(instruments_uuid) == list:
            for inst in instruments_uuid:
                self.instruments.pop(inst)

    def pop_all_instruments(self):
        self.instruments = dict()

    def set_pending_instruments(self, instruments):
        self.pending_instruments = instruments

    def load_pending_instruments(self):
        """
        Loads new instruments, deleting previous
        when there are pending instuments
        """
        if self.pending_instruments != None:
            self.pop_all_instruments()
            self.add_instrument(self.pending_instruments)
            self.pending_instruments = None

    def reload_instruments(self):
        """
        Loads new instruments, when pending
        Reloads data for instruments
        """
        self.load_pending_instruments()

        for uuid in self.instruments:
            data = self.client.get_lastday_data(uuid)[0]
            data_dict = dict()
            data_dict["timestamp"] = data["timestamp"]
            data_dict["price"] = round(data["close"], 2)
            data_dict["change"] = round(100 * (data["close"] / data["open"] - 1), 2)

            self.instruments[uuid] = data_dict

    def reload_instrument(self, uuid):
        """
        Gets data for given instrument
        """
        data = self.client.get_lastday_data(uuid)[0]
        data_dict = dict()
        data_dict["timestamp"] = data["timestamp"]
        data_dict["price"] = round(data["close"], 2)
        data_dict["change"] = round(100 * (data["close"] / data["open"] - 1), 2)

        self.instruments[uuid] = data_dict

    def get_instruments_data(self):
        return self.instruments

    def get_widget_patch(self, max_length):
        """
        Returns created list of stings,
        representing actual results of financial instruments
        """
        self.reload_instruments()
        whole_patch = []
        length = 0
        for uuid in self.instruments:
            uuid_data = self.get_instruments_data()[uuid]
            string = uuid + " " + str(uuid_data["price"]) + " " + str(uuid_data["change"]) + "%"
            if uuid_data["change"] > 0:
                patch = (string, 1)
                length += len(string) + 6
            elif uuid_data["change"] < 0:
                patch = (string, -1)
                length += len(string) + 6
            else:
                patch = (string, 0)
                length += len(string) + 5

            if length > max_length:
                return whole_patch

            whole_patch.append(patch)

        return whole_patch
