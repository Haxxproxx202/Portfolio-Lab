import pytest

TEST_INSTITUTION_DATA = [
        ('NewName', 'Whatever', 1),
        ('NewName2', 'Whatever2', 2),
        ('NewName3', 'Whatever3', 3),
        ('NewName4', 'Whatever4', 2),
        ('NewName5', 'Whatever5', 1),
    ]


@pytest.mark.parametrize(
    "name, description, type", TEST_INSTITUTION_DATA
)
def test_institution_instance(
        db, institution_factory, name, description, type
):
    test = institution_factory(
        name=name,
        description=description,
        type=type,
    )

    assert isinstance(type, int)
    assert isinstance(name, str)
    # with pytest.raises(Exception):
    #     isinstance(type, str)



