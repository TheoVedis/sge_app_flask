import pandas as pd
import random

data: pd.DataFrame = pd.read_csv(
    r"C:\Users\TVedis\Documents\STAGE-SGE\app\code_flask\base_clients.csv",
    sep=",",
    dtype=str,
)

letter = [chr(i) for i in range(91 - 26, 91)]


def random_char():
    return letter[int(random.random() * 26)]


def gen_password(ref: str, nom: str) -> str:
    mdp = "".join([ref] + [i[:1] for i in nom.split(" ") if i.isalpha()])[:6]

    while len(mdp) < 6:
        mdp += random_char()

    return mdp


for i, row in data.iterrows():
    data.at[i, "MDP"] = gen_password(str(row["REF"]), str(row["NOM"]))

data.to_csv(
    r"C:\Users\TVedis\Documents\STAGE-SGE\app\code_flask\base_clients.csv", index=False
)

print(data)