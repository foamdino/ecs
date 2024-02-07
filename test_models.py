from models import World, System, AddToCart, RemoveFromCart, ApplySpecialOffer, CartSystem

def test_create_entity():
    w = World()
    e = w.create_entity()
    # first entity will be id 1
    assert e == 1


def test_entity_in_catalogue():
    w = World()
    e = w.create_entity(AddToCart())

    assert w.entity_in_catalogue(e)


def test_remove_entity():
    w = World()
    e = w.create_entity(AddToCart())

    assert e != None
    assert w.entity_in_catalogue(e)

    w.remove_entity(e)
    assert not w.entity_in_catalogue(e)


def test_register_system():
    w = World()
    s = System()

    w.register_system("testsys", s)
    assert w.systems["testsys"] == s


def test_unregister_system():
    w = World()
    s = CartSystem()
    w.register_system("cartsys", s)

    assert w.systems.get("cartsys") == s

    w.unregister_system("cartsys")
    assert w.systems.get("cartsys") == None


def test_view_catalogue():
    w = World()

    w.create_entity(AddToCart())

    w.view_catalogue()


def test_get_entities_with_components():
    w = World()

    created_entity = w.create_entity(AddToCart())

    assert w.query(AddToCart()) == [created_entity]

    new_entity = w.create_entity(AddToCart(), ApplySpecialOffer())

    assert w.query(AddToCart(), ApplySpecialOffer()) == [new_entity]

    assert w.query(AddToCart()) != \
        w.query(AddToCart(), ApplySpecialOffer())


def test_process():
    w = World()
    e = w.create_entity(AddToCart())
    cs = CartSystem()

    cs.process(w)
