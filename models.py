
from dataclasses import dataclass
from itertools import count

entity_count = count(start=1)

class World:
    """Holds the entire state
       * systems registered
       * catalogue of entities
    """
    def __init__(self):
        self.systems = {}
        self.catalogue = {}


    def create_entity(self, *components):
        e = next(entity_count)

        # for each component associated with this entity
        # create a dict for the component (if it's the first time we've seen that component type)
        # essentially we build a catalogue
        for c in components:
            if self.catalogue.get(c) is None:
                self.catalogue[c] = []

            # register this entity into the list associated with this component
            c_list = self.catalogue.get(c)
            c_list.append(e)

        return e

    def remove_entity(self, entity):
        """Checks the catalogue of dictionaries and removes the entity from each one"""
        for k,v in self.catalogue.items():
            if entity in v:
                self.catalogue[k].remove(entity)


    def entity_in_catalogue(self, entity):
        """Check if a given entity is contained in the catalogue"""
        for k,v in self.catalogue.items():
            if entity in v:
                return True

        return False


    def view_catalogue(self):
        """display the catalogue contents for debugging"""
        print(f"Systems {self.systems}")
        for k,v in self.catalogue.items():
            print(f"{k} -> {v}")


    def register_system(self, sysname, system):
        """Registers a system with the world - maybe move this to global later?"""
        self.systems[sysname] = system


    def unregister_system(self, sysname):
        """Unregister a system"""
        del self.systems[sysname]


    def query(self, *components):
        matched_entities = []
        # get the first list of entities matching the first component
        entities = self.catalogue[components[0]]

        # simple case - only one component so everything in this list 'matches'
        if len(components) == 1:
            matched_entities = entities

        else:
            # now for each of the entities in the first list - match with each subsequent list
            for e in entities:
                #print(f"looking up for {e}")
                for c in components[1:]:
                    if e in self.catalogue[c]:
                        matched_entities.append(e)

        return matched_entities


    def evolve(self):
        """call process method on every registered system"""
        for s in self.systems.values():
            s.process(self.world)



class Component:
    pass

class System:
    def process(world):
        pass

class CartSystem(System):
    """
    This system handles messages that mutate the state of the cart
    * AddToCart
    * RemoveFromCart
    * ApplySpecialOffer
    """

    def process(self, world):
        """
        Find all the entities with the components we care about: filter
        """
        to_process = world.query(AddToCart(), RemoveFromCart(), ApplySpecialOffer())

@dataclass(frozen=True)
class AddToCart(Component):
    pass

@dataclass(frozen=True)
class RemoveFromCart(Component):
    pass

@dataclass(frozen=True)
class ApplySpecialOffer(Component):
    pass
