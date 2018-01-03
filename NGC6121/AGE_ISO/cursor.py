# -*- coding: utf-8 -*-

"""
Questo modulo contiene la classe Cursor.
Il suo scopo è permettere di aggiungere punti ad un grafico
esistente e di tener traccia di questi.

Richiede wxPython come backend di matplotlib.
"""

from __future__ import print_function
import sys
import matplotlib
matplotlib.use('WXAgg')
from matplotlib import pyplot as plt
import numpy as np

# pylint: disable=invalid-name
# alcuni nomi per modità devono essere lasciati come sono

# pylint: disable=too-many-instance-attributes
# Per ora servono tutti gli attributi definiti.

# pylint: disable=too-many-arguments
# Per ora servono tutti gli argomenti

class Cursor():

    """
    Questa classe gestisce l'aggiunta dei punti al grafico.
    Deve essere creato un oggetto Cursor come segue

        c = Cursor(self, fig, ax, plot_points=True, style='ro', zoom=[None,None], **kwargs)

    dove

        fig           ->  oggetto figura di matplotlib
        ax            ->  oggetto asse di matplotlib
        plot_points   ->  flag per determinare se plottare o meno i nuovi punti
        color         ->  colore dei punti aggiunti (se plottati) [colori di pyplot]
        zoom          ->  fa uno zoom verso il punto aggiunto riducendo i limiti alla 
                          larghezza specificata
        kwargs        ->  non in uso per adesso

    Va quindi attivato al momento dell'uso tramite

        c.start()

    I punti vengono aggiunti tramite il tasto sinistro del mouse e si
    terminare l'operazione con il tasto destro.
    Per ottenere le coordinate dei punti con un comando solo è possibile usare

        x, y = c.get_x_y()

    [In via di sviluppo]
    """
    allowed_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, fig, ax, plot_points=True, color='r', zoom=[None,None], **kwargs):
        self.fig = fig
        self.ax = ax
        self.plot_points = plot_points
        if color not in self.allowed_colors:
            print("Il colore '{}' non è tra quelli permessi,".format(color))
            print("\t {}".format(self.allowed_colors))
            print("Uso il colore di default ('r').")
            color = 'r'
        self.style = color+'.'
        self.zoom = zoom
        self.kwargs = kwargs

        self.x = []
        self.y = []
        self.button_conn = None

        if self.zoom[0] is not None:
            self.old_xlim = self.ax.get_xlim()
            print("Limiti originari in x -> {}".format(self.old_xlim))
        if self.zoom[1] is not None:
            self.old_ylim = self.ax.get_ylim()
            print("Limiti originari in y -> {}".format(self.old_ylim))

    def start(self):
        """Va chiamato nel codice."""
        self.button_conn = self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        plt.ion()
        print("Started.")

    def stop(self):
        """Chiamato automaticamente."""
        self.fig.canvas.mpl_disconnect(self.button_conn)
        plt.ioff()
        print("\nStopped.")

    def on_button_press(self, event):
        """Gestisce gli eventi legati al mouse."""
        #btn = event.button
        x = event.xdata
        y = event.ydata

        if (x is not None) and (y is not None):
            if event.button == 1:
                self.x.append(x)
                self.y.append(y)
                print('Add point at x={:<10.7f} y={:<10.7f}'.format(x, y), end='\r')
                sys.stdout.flush()
                if self.plot_points:
                    self.ax.plot(x, y, self.style)
                    if self.zoom[0]:
                        self.ax.set_xlim(left=x-self.zoom[0]/2., right=x+self.zoom[0]/2.)
                    if self.zoom[1]:
                        self.ax.set_ylim(top=y-self.zoom[1]/2., bottom=y+self.zoom[1]/2.)
                    self.fig.canvas.draw()
                
        if event.button == 3:
            if self.plot_points:
                print()
                if self.zoom[0]:
                    print("Ritorno ai limiti originari in x.")
                    self.ax.set_xlim(left=self.old_xlim[0],right=self.old_xlim[1])
                if self.zoom[1]:
                    print("Ritorno ai limiti originari in y.")
                    self.ax.set_ylim(bottom=self.old_ylim[0],top=self.old_ylim[1])
                self.fig.canvas.draw()

            self.stop()

    def get_x_y(self):
        """Ritorna le coordinate x e y dei punti aggiunti."""
        return np.array(self.x), np.array(self.y)


# def onclick(event):
#     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#           ('double' if event.dblclick else 'single', event.button,
#            event.x, event.y, event.xdata, event.ydata))

# if __name__ == '__main__':
#     fig, ax = plt.subplots()
#     ax.plot(np.random.rand(10))
#     cid = fig.canvas.mpl_connect('button_press_event', onclick)
#     plt.show()
