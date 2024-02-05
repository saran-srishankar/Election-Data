"""CSC148 Assignment 0: Starter code

=== CSC148 Winter 2022 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for Assignment 0.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) University of Toronto
"""
from datetime import date
from typing import Dict, Tuple, List, Set, Optional, TextIO

# Constants that can be used throughout this module.
# Column numbers where various values can be found in the csv files containing
# election results.
RIDING = 1
PARTY = 13
VOTES = 17


# Helper functions
def clean_line(line: str) -> List[str]:
    """Given a line of data from csv file on elections, returns a list of str
    of length 18 where each value in the list is stripped and does not contain
    quotation marks"""
    # Creates a list of the entries from line
    lst = line.split(sep=',')

    # Strips the entries in lst
    for i in range(len(lst)):
        lst[i] = lst[i].strip()

    # Remove quotes from each entry
    remove_quotes(lst)

    return lst


def remove_quotes(lst: List[str]) -> None:
    """Mutates given lst, by making each value of the lst has all quotation
    characters removed.
    """
    for i in range(len(lst)):
        if '"' in lst[i]:
            lst[i] = lst[i][1:-1]


class Election:
    """Data for a single election in a parliamentary democracy.

    === Private Attributes ===
    _d: the date of this election.
    _ridings: all ridings for which any votes have been recorded in this
        election.
    _parties: all parties for which any votes have been recorded in this
        election.
    _results: the vote counts for this election.  Each key is the name of a
        riding, and its value is a dictionary of results for that one riding.
        Each of its keys, in turn, is the name of a party, and the associated
        value is the number of votes earned by that party in that riding.
            A party only appears in the dictionary for a riding if that party
        has had at least one vote recorded in that riding.

    === Representation Invariants ==
    - For all strings s, s in self._ridings iff s in self._results
    - For all strings s, s in self._parties iff s in self._results[r] for some r
    - All recorded vote counts are greater than 0. That is,
      for every key (riding, results) in self._results,
          for every (party, votes) in results,
              votes > 0

    === Sample Usage ===
    >>> e = Election(date(2000, 2, 8))
    >>> e.update_results('r1', 'ndp', 1234)
    >>> e.update_results('r1', 'lib', 1345)
    >>> e.update_results('r1', 'pc', 1456)
    >>> e.riding_winners('r1')
    ['pc']
    >>> e.update_results('r2', 'pc', 1)
    >>> e.popular_vote() == {'ndp': 1234, 'lib': 1345, 'pc': 1457}
    True
    >>> e.results_for('r1', 'lib')
    1345
    >>> e.party_seats() == {'ndp': 0, 'lib': 0, 'pc': 2}
    True
    """
    _d: date
    _ridings: List[str]
    _parties: List[str]
    _results: Dict[str, Dict[str, int]]

    def __init__(self, d: date) -> None:
        """Initialize a new election on date d and with no ridings, parties,
        or votes recorded so far.

        >>> e = Election(date(2000, 2, 8))
        >>> e._d
        datetime.date(2000, 2, 8)
        """
        self._d = d
        self._ridings = []
        self._parties = []
        self._results = {}

    def ridings_recorded(self) -> List[str]:
        """Return the ridings in which votes have been recorded in this
         election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.ridings_recorded()
        ['r1']
        >>> e.update_results('r2', 'ndp', 1)
        >>> e.ridings_recorded()
        ['r1', 'r2']
        """
        # Make a copy of the mutable attribute self._ridings
        ridings_copy = self._ridings.copy()
        return ridings_copy

    def update_results(self, riding: str, party: str, votes: int) -> None:
        """Update this election to reflect that in <riding>, <party> received
        <votes> additional votes.

        <riding> may or may not already have some votes recorded in this
        election.  <party> may or may not already have some votes recorded in
        this riding in this election.

        Precondition: votes >= 1

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.results_for('r1', 'ndp')
        1
        >>> e.update_results('r1', 'ndp', 1000)
        >>> e.results_for('r1', 'ndp')
        1001
        """

        # Adding riding to self._ridings if it's not there
        if riding not in self._ridings:
            self._ridings.append(riding)

        # Adding party to self._parties if it's not there
        if party not in self._parties:
            self._parties.append(party)

        # Deal with the case where riding is not in self._results or riding
        # is and party is not in self._results[riding]
        if riding not in self._results:
            self._results[riding] = {party: votes}
        elif party not in self._results[riding]:
            self._results[riding][party] = votes

        # We can now assume riding is in self._results and party is in
        # self._results[riding]
        else:
            self._results[riding][party] += votes

    def read_results(self, input_stream: TextIO) -> None:
        """Update this election with the results in input_stream.

        Precondition: input_stream is an open csv file, in the format defined
        in the A0 handout.
        """
        # Skips header line of input_stream
        input_stream.readline()

        # Analyze each line of data
        for line in input_stream:
            # Call private helper function to split the line's data into a list
            # and then remove the unnecessary quotations
            list_of_entries = clean_line(line)

            # Assign values to riding, party and vote
            riding = list_of_entries[RIDING]
            party = list_of_entries[PARTY]
            votes = int(list_of_entries[VOTES])

            # If vote > 0, then add this result to the election.
            if votes > 0:
                self.update_results(riding, party, votes)

    def results_for(self, riding: str, party: str) -> Optional[int]:
        """Return the number of votes received in <riding> by <party> in
        this election.

        Return None if <riding> does not have any votes recorded in this
        election, or if it does, but <party> does not have any votes recorded
        in this riding in this election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1234)
        >>> e.update_results('r1', 'lib', 1345)
        >>> e.update_results('r1', 'pc', 1456)
        >>> e.update_results('r2', 'pc', 1)
        >>> e.results_for('r1', 'pc')
        1456
        >>> e.results_for('r2', 'pc')
        1
        """
        if riding not in self._ridings or party not in self._results[riding]:
            return None
        else:
            # Note: self._results[riding][party] is immutable so it's ok to
            # return
            return self._results[riding][party]

    def riding_winners(self, riding: str) -> List[str]:
        """Return the winners, in <riding>, of this election.

        The winner is the party or parties that received the most votes in
        total. (There may have been a tie.) The return value is a list so
        that, in the case of ties, we can return a list of election_winners.
        If there is no tie, the length of the returned list is 1.

        Precondition: <riding> has at least 1 vote recorded in this election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.riding_winners('r1')
        ['pc']
        """
        # winners will be our return list, consisting of all winning parties
        winners = []
        # winning_vote will measure the largest vote in riding
        winning_vote = 0

        for party in self._results[riding]:
            if self._results[riding][party] > winning_vote:
                winning_vote = self._results[riding][party]
                winners = [party]
            elif self._results[riding][party] == winning_vote:
                winners.append(party)

        return winners

    def popular_vote(self) -> Dict[str, int]:
        """For each party, return the total number of votes it earned, across
        all ridings, in this election.

        Include only parties that have at least one vote recorded in at least
        one riding.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'pc', 4)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.popular_vote() == {'ndp': 8, 'lib': 7, 'pc': 7, 'green': 6}
        True
        """
        # Initialize return dictionary
        d = {}
        for party in self._parties:
            d[party] = 0

        for riding in self._ridings:
            for party in self._results[riding]:
                d[party] += self._results[riding][party]

        return d

    def party_seats(self) -> Dict[str, int]:
        """For each party, return the number of ridings that it won in this
        election.

        Include only parties that have at least one vote recorded in at least
        one riding.  If there was a tie in a riding, the riding doesn't
        contribute to the seat count for any of the parties that were tied in
        that riding.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'pc', 4)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.party_seats() == {'pc': 1, 'ndp': 1, 'lib': 0, 'green': 0}
        True
        """
        d = {}
        for party in self._parties:
            d[party] = 0

        for riding in self._ridings:
            if len(self.riding_winners(riding)) == 1:
                riding_winner = self.riding_winners(riding)[0]
                d[riding_winner] += 1

        return d

    def election_winners(self) -> List[str]:
        """Return the party (or parties, in the case of a tie) that won the
        most seats in this election.

        If no votes have been recorded in any riding in this election,
        return the empty list.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.update_results('r2', 'pc', 8)
        >>> e.election_winners()
        ['pc']
        """
        lst = []
        party_seats = self.party_seats()

        max_seats_won = 0
        for party in party_seats:
            if party_seats[party] > max_seats_won:
                max_seats_won = party_seats[party]
                lst = [party]
            elif party_seats[party] == max_seats_won:
                lst.append(party)

        return lst


