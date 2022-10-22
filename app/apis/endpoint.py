import yaml


class EndPoint:
    def __init__(self):
        config = self._read_config()
        self.headers = {
            "accept": "text/plain",
            "Authorization": "Bearer " + config["alemira"]["userapi"]["token"],
        }
        self.uri = config["alemira"]["userapi"]["uri"]

    def _read_config(self) -> dict:
        with open("./app/config.yaml") as f:
            data = f.read()
            return yaml.safe_load(data)
