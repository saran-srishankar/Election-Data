from elections import Election, Jurisdiction
from datetime import date

def test_init() -> None:
    """Test function for Election.__init__.
    Testing to see whether it is initialized properly."""
    e = Election(date(2000, 3, 25))
    assert e._d == date(2000, 3, 25)
    assert e._ridings == []
    assert e._parties == []
    assert e._results == {}

def test_ridings_recorded() -> None:
    """Test function for Election.ridings_recorded
    Testing to see whether the object returned is different from the instance
    attributes of Election"""
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 5)
    assert e.ridings_recorded() is not e._ridings

def test_update_results1() -> None:
    """Test function for Election.update_results
    Testing to see whether the function alters the attributes of the Election
    object correctly.
    """
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 10)
    assert e._ridings == ['r1']
    assert e._parties == ['ndp']
    assert e._results == {'r1': {'ndp': 10}}
    e.update_results('r1', 'ndp', 11)
    assert e._ridings == ['r1']
    assert e._parties == ['ndp']
    assert e._results == {'r1': {'ndp': 21}}
    e.update_results('r2', 'pc', 100)
    assert e._ridings == ['r1', 'r2']
    assert e._parties == ['ndp', 'pc']
    assert e._results == {'r1': {'ndp': 21}, 'r2': {'pc': 100}}

def test_update_results2() -> None:
    """Test function for Election.update_results
    Testing to see whether the function alters the attributes of the Election
    object correctly.
    """
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'Green', 4)
    assert e._ridings == ['r1']
    assert e._parties == ['Green']
    assert e._results == {'r1': {'Green': 4}}
    e.update_results('r1', 'Conservative', 90)
    assert e._ridings == ['r1']
    assert e._parties == ['Green', 'Conservative']
    assert e._results == {'r1': {'Green': 4, 'Conservative': 90}}
    e.update_results('r1', 'NDP', 34)
    assert e._ridings == ['r1']
    assert e._parties == ['Green', 'Conservative', 'NDP']
    assert e._results == {'r1': {'Green': 4, 'Conservative': 90, 'NDP': 34}}

def test_read_results() -> None:
    """Test function for Election.read_results.
    Will test the function on brampton-centre.csv found in data folder of a0"""
    file = open('brampton-centre.csv')
    e = Election(date(2000, 3, 25))
    e.read_results(file)
    file.close()
    assert e._ridings == ['Brampton Centre']
    assert e._parties == ['Green Party', 'Conservative', 'NDP-New Democratic Party']
    assert e._results == {'Brampton Centre': {'Green Party': 4, 'Conservative': 90, 'NDP-New Democratic Party': 34}}

def test_riding_winners() -> None:
    """Test function for Election.riding_winners.
    Will test the function to see if it returns multi-length list for a riding
    with ties."""
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 100)
    e.update_results('r1', 'pc', 200)
    e.update_results('r1', 'ndp', 100)
    assert e.riding_winners('r1') == ['ndp', 'pc'] or \
        e.riding_winners('r1') == ['pc', 'ndp']


def test_party_seats() -> None:
    """Test function for Election.party_seats.
    Will test against the case that there is a tie in a riding and so no one
    wins the riding."""
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 1)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 1)
    e.update_results('r1', 'green', 1)
    e.update_results('r2', 'ndp', 5)
    e.update_results('r2', 'lib', 1)
    e.update_results('r2', 'lib', 2)
    e.update_results('r2', 'pc', 3)
    e.update_results('r2', 'green', 4)
    assert e.party_seats() == {'ndp': 1, 'lib': 0, 'pc': 0, 'green': 0}

def test_election_winners() -> None:
    """Test function for Election.election_winners.
    Will test against the case that there are ties in the number of seats won
    by multiple parties."""
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 1)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 1)
    e.update_results('r1', 'green', 1)
    e.update_results('r2', 'ndp', 2)
    e.update_results('r2', 'ndp', 3)
    e.update_results('r2', 'lib', 4)
    e.update_results('r2', 'pc', 4)
    e.update_results('r2', 'green', 4)
    e.update_results('r3', 'ndp', 4)
    e.update_results('r3', 'lib', 5)
    e.update_results('r3', 'pc', 4)
    e.update_results('r3', 'green', 4)
    e.update_results('r4', 'ndp', 4)
    e.update_results('r4', 'lib', 4)
    e.update_results('r4', 'pc', 5)
    e.update_results('r4', 'green', 4)
    assert e.election_winners() == ['ndp', 'lib', 'pc']

def test_election_winners2() -> None:
    """Test function for Election.election_winners.
    Will test against the case that there are no ties in the number of seats
    won."""
    e = Election(date(2000, 3, 25))
    e.update_results('r1', 'ndp', 2)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 1)
    e.update_results('r1', 'green', 1)
    e.update_results('r2', 'ndp', 2)
    e.update_results('r2', 'ndp', 3)
    e.update_results('r2', 'lib', 4)
    e.update_results('r2', 'pc', 4)
    e.update_results('r2', 'green', 4)
    e.update_results('r3', 'ndp', 4)
    e.update_results('r3', 'lib', 5)
    e.update_results('r3', 'pc', 4)
    e.update_results('r3', 'green', 4)
    e.update_results('r4', 'ndp', 4)
    e.update_results('r4', 'lib', 4)
    e.update_results('r4', 'pc', 5)
    e.update_results('r4', 'green', 4)
    assert e.election_winners() == ['ndp']


def test_read_results() -> None:
    """Test function for Jurisdiction.read_results.
    Will test basic functionality of read_results."""
    country = Jurisdiction('Canada')
    input_stream = open('brampton-centre.csv')
    d = date(2000, 3, 25)
    country.read_results(2000, 3, 25, input_stream)
    input_stream.close()

    assert country._elections[d]._d == d
    assert country._elections[d]._ridings == ['Brampton Centre']
    assert country._elections[d]._parties == ['Green Party',
                                               'Marxist-Leninist',
                                               'Conservative',
                                               'NDP-New Democratic Party']
    assert country._elections[d]._results == {'Brampton Centre':
                                                  {'Green Party': 4,
                                                   'Marxist-Leninist': 10,
                                                   'Conservative': 90,
                                                   'NDP-New Democratic Party':
                                                       34}}


def test_riding_changes() -> None:
    """Test function for Jurisdiction.riding_changes.
    Will test under the case that a jurisdiction has more than 2 elections, so
    we are expecting at least 2 tuples in the return statement of
    Jurisdiction.riding_changes"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 1)
    e1.update_results('r1', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    j._elections[date(2000, 2, 8)] = e1
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 1)
    e2.update_results('r3', 'pc', 1)
    j._elections[date(2004, 5, 16)] = e2
    e3 = Election(date(2007, 3, 25))
    e3.update_results('r2', 'ndp', 1)
    e3.update_results('r4', 'pc', 1)
    e3.update_results('r5', 'ndp', 1)
    j._elections[date(2007, 3,25)] = e3
    assert j.riding_changes() == [({'r2'}, {'r3'}), ({'r1', 'r3'},
                                                     {'r2', 'r4', 'r5'})]

def test_small_data() -> None:
    """Testing to see whether my program works, using the data of small_data.csv
    found in the data folder of a0."""
    data = open('data/small_data.csv')
    j = Jurisdiction('Canada')
    j.read_results(2000, 3, 25, data)
    data.close()
    assert j._elections[date(2000, 3, 25)].popular_vote() == \
           {"Liberal": 2940, "Green Party": 76, "Conservative": 773,
            "NDP-New Democratic Party": 293}

if __name__ == '__main__':
    import pytest
    pytest.main(['elections test.py'])
