

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
import pandas as pd

def get_top_recommendation(n:int=10, order:None|list=None, **kwags):
    # Sample data
    data = pd.read_csv('clean_phone_data_final.csv')
    df = pd.DataFrame(data)
    
    
    # make all columns string
    df = df.astype(str)


    # Combine the pipelines only for those non-existing phone specs keys
    feature_union_keys = []
    for key in kwags.keys():
        if key in df.columns:
            feature_union_keys.append(
                (key, Pipeline([
                    ('selector', FunctionTransformer(lambda x: x[key], validate=False)),
                    ('tfidf', TfidfVectorizer(stop_words='english'))
                ]))
            )

    # Combine the pipelines using FeatureUnion
    feature_union = FeatureUnion(feature_union_keys)

    # Fit and transform the data
    feature_vectors = feature_union.fit_transform(df)

    # Now feature_vectors contains TF-IDF representations for both 'brand' and 'model'
    from sklearn.neighbors import NearestNeighbors

    # Create a DataFrame for the non-existing phone specs
    non_existing_df = pd.DataFrame([kwags])

    # Transform the non-existing phone specs using the previously defined FeatureUnion
    non_existing_feature_vectors = feature_union.transform(non_existing_df)

    # Create a NearestNeighbors model
    knn = NearestNeighbors(n_neighbors=50, metric='minkowski')

    # Fit the feature vectors to the knn model
    knn.fit(feature_vectors)

    # Find the nearest neighbors for the non-existing phone specs
    distances, indices = knn.kneighbors(non_existing_feature_vectors)

    # Print top recommendation
    top_recommendation = df.iloc[indices[0]][:n]

    #  sort values based on the order
    if order:
        top_recommendation = top_recommendation.sort_values(by=order, ascending=False)

    # get the order of the columns
    columns = top_recommendation.columns.to_list()



    return top_recommendation.to_dict(orient="records")






print(get_top_recommendation(n=int(10), **{'brand': 'xiaomi', 'os': 'android', 'release': '2024'}))
