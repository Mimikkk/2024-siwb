 #!/bin/bash
rounds=30
parties=20
dataset=clinical

#test config
# rounds=20
# parties=3
# dataset=pima

variants=('small_preserved' 'small_random' 'average_preserved' 'average_random' 'large_preserved' 'large_random')
variants2=('small_random')
for variant in "${variants[@]}"
do
	py experiments.py --dataset=$dataset \
		--model=mlp \
		--device=cpu \
		--comm_round=$rounds \
		--n_parties=$parties \
		--partition=$variant \
		--alg=fedavg 

	py experiments.py --dataset=$dataset \
		--model=mlp \
		--device=cpu \
		--comm_round=$rounds \
		--n_parties=$parties \
		--partition=$variant \
		--alg=fedprox 

	py plots.py --variant=$variant
done