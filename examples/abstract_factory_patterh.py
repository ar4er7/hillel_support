from abc import ABC, abstractmethod


# Abstract products
class Chair(ABC):
    @abstractmethod
    def sit_on(self):
        pass


class Table(ABC):
    @abstractmethod
    def dine_on(self):
        pass


# Concrete products
class ModernChair(Chair):
    def sit_on(self):
        print("Sitting on a modern chair.")


class VictorianChair(Chair):
    def sit_on(self):
        print("Sitting on a Victorian chair.")


class ModernTable(Table):
    def dine_on(self):
        print("Dining on a modern table.")


class VictorianTable(Table):
    def dine_on(self):
        print("Dining on a Victorian table.")


# Abstract factory
class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_table(self) -> Table:
        pass


# Concrete factories
class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self):
        return ModernChair()

    def create_table(self):
        return ModernTable()


class VictorianFurnitureFactory(FurnitureFactory):
    def create_chair(self):
        return VictorianChair()

    def create_table(self):
        return VictorianTable()


def client_code(factory: FurnitureFactory):
    chair = factory.create_chair()
    table = factory.create_table()

    chair.sit_on()
    table.dine_on()


client_code(ModernFurnitureFactory())
