"""
Test the Look Ahead Routine algorithm for course allocation.

Programmers: Hadar Bitan, Yuval Ben-Simhon
Date: 19.5.2024
We used chat-GPT and our friends from the university for ideas of cases.
"""

import pytest
from fairpyx import Instance
from fairpyx.algorithms.Optimization_Matching.FaStGen import LookAheadRoutine

def test_look_ahead_routine_basic_case():
    """
    Basic test case for the Look Ahead Routine algorithm.
    """
    # Define the instance
    S = ["s1", "s2", "s3", "s4", "s5"]
    C = ["c1", "c2", "c3", "c4"]
    V = {       #the colleges valuations
        "c1" : {"s1":50,"s2":23,"s3":21,"s4":13,"s5":10}, 
        "c2" : {"s1":45,"s2":40,"s3":32,"s4":29,"s5":26}, 
        "c3" : {"s1":90,"s2":79,"s3":60,"s4":35,"s5":28}, 
        "c4" : {"s1":80,"s2":48,"s3":36,"s4":29,"s5":15}
    }                               
    U = {       #the students valuations
        "s1" : {"c1":16,"c2":10,"c3":6,"c4":5}, 
        "s2" : {"c1":36,"c2":20,"c3":10,"c4":1}, 
        "s3" : {"c1":29,"c2":24,"c3":12,"c4":10}, 
        "s4" : {"c1":41,"c2":24,"c3":5,"c4":3}, 
        "s5" : {"c1":36,"c2":19,"c3":9,"c4":6}
    }                              
    I = (S, C, U ,V)
    match = {
        "c1" : ["s1","s2"], 
        "c2" : ["s3"], 
        "c3" : ["s4"], 
        "c4" : ["s5"]
    }
    down = 4
    LowerFix = [4]
    UpperFix = [1]
    SoftFix = []


    # Run the Look Ahead Routine algorithm
    new_match, new_LowerFix, new_UpperFix, new_SoftFix = LookAheadRoutine(I, match, down, LowerFix, UpperFix, SoftFix)

    # Define the expected output
    expected_new_match = {"c1": ["s1", "s2"], "c2": ["s3"], "c3" : ["s4"], "c4" : ["s5"]}
    expected_new_LowerFix = [4]
    expected_new_UpperFix = [1, 4]
    expected_new_SoftFix = []

    # Assert the result
    assert new_match == expected_new_match, "Look Ahead Routine algorithm basic case failed"
    assert new_LowerFix == expected_new_LowerFix, "Look Ahead Routine algorithm basic case failed on LowerFix"
    assert new_UpperFix == expected_new_UpperFix, "Look Ahead Routine algorithm basic case failed on UpperFix"
    assert new_SoftFix == expected_new_SoftFix, "Look Ahead Routine algorithm basic case failed on SoftFix"

def test_look_ahead_routine_edge_cases():
    """
    Test edge cases for the Look Ahead Routine algorithm.
    """
    # Edge case 1: Empty input
    I_empty = (set(), set(), {}, {})
    match_empty = {}
    down_empty = ""
    LowerFix_empty = []
    UpperFix_empty = []
    SoftFix_empty = []

    new_match_empty, new_LowerFix_empty, new_UpperFix_empty, new_SoftFix_empty = LookAheadRoutine(I_empty, match_empty, down_empty, LowerFix_empty, UpperFix_empty, SoftFix_empty)
    assert new_match_empty == {}, "Look Ahead Routine algorithm failed on empty input"
    assert new_LowerFix_empty == [], "Look Ahead Routine algorithm failed on empty input (LowerFix)"
    assert new_UpperFix_empty == [], "Look Ahead Routine algorithm failed on empty input (UpperFix)"
    assert new_SoftFix_empty == [], "Look Ahead Routine algorithm failed on empty input (SoftFix)"

    # Edge case 2: Single student and single course
    I_single = ({"s1"}, {"c1"}, {"s1": {"c1":100}}, {"c1": {"s1":80}})
    match_single = {"c1": ["s1"]}
    down_single = "c1"
    LowerFix_single = []
    UpperFix_single = []
    SoftFix_single = []

    new_match_single, new_LowerFix_single, new_UpperFix_single, new_SoftFix_single = LookAheadRoutine(I_single, match_single, down_single, LowerFix_single, UpperFix_single, SoftFix_single)
    assert new_match_single == {"c1": ["s1"]}, "Look Ahead Routine algorithm failed on single student and single course"
    assert new_LowerFix_single == [], "Look Ahead Routine algorithm failed on single student and single course (LowerFix)"
    assert new_UpperFix_single == [], "Look Ahead Routine algorithm failed on single student and single course (UpperFix)"
    assert new_SoftFix_single == [], "Look Ahead Routine algorithm failed on single student and single course (SoftFix)"

def test_look_ahead_routine_large_input():
    """
    Test the Look Ahead Routine algorithm on a large input.
    """
    # Define the instance with a large number of students and courses
    num_students = 100
    num_college = 50
    students = {f"s{i}" for i in range(1, num_students + 1)}
    colleges = {f"c{i}" for i in range(1, num_college + 1)}
    U = {student: list(colleges) for student in students}
    V = {course: list(students) for course in colleges}

    I_large = (students, colleges, U, V)
    match_large = {course: [] for course in colleges}
    down_large = "c1"
    LowerFix_large = []
    UpperFix_large = []
    SoftFix_large = []

    # Run the Look Ahead Routine algorithm
    new_match_large, new_LowerFix_large, new_UpperFix_large, new_SoftFix_large = LookAheadRoutine(I_large, match_large, down_large, LowerFix_large, UpperFix_large, SoftFix_large)

    # Add assertions
    # Ensure that all students are considered in the new matching
    assert all(student in {s for lst in new_match_large.values() for s in lst} for student in students), "Not all students are considered in the new matching"

    # Ensure no student is matched to more than one course
    all_students = [s for lst in new_match_large.values() for s in lst]
    assert len(all_students) == len(set(all_students)), "A student is matched to more than one course"

    # Ensure LowerFix, UpperFix, and SoftFix are updated correctly
    assert isinstance(new_LowerFix_large, list), "LowerFix is not a list"
    assert isinstance(new_UpperFix_large, list), "UpperFix is not a list"
    assert isinstance(new_SoftFix_large, list), "SoftFix is not a list"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