class Jurisdiction:
    """The election history for a jurisdiction that is a parliamentary
    democracy.

    === Private Attributes ===
    _name: the name of this jurisdiction.
    _elections: the election history for this jurisdiction.  Each key is a date,
        and its value holds the results of an election that was held on that
        date.

    === Representation Invariants ==
    None.

    === Sample Usage ===
    # See the method docstrings for sample usage.
    """
    _name: str
    _elections: Dict[date, Election]

    def __init__(self, name: str) -> None:
        """Initialize this jurisdiction, with no elections so far.

        >>> country = Jurisdiction('Canada')
        >>> country._name
        'Canada'
        >>> country._elections
        {}
        """
        self._name = name
        self._elections = {}

    def read_results(self, year: int, month: int, day: int,
                     input_stream: TextIO) -> None:
        """Read and record results for an election in this jurisdiction.

        If there are already some results stored for an election on this date,
        add to them.

        Precondition: input_stream is an open csv file, in the format defined
        in the A0 handout.
        """
        date_of_election = date(year, month, day)

        # Add an election object to the dictionary with key date_of_election
        # if an election does not already exist on that date
        if date_of_election not in self._elections:
            self._elections[date_of_election] = Election(date_of_election)

        # Now read the results to that election on that date.
        self._elections[date_of_election].read_results(input_stream)

    def party_wins(self, party: str) -> List[date]:
        """Return a list of all dates on which <party> won an election in this
        jurisdiction.

        If the party tied for most seats in an election, do include that date
        in the result.

        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 2)
        >>> e1.update_results('r1', 'pc', 3)
        >>> e1.update_results('r2', 'lib', 10)
        >>> e1.update_results('r2', 'pc', 20)
        >>> e1.update_results('r3', 'ndp', 200)
        >>> e1.update_results('r3', 'pc', 100)
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 10)
        >>> e2.update_results('r1', 'lib', 20)
        >>> e2.update_results('r2', 'lib', 50)
        >>> e2.update_results('r2', 'pc', 5)
        >>> e3 = Election(date(2008, 6, 1))
        >>> e3.update_results('r1', 'ndp', 101)
        >>> e3.update_results('r1', 'lib', 102)
        >>> e3.update_results('r2', 'ndp', 1001)
        >>> e3.update_results('r2', 'lib', 1002)
        >>> j = Jurisdiction('Canada')
        >>> j._elections[date(2000, 2, 8)] = e1
        >>> j._elections[date(2003, 5, 16)] = e2
        >>> j._elections[date(2003, 6, 1)] = e3
        >>> j.party_wins('lib')
        [datetime.date(2003, 5, 16), datetime.date(2003, 6, 1)]
        """
        lst = []
        for d in self._elections:
            if party in self._elections[d].election_winners():
                lst.append(d)

        return lst

    def party_history(self, party: str) -> Dict[date, float]:
        """Return this party's percentage of the popular vote in each election
        in this jurisdiction's history.

        Each key in the result is a date on which there was an election in
        this jurisdiction.  Its value is the percentage of the popular vote
        earned by party in that election.

        >>> j = Jurisdiction('Canada')
        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 2)
        >>> e1.update_results('r1', 'pc', 3)
        >>> e1.update_results('r2', 'pc', 4)
        >>> e1.update_results('r2', 'lib', 5)
        >>> e1.update_results('r2', 'green', 6)
        >>> e1.update_results('r2', 'ndp', 7)
        >>> e1.popular_vote() == {'ndp': 8, 'lib': 7, 'pc': 7, 'green': 6}
        True
        >>> j._elections[date(2000, 2, 8)] = e1
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 40)
        >>> e2.update_results('r1', 'lib', 5)
        >>> e2.update_results('r2', 'lib', 10)
        >>> e2.update_results('r2', 'pc', 20)
        >>> e2.popular_vote() == {'ndp': 40, 'lib': 15, 'pc': 20}
        True
        >>> j._elections[date(2004, 5, 16)] = e2
        >>> j.party_history('lib') == {date(2000, 2, 8): 0.25, \
        date(2004, 5, 16): 0.2}
        True
        """
        dic = {}  # Create return dictionary

        # Parse through each date in this jurisdiction's history of elections.
        # I will then calculate the party's popular vote percentage for each
        # date and add the key-value pair to dic
        for d in self._elections:
            pop_vote = self._elections[d].popular_vote()
            total_votes = 0
            for _party in pop_vote:
                total_votes += pop_vote[_party]
            # It's possible no data is in self._elections[d], so treat the case
            # where total_votes == 0 as a separate case.  Also, we can add in
            # the case where party is not in pop_vote.
            if total_votes == 0 or party not in pop_vote:
                dic[d] = 0.0
            else:
                dic[d] = pop_vote[party] / total_votes

        return dic

    def riding_changes(self) -> List[Tuple[Set[str], Set[str]]]:
        """Return the changes in ridings across elections in this jurisdiction.

        Include a tuple for each adjacent pair of elections, in order by date.
        The tuple should contain, first, a set of ridings that were removed
        between these two elections, and then a set of ridings that were added.

        Precondition: There is at least one election recorded for this
        jurisdiction.

        >>> j = Jurisdiction('Canada')
        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 1)
        >>> e1.update_results('r1', 'pc', 1)
        >>> e1.update_results('r2', 'pc', 1)
        >>> e1.update_results('r2', 'lib', 1)
        >>> e1.update_results('r2', 'green', 1)
        >>> e1.update_results('r2', 'ndp', 1)
        >>> j._elections[date(2000, 2, 8)] = e1
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 1)
        >>> e2.update_results('r3', 'pc', 1)
        >>> j._elections[date(2004, 5, 16)] = e2
        >>> j.riding_changes() == [({'r2'}, {'r3'})]
        True
        """
        lst = []
        if len(self._elections) == 1:
            # This covers the case where jurisdiction only has 1 election date
            return lst
        else:
            # Now we can assume jurisdiction has at least 2 election dates

            # This gets us a list of all the keys (so dates of elections in this
            # case) of self._elections.
            election_dates = list(self._elections)

            # Sort the election_dates by date in increasing order
            election_dates.sort()

            # Since we need to count every 2 consecutive election dates, we
            # will parse through from the first index to the 2nd last index of
            # election_dates
            for i in range(len(election_dates) - 1):
                ridings_start = set(
                    self._elections[election_dates[i]].ridings_recorded())
                ridings_end = set(
                    self._elections[election_dates[i + 1]].ridings_recorded())
                lst.append((ridings_start - ridings_end, ridings_end
                            - ridings_start))

        return lst


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['Election.read_results', 'Jurisdiction.read_results'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'datetime', 'typing'
        ],
        'max-attributes': 15
    })

    import doctest
    doctest.testmod()

    # An example of reading election results from a file.
    c = Jurisdiction('Canada')
    with open('data/parkdale-highpark.csv') as file:
        c.read_results(2015, 2, 3, file)
    with open('data/nunavut.csv') as file:
        c.read_results(2015, 2, 3, file)
    with open('data/labrador.csv') as file:
        c.read_results(2015, 2, 3, file)
    # An example of using that data to calculate some things.
    print(c.party_history('Liberal'))
    print(c.party_history('Conservative'))
    print(c.party_history('Green Party'))
    print(c.party_history('NDP-New Democratic Party'))
