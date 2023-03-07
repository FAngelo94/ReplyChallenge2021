from solution import Solution
files = ['data_scenarios_a_example.in', 'data_scenarios_b_mumbai.in', 'data_scenarios_c_metropolis.in', 'data_scenarios_d_polynesia.in', 'data_scenarios_e_sanfrancisco.in', 'data_scenarios_f_tokyo.in']

""" for i in files:
    print('file: ', i)
    s = Solution.load_problem(i)
    s.print()
    s.order_buildings()
    s.order_antennas()
    s.print() """

for i in files[0:2]:
    print('file: ', i)
    s = Solution.load_problem(i)
    s.order_buildings()
    s.order_antennas()
    if(i == 'data_scenarios_c_metropolis.in'):
        s.find_solution_antenna_in_buildings()
    else:
        s.find_solution_antenna_in_buildings()
        #s.find_solution_2()
    s.score()
    s.dump()

"""
s = Solution.load_problem(files[1])
s.find_solution()
 s.Sx[0] = 12
s.Sy[0] = 3
s.Sx[1] = 7
s.Sy[1] = 6
s.Sx[2] = 11
s.Sy[2] = 7
s.Sx[3] = 2
s.Sy[3] = 4 
s.score()
s.dump()
"""