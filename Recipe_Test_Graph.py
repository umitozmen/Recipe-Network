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

    return df1 , print(f"./dataset/{nRowsRead}_samples.csv created")

def create_dlg_ke_relations(df1):
    
    col_list_to_tidy = ["Name","RecipeCategory","RecipeIngredientQuantities","RecipeIngredientParts"]

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

    #df_rel.to_csv("./dataset/train.tsv", header = None, index = None, sep = "\t")

    return df_rel

if __name__ == "__main__":

    nRowsRead = 1000

    
    df1 = get_sample_file(nRowsRead)

    df_rel = create_dlg_ke_relations(df1)

    G = nx.Graph()

    for i, ing in enumerate(df_rel['head']):
        G.add_nodes_from([(f'i{i}', {"name_": ing, "type_":"Ingredient"})])
    
    for i, rec in enumerate(df_rel['tail']):
        G.add_nodes_from([(f'r{i}', {"name_": rec, "type_":"Recipe"})])

    print(G.number_of_nodes())

    # G = nx.Graph()
    # G.add_nodes_from([(0, {"name_":"Biryani", "type_":"Recipe"}),
    #                 (1, {"name_":"Best Lemonade", "type_":"Recipe"})])
    


    # G.add_edges_from([(0,3),(0,4),(0,5),(1,4),(1,3),(1,6)])

    
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.axis('equal')
    # plt.show()

