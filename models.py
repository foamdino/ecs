
from dataclasses import dataclass
from itertools import count

entity_count = count(start=1)

class World:
    """Holds the entire state
       * systems registered
       * catalogue of entities: dictionary of component_types -> entity_list
       * dictionary of entities (k) with the component data (v)
    """
    def __init__(self):
        self.systems = {}
        self.catalogue = {}
        self.entities = {}

    def create_entity(self, *components):
        e = next(entity_count)

        # store the entity and associated list of components
        self.entities[e] = components

        # for each component associated with this entity
        # create a dict for the component (if it's the first time we've seen that component type)
        # essentially we build a catalogue
        for c in components:
            if self.catalogue.get(type(c)) is None:
                self.catalogue[type(c)] = []

            # register this entity into the list associated with this component
            c_list = self.catalogue.get(type(c))
            c_list.append(e)

        return e


    def remove_entity(self, entity):
        """Checks the catalogue of dictionaries and removes the entity from each one"""
        for k,v in self.catalogue.items():
            if entity in v:
                self.catalogue[k].remove(entity)

        # finally delete entity from entities
        del self.entities


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


    def view_entities(self):
        print(f"Entities {self.entities}")
        for k,v in self.entities.items():
            print(f"{k} -> {v}")


    def register_system(self, system):
        """Registers a system with the world - maybe move this to global later?"""
        self.systems[type(system)] = system


    def unregister_system(self, system):
        """Unregister a system"""
        del self.systems[type(system)]
      

    def query(self, *component_types):
        matched_entities = []
        # get the first list of entities matching the first component
        print(f"components[0]: {component_types[0]}")
        entities = self.catalogue[component_types[0]]

        # simple case - only one component so everything in this list 'matches'
        if len(component_types) == 1:
            matched_entities = entities

        else:
            # now for each of the entities in the first list - match with each subsequent list
            for e in entities:
                print(f"looking up for {e}")
                for c in component_types[1:]:
                    print(f"using {c} to lookup")
                    if c in self.catalogue:
                        if e in self.catalogue[c]:
                            matched_entities.append(e)
                    else:
                        print(f"{c} not found in catalogue")


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
        print("processing cart system...")
        to_process = world.query(AddToCart)
        for e in to_process:
            comps = world.entities[e]
            for c in comps:
                if type(c) == AddToCart:
                    print(f"found: {e}, adding {c.qty} of {c.product_id} to shopping cart")



class AddToCart(Component):
    product_id: str
    qty: int

    def __init__(self, product_id="", qty=-1):
        self.product_id = product_id
        self.qty = qty

@dataclass
class RemoveFromCart(Component):
    product_id: str
    qty: int

@dataclass
class ApplySpecialOffer(Component):
    message: str

    def __init__(self, message):
        self.message = message
