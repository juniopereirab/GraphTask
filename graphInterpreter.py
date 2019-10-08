# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt

dados = open("testeDep.csv").readlines()
del dados[0]

for i in range(len(dados)):
    dados[i] = dados[i].split(";")

id_vot = {}
voto = {}
orient_part = {}
orient_gov = {}

votacao = []
partido = []
governo = []

category_names = ['Não', 'Abstenção', 'Ausente', 'Obstrução', 'Sim']
category_names2 = ['Não', 'Obstrução', 'Liberado', 'Sim']

for i in range(len(dados)):
    for j in range(len(dados[i])):
        dados[i][j] = dados[i][j].replace('\n', '')

# id_vot = 1
# voto = 12
# voto_part = 13
# voto _gov = 14

for i in dados:
    id_vot[i[0]] = 0

for j in category_names:
    voto[j] = 0

for j in category_names2:
    orient_part[j] = 0

for j in category_names2:
    orient_gov[j] = 0

for i in dados:
    id_vot[i[0]] += 1

tam = len(id_vot)
tam1 = len(dados)

num_votos = int(tam1/tam)
cont = 0

for i,j in enumerate(dados):
    if i % num_votos == 0 and i != 0:
        votacao.append(voto)
        voto = {'Sim': 0, 'Não': 0, 'Abstenção': 0, 'Obstrução':0, 'Ausente':0 }
        voto[j[11]] += 1
    else:
        voto[j[11]] += 1

votacao.append(voto)

for i,j in enumerate(dados):
    if i % num_votos == 0 and i != 0:
        partido.append(orient_part)
        orient_part = {'Sim': 0, 'Não': 0, 'Obstrução':0, 'Liberado':0 }
        orient_part[j[12]] += 1
    else:
        orient_part[j[12]] += 1

partido.append(orient_part)

for i,j in enumerate(dados):
    if i % num_votos == 0 and i != 0:
        governo.append(orient_gov)
        orient_gov = {'Sim': 0, 'Não': 0, 'Obstrução':0, 'Liberado':0 }
        orient_gov[j[13]] += 1
    else:
        orient_gov[j[13]] += 1

governo.append(orient_gov)

votaGrafico = {}
partGrafico = {}
goveGrafico = {}

for i in id_vot.keys():
    votaGrafico[i] = []

for i in id_vot.keys():
    partGrafico[i] = []

for i in id_vot.keys():
    goveGrafico[i] = []

for i, j in zip(id_vot.keys(), votacao):
    votaGrafico[i] = list(j.values())

for i, j in zip(id_vot.keys(), partido):
    partGrafico[i] = list(j.values())

for i, j in zip(id_vot.keys(), governo):
    goveGrafico[i] = list(j.values())


def survey(results, category_names, nome):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(int(c)), ha = 'center', va = 'center', color = text_color)
            ax.legend(ncol = len(category_names), bbox_to_anchor=(0,1), loc = 'lower left', fontsize = 'small')

    plt.savefig(nome, dpi=300)
    return fig, ax


survey(votaGrafico, category_names, "./GraphProject/assets/images/votaGrafico.png")
survey(partGrafico, category_names2, "./GraphProject/assets/images/partGrafico.png")
survey(goveGrafico, category_names2, "./GraphProject/assets/images/goveGrafico.png")
