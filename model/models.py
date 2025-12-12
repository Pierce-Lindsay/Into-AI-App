import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, matthews_corrcoef
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier


#model constants
K_SPLIT_COUNT = 5
MAX_ITER = 1000
#we want all scoring to be done according to MCC
#SCORER = make_scorer(matthews_corrcoef)
SCORER = 'neg_log_loss'
CV = StratifiedKFold(n_splits=K_SPLIT_COUNT, shuffle=True, random_state=1)

#base class for models
class Model:
    def __init__(self, train_X, train_Y):
        self.train_X = train_X
        self.train_Y = train_Y
        #filled in when functions called
        self.grid = None
        self.predicted = None
        self.best_perams = None
        self.best_score = None
        self.test_score = None
        self.best_model = None
        self.name = "model"
        
    #optimize the model's perams for the given training data   
    def optimize(self):
        print("Fit not implemented!")
    
    #update the grid by fitting and setting important values  
    def update_grid(self):
        self.grid.fit(self.train_X, self.train_Y)
        self.best_perams = self.grid.best_params_
        self.best_score = self.grid.best_score_
        self.best_model = self.grid.best_estimator_
    
    #print important values for training
    def print_best_from_optimize(self):
        print(f"{self.name}: {self.best_perams}: {self.grid.best_score_}")
    
    #update test_data prections values and print them
    def update_best_predictions(self, test_X, test_Y):
        #find the best peram combo and use it to get a score from test data
        self.predicted = self.grid.best_estimator_.predict(test_X)
        self.test_score = matthews_corrcoef(test_Y, self.predicted)
        print(f"{self.name}: {self.best_perams}: {self.test_score}")
        

#wrapper class for fitting SVM
class SVM(Model):
    def __init__(self, train_X, train_Y):
        super().__init__(train_X, train_Y)
        self.name = "SVM" 

    def optimize(self):
        #param combinations  
        param_grid = {'clf__C':[0.1, 1, 10], 
                      'clf__gamma':[0.001,0.01, 0.1, 1], 
                      'clf__kernel':['rbf', 'sigmoid', 'linear']}
        
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(probability=True,random_state=1, max_iter=MAX_ITER))])
        
        print("Fitting...SVM!")
        self.grid = GridSearchCV(pipe, param_grid, scoring=SCORER, cv=CV)
        self.update_grid()
        
#wrapper class for K nearest Neighbors    
class KNeighbors(Model):
    def __init__(self, train_X, train_Y):
        super().__init__(train_X, train_Y)
        self.name = "KNN" 
            
    def optimize(self):
        #params to optimize
        param_grid = {'clf__n_neighbors':[2, 4, 6, 8], 
                      'clf__algorithm':['ball_tree', 'kd_tree', 'brute'], 
                      'clf__p':[1, 2]}
        pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", KNeighborsClassifier())])
        
        self.grid = GridSearchCV(pipe, param_grid, scoring=SCORER, cv=CV)
        self.update_grid()                   

#wrapper class for decision tree
class DecisionTree(Model):
    def __init__(self, train_X, train_Y):
        super().__init__(train_X, train_Y)
        self.name = "Decision Tree" 
    
    def optimize(self):   
        #params to optimize
        param_grid = {'clf__criterion':["gini", "entropy"], 
                      'clf__max_depth':[None, 100, 10, 5], 
                      'clf__ccp_alpha':[0.001, 0.01, 0.1]}
        
        pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", DecisionTreeClassifier(random_state=1))])
        
        self.grid = GridSearchCV(pipe, param_grid, scoring=SCORER, cv=CV)
        self.update_grid()
        
#wrapper for logistic regression 
class LogRegression(Model):
    def __init__(self, train_X, train_Y):
        super().__init__(train_X, train_Y)
        self.name = "Logistic Regression"

    def optimize(self):
        #perams to optimize
        param_grid = {'clf__penalty':[None, "l2"], 
                      'clf__C':[0.01, 0.1, 1, 10], 
                      'clf__solver':["lbfgs", "saga"]}
        pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=MAX_ITER))])
        
        self.grid = GridSearchCV(pipe, param_grid, scoring=SCORER, cv=CV)
        self.update_grid()  
        
class XGB(Model):
    def __init__(self, train_X, train_Y):
        super().__init__(train_X, train_Y)
        self.name = "XG boost"

    def optimize(self):
        #perams to optimize
        param_grid = {'clf__n_estimators':[100, 200, 400, 600, 900], 
                      'clf__max_depth':[3, 5, 10, 20], 
                      'clf__learning_rate':[0.001, 0.01, 0.1]}
        pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", XGBClassifier(objective = 'binary:logistic',
                              eval_metric= 'logloss'))])
        
        self.grid = GridSearchCV(pipe, param_grid, scoring=SCORER, cv=CV, n_jobs=-1)
        self.update_grid()  