import pandas as pd
import folium 
from folium import plugins
from sklearn.metrics import confusion_matrix
import itertools 
from matplotlib import plt
import numpy as np


class Data:
    def __init__(self,data):
        self.path_map = 'map.html'
        self.path_csv = 'raw_data.csv'
        self.path_out = 'res.png'
        self.classes=[0, 1]
        self.normalize=False
        self.df = None

    def map(self, data):
        df = pd.DataFrame(data)
        self.df = df
        df.to_csv( self.path_csv, index=False)
        df = pd.read_csv(self.path_csv, sep=';')
        m = folium.Map([58, 76], zoom_start=3)
        hm = folium.plugins.HeatMap(df[['hex_lat', 'hex_lon']].values, radius=12)
        hm.add_to(m)
        m.save(self.path_map)

    def get_predict(self):
        y_pred = self.df['y_pred'].values
        y_test = self.df['y_test'].values
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(7, 7))
        plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        plt.title("Confusion matrix")
        plt.colorbar()
        tick_marks = np.arange(len(self.classes))
        plt.xticks(tick_marks, self.classes, rotation=90)
        plt.yticks(tick_marks, self.classes)
        if self.normalize:
            cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        thresh = cm.max() / 2.0
        cm = np.round(cm, 2)
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(
                j,
                i,
                cm[i, j],
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )
        plt.ylabel("True label")
        plt.xlabel("Predicted label")
        plt.savefig(self.path_out)