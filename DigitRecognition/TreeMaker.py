from sklearn import datasets
from sklearn.svm import SVC
from scipy import misc
from sklearn import tree
import subprocess

clf = tree.DecisionTreeClassifier()
digits = datasets.load_digits()

clf = clf.fit(digits.data, digits.target)
tree.export_graphviz(clf, out_file='tree.dot', proportion=True,filled=True,impurity=False)

subprocess.call(['dot', '-Tpdf', 'tree.dot', '-o', 'tree.pdf'])
