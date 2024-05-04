import matplotlib.pyplot as plt 
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--variant', type=str, default='undefined')
args = parser.parse_args()

fedavg_path = "logs\experiment-"+args.variant+"-fedavg"
fedprox_path = "logs\experiment-"+args.variant+"-fedprox"

df_avg = pd.read_csv(fedavg_path)
df_prox = pd.read_csv(fedprox_path)


color = plt.get_cmap('Paired')
plt.plot(df_avg.idx, df_avg.te_acc, color=color(0))
plt.plot(df_prox.idx, df_prox.te_acc, "--", color=color(1))
plt.plot(df_avg.idx, df_avg.te_gmean, color=color(8))
plt.plot(df_prox.idx, df_prox.te_gmean, "--", color=color(9))
plt.xlabel('Communication round')
plt.ylabel('Global Model Test accuracy')
plt.title("Distribution variant: "+args.variant)
pos = 29
idx = len(df_avg.te_acc) - 1
buf = 0.005
plt.text(pos, df_avg.te_acc[idx] + buf, round(df_avg.te_acc[idx], 3), ha = 'center')
plt.text(pos, df_avg.te_gmean[idx] + buf, round(df_avg.te_gmean[idx], 3), ha = 'center')
plt.text(pos, df_prox.te_acc[idx] + buf, round(df_prox.te_acc[idx], 3), ha = 'center')
plt.text(pos, df_prox.te_gmean[idx] + buf, round(df_prox.te_gmean[idx], 3), ha = 'center')
plt.legend(['FedAvg acc', 'FedProx acc', 'FedAvg gmean', 'FedProx gmean'])

# save the figure
plt.savefig("figures/plot-"+args.variant+".png", dpi=300, bbox_inches='tight')
# plt.show()