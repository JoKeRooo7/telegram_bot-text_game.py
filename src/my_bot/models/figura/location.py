class Location:
    def __init__(self, _id: int, name: str, descriptoin: str) -> None:
        self._id = _id
        self._name = name
        self._description = descriptoin

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value


# для метода go
class Direction:
    def __init__(self, direction: str) -> None:
        self._direction = direction

    @property
    def direction(self) -> str:
        return self._direction
