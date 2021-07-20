from pathlib import Path
import matplotlib.pyplot as plt # plotting
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import networkx as nx
import glob
import os

def get_sample_file(nRowsRead=None):

    main_directory = Path(__file__).parent.parent / 'dataset recipe'
    dataset_file = [main_directory/'recipes.csv']
    col_list = ["RecipeId","Name","RecipeCategory","RecipeIngredientQuantities","RecipeIngredientParts","AggregatedRating","ReviewCount"]
    dtype_dic= { 'RecipeId':int, 'Name':str, 'RecipeCategory':str, 'RecipeIngredientQuantities':str, 'RecipeIngredientParts':str, 'AggregatedRating':float, 'ReviewCount':float }
    #nRowsRead specify 'None' if want to read whole file
    
    df1 = pd.read_csv(dataset_file[0], delimiter=',', usecols=col_list, dtype = dtype_dic)

    df1.dataframeName = f'{nRowsRead}_samples.csv'

    #df1.to_csv(f"./dataset/{nRowsRead}_samples.csv", index = None, sep = ",")

    return df1 #, print(f"./dataset/{nRowsRead}_samples.csv created")

def data_eng(df1,col_list_to_tidy):

    for col in col_list_to_tidy:
        df1[col] = df1[col].str.replace('c("','', regex = False)
        df1[col] = df1[col].str.replace('", "',',', regex = False)
        df1[col] = df1[col].str.replace('"','', regex = False)
        df1[col] = df1[col].str.replace(')','', regex = False)  
        df1[col] = df1[col].str.split(',')

    df1.reset_index(drop=True)
    
    #df1.to_csv(f"./dataset/{nRowsRead}_samples.csv", index = None, sep = ",")

    df_rel = pd.DataFrame(columns = ["head", "rel", "tail"])

    for i, rec_val in enumerate(df1["RecipeIngredientParts"]) :
        if i in [100000,200000,300000,400000,500000]:
            df_rel.to_csv(f"./dataset/train{i}.tsv", header = None, index = None, sep = "\t")
            df_rel = pd.DataFrame(columns = ["head", "rel", "tail"])

        for ing_val in rec_val:
            df_rel = df_rel.append({"head": ing_val.strip(), "rel" : "ingredient_of", "tail": df1.iloc[i]['Name'][0].strip()}, ignore_index=True)

    df_rel.to_csv(f"./dataset/train_last.tsv", header = None, index = None, sep = "\t")

if __name__ == "__main__":

    #nRowsRead = 'all'
    #col_list_to_tidy = ["Name","RecipeCategory","RecipeIngredientQuantities","RecipeIngredientParts"]
    
    #df1 = get_sample_file(nRowsRead, col_list_to_tidy)

    main_directory = Path(__file__).parent / 'dataset'
     
    all_files = glob.glob(os.path.join(main_directory, "*.tsv")) 

    df_from_each_file = (pd.read_csv(f) for f in all_files)
    concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
    
    concatenated_df.to_csv(f"./dataset/train_allset.tsv", header = None, index = None, sep = "\t")
    # G = nx.Graph()

    # for i, rec in enumerate(df_rel['tail']):
    #     G.add_nodes_from([(rec, {"id_": f'r{i}', "type_":"Recipe"})])

    # for i, ing in enumerate(df_rel['head']):
    #     G.add_nodes_from([(ing, {"id_": f'i{i}', "type_":"Ingredient"})])
    #     G.add_edges_from([(ing,df_rel.iloc[i]['tail'])])

    # print(G.number_of_nodes())
    # print(G.number_of_edges())
   
    # nx.draw(G, with_labels=False)
    # plt.axis('equal')
    # plt.show()

    # import json
    # from networkx.readwrite import json_graph

    # for n in G:
    #     G.nodes[n]['name'] = n

    # d = json_graph.node_link_data(G)
    # json.dump(d, open('force/force.json','w'))

    # from networkx import http_server
    # http_server.load_url('force/force.html')
