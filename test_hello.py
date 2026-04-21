from hello import hello_world

def test_list_exists():
    duties = hello_world()
    assert type(duties) == list