import sys
import json
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

from dataset import Dataset
from utils import *

if __name__ == "__main__":
    dataset = Dataset(root + "/data", do_dummies=True)
    train_x, train_y, _ = dataset.get_cancel_data()
    print(train_x.shape)
    groups = dataset.get_groups("train")
    models = [weighted(RandomForestClassifier)(random_state=0, n_jobs=4)]
    models = [RandomForestClassifier(random_state=0, n_jobs=4)]
    params_grid = [{
        'criterion': ['entropy', 'gini'],
        'n_estimators': [200, 400, 600, 800, 1000],
        'max_features': ['auto', None],
        'max_depth': [8, 10, 20, 40, 60, 80, 100, None],
        'min_samples_split': [2e-4, 1e-3, 2e-3, 1e-2],
        'min_samples_leaf': [1e-4, 5e-4, 1e-3, 5e-3], }]
    print(params_grid)
    splits = range(2, 5)
    for model, params_grid in zip(models, params_grids):
        cv = GroupTimeSeriesSplit(n_splits=5).split(train_x, groups=groups, select_splits=splits)
        results = single_search_cv(x=train_x, y=train_y, groups=groups, model=model, params_grid=params_grid, cv=cv, \
                            scoring="neg_mean_absolute_error", n_iter=5, random_state=0, n_jobs=4)
        
        print_format = lambda sort_key: json.dumps(sorted(results, key=sort_key, reverse=True), indent=4)
        
        print("mean_score:", print_format(sort_key=lambda item: item["mean_score"]))
        for i, split in enumerate(splits):
            print("split{}_score:".format(split), print_format(sort_key=lambda item: item["scores"][i]))
        print('\n')
