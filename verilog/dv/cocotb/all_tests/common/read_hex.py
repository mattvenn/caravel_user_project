

class ReadHex():
    def __init__(self, file_name):
        self.file_name = file_name

    def hex_to_list(self, hex_string):
        hex_string = hex_string.replace("\n", " ").replace("@", "").strip()
        hex_values = hex_string.split()
        return [int(hex_value, 16) for hex_value in hex_values]

    def read_hex(self):
        hex_dict = {}
        with open(self.file_name, 'r') as file:
            current_key = None
            current_data = []

            for line in file:
                if line.startswith("@"):
                    if current_key is not None:
                        hex_dict[current_key] = self.hex_to_list(" ".join(current_data))
                    current_key = int(line.strip().replace("@", ""), 16)
                    current_data = []
                else:
                    current_data.append(line.strip())
            if current_key is not None:
                hex_dict[current_key] = self.hex_to_list(" ".join(current_data))
        return hex_dict
