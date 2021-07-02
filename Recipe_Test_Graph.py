from pathlib import Path
#from mpl_toolkits.mplot3d import Axes3D
#from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
#import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import networkx as nx

def get_sample_file(nRowsRead=None):

    main_directory = Path(__file__).parent.parent / 'dataset recipe'
    dataset_file = [main_directory/'recipes.csv']
    col_list = ["RecipeId","Name","RecipeCategory","RecipeIngredientQuantities","RecipeIngredientParts","AggregatedRating","ReviewCount"]
    dtype_dic= { 'RecipeId':int, 'Name':str, 'RecipeCategory':str, 'RecipeIngredientQuantities':str, 'RecipeIngredientParts':str, 'AggregatedRating':float, 'ReviewCount':float }
    #nRowsRead specify 'None' if want to read whole file
    
    df1 = pd.read_csv(dataset_file[0], delimiter=',', usecols=col_list, dtype = dtype_dic).sample(nRowsRead, random_state=44)

    df1.dataframeName = f'{nRowsRead}_samples.csv'

    #df1.to_csv(f"./dataset/{nRowsRead}_samples.csv", index = None, sep = ",")

    return df1 #, print(f"./dataset/{nRowsRead}_samples.csv created")

if __name__ == "__main__":

    nRowsRead = 1000
    col_list_to_tidy = ["Name","RecipeCategory","RecipeIngredientQuantities","RecipeIngredientParts"]
    
    df1 = get_sample_file(nRowsRead)

    for col in col_list_to_tidy:
        df1[col] = df1[col].str.replace('c("','', regex = False)
        df1[col] = df1[col].str.replace('", "',',', regex = False)
        df1[col] = df1[col].str.replace('"','', regex = False)
        df1[col] = df1[col].str.replace(')','', regex = False)  
        df1[col] = df1[col].str.split(',')

    df1.reset_index(drop=True)

    df_rel = pd.DataFrame(columns = ["head", "rel", "tail"])

    for i, rec_val in enumerate(df1["RecipeIngredientParts"]) :
        for ing_val in rec_val:
            df_rel = df_rel.append({"head": ing_val.strip(), "rel" : "ingredient_of", "tail": df1.iloc[i]['Name'][0].strip()}, ignore_index=True)


    df1.to_csv(f"./dataset/{nRowsRead}_samples.csv", index = None, sep = ",")
    df_rel.to_csv("./dataset/train.tsv", header = None, index = None, sep = "\t")
    #df1['RecipeIngredientParts'] = df2


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


    # test_directory = Path(__file__).parent / 'dataset'
    # dataset_file = [test_directory/'relations.tsv']
    # df1 = pd.read_csv(dataset_file[0], delimiter='\t')


    # df1.to_csv("./dataset/test.txt", header = None, index = None, sep = "\t")
