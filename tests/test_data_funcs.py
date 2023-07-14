from data.funcs import get_team, iso_to_dt


def test_get_team() -> None:

    assert get_team("Cleveland Guardians") == "CLE" and get_team("San Francisco Giants") == "SF"

def test_iso_to_dt() -> None:

    dt_object = iso_to_dt("2023-07-14T15:42:39Z")
    assert (dt_object.tzname(), str(dt_object.date()), str(dt_object.time())) == ("UTC", "2023-07-14", "15:42:39")
