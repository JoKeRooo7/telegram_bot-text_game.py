class NPC:
    def __init__(self, name: str) -> None:
        # self._id = _id
        self._name = name

    # @property
    # def id(self) -> int:
    #     return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def talk(self) -> None:
        pass

    def receive(self, item: str) -> None:
        """Get item from protagonist"""
        print(f"{self._name} receive {item}")
