from Richi.solution import Solution, random_sol

s = Solution.load_problem("data_scenarios_a_example.in")
s.Scol[0] = 12
s.Srow[0] = 3
s.Scol[1] = 7
s.Srow[1] = 6
s.Scol[2] = 11
s.Srow[2] = 7
s.Scol[3] = 2
s.Srow[3] = 4

if __name__ == "__main__":
    problems = ["data_scenarios_a_example.in", "data_scenarios_b_mumbai.in", "data_scenarios_c_metropolis.in",
                "data_scenarios_d_polynesia.in", "data_scenarios_e_sanfrancisco.in", "data_scenarios_f_tokyo.in"]
    for problem in problems:
        s = Solution.load_problem(problem)
        print(f"problem loaded {problem}")
        random_sol(s)
        s.dump()

