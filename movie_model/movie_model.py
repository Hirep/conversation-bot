from sklearn.externals import joblib
import mpld3
import pandas as pd
from sklearn.manifold import MDS
import matplotlib.pyplot as plt



class Movies:
    def __init__(self, km, num_clusters, vocab_frame, films, frame, terms):
        self.KMmodel = km
        self.n_clusters = num_clusters
        self.vocab_frame = vocab_frame
        self.films = films
        self.frame = frame
        self.terms = terms
    def __str__(self):
        return "K-means model\n# of clusters: {}".format(self.n_clusters)

model = joblib.load('MovieModel.pkl')

def cluster_info():

    s = ""
    s += "Top terms per cluster: \n"
    order_centroids = model.KMmodel.cluster_centers_.argsort()[:, ::-1]
    for i in range(model.n_clusters):
        s += "\n\nCluster #{} words:\n".format(i)
        for ind in order_centroids[i, :6]:
            s += ' {}'.format(model.vocab_frame.ix[model.terms[ind].split(' ')].values.tolist()[0][0])

        s += "\nCluster #{} titles: \n".format(i)
        for title in model.frame.ix[i]['title'].values.tolist():
            s += ' {}'.format(title)
    return s

class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}


def cluster_graphic_html():

    MDS()

# two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(model.dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]
    clusters = model.KMmodel.labels_.tolist()
    #create data frame that has the result of the MDS plus the cluster numbers and titles
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=model.titles))

#group by cluster
    groups = df.groupby('label')

#define custom css to format the font and to remove the axis labeling
    css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }
"""

# Plot
    fig, ax = plt.subplots(figsize=(14,6)) #set plot size
    ax.margins(0.03) # Optional, just adds 5% padding to the autoscaling

    #set up colors per clusters using a dict
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
    cluster_names = {0: 'Family, home, war',
                 1: 'Police, killed, murders',
                 2: 'Father, New York, brothers',
                 3: 'Dance, singing, love',
                 4: 'Killed, soldiers, captain'}
#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, label=cluster_names[name], mec='none', color=cluster_colors[name])
        ax.set_aspect('auto')
        labels = [i for i in group.title]

        #set tooltip using points, labels and the already defined 'css'
        tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
                                           voffset=10, hoffset=10, css=css)
        #connect tooltip to fig
        mpld3.plugins.connect(fig, tooltip, TopToolbar())

        #set tick marks as blank
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])

        #set axis as blank
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)


    ax.legend(numpoints=1) #show legend with only one dot

    mpld3.display() #show the plot

    #uncomment the below to export to html
    html = mpld3.fig_to_html(fig)
    return html

def get_general_info():
    pass

def get_cluster_info():
    return cluster_info()

def get_cluster_graphic():
    return cluster_graphic_html()

def get_dendrogram():
    return
