from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import networkx as nx

def get_file_names():
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()

def set_prog(prog="dot"):
    path = r'C:\Program Files (x86)\Graphviz\bin' # bin directory of graphviz
    prog = os.path.join(path, prog) + '.exe'
    return prog


if __name__ == "__main__":

    # #get_file_names()
    # test_directory = Path(__file__).parent / 'dataset'
    # dataset_file = [test_directory/'1000_samples.csv']
    
    # nRowsRead = 5 # specify 'None' if want to read whole file
    
    # df1 = pd.read_csv(dataset_file[0], delimiter=',', nrows = nRowsRead)
    # df1.dataframeName = '1000_samples.csv'
    # #print(list(df1.columns))
    # df2 = df1['RecipeIngredientParts']
    
    # n = 0
    # for (columnName, columnData) in df2.iteritems():
    #     columnData = columnData.replace('c("','')
    #     columnData = columnData.replace('", "',',')
    #     columnData = columnData.replace('")','')
    #     columnData = list(columnData.split(","))
    #     df2.iloc[n] = columnData
    #     n = n+1

    # df1['RecipeIngredientParts'] = df2


    # G = nx.Graph()
    # G.add_nodes_from([(0, {"name_":"Biryani", "type_":"Recipe"}),
    #                 (1, {"name_":"Best Lemonade", "type_":"Recipe"})])
    
    # G.add_nodes_from([(2, {"name_":"blueberries", "type_":"Ingredient"}),
    #                 (3, {"name_":"granulated sugar", "type_":"Ingredient"}),
    #                 (4, {"name_":"vanilla yogurt", "type_":"Ingredient"}),
    #                 (5, {"name_":"lemon juice", "type_":"Ingredient"}),
    #                 (6, {"name_":"peppercorns", "type_":"Ingredient"})])

    # G.add_edges_from([(0,3),(0,4),(0,5),(1,4),(1,3),(1,6)])

    
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.axis('equal')
    # plt.show()


    # import dgl
    # import dglke
    # g = dgl.from_networkx(G)
    # #print(g.nodes())
    # #print(g.edges())

    # from dgl.data.utils import save_graphs
    # save_graphs("./data.bin", [g])

    # test_directory = Path(__file__).parent / 'dataset'
    # dataset_file = [test_directory/'relations.tsv']
    # df1 = pd.read_csv(dataset_file[0], delimiter='\t')


    # df1.to_csv("./dataset/test.txt", header = None, index = None, sep = "\t")

    import subprocess
    subprocess.run(["dglke_train","--model_name", "TransE_l2",\
                "--batch_size", "1000",\
                "--neg_sample_size", "200", \
                "--hidden_dim", "400", \
                "--gamma", "19.9", \
                "--lr", "0.25", \
                "--max_step", "24000", \
                "--log_interval", "100", \
                "--batch_size_eval", "16", \
                "-adv", \
                "--regularization_coef", "1.00E-09", \
                "--gpu", "0", \
                "--save_path", "./data", \
                "--data_path", "./dataset/", \
                "--format", "raw_udd_hrt", \
                "--data_files", "train.tsv", \
                "--dataset", "xxx",\
                "--neg_sample_size_eval", "10000"
                ], stdout=subprocess.PIPE)