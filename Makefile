setup:
	pipenv install

theory: compile_theory clean_theory

compile_theory:
	pdflatex -shell-escape src/tex/theory.tex

clean_theory:
	rm -f theory.aux theory.out texput.log

generate_test:
	pipenv run python3 src/py/generate_test.py --global-test > result/test.txt

run_exp_solution:
	pipenv run python3 src/py/exp_solver.py -p < result/test.txt > result/exp_res.txt

run_pol_solution:
	python3 src/py/pol_solver.py -p < result/test.txt > result/pol_res.txt

results:
	pipenv run python3 src/py/calc_results.py result/
