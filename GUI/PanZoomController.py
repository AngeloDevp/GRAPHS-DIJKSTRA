class PanZoomController:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.pan_state = {'is_panning': False, 'start_x': 0, 'start_y': 0, 'xlim': None, 'ylim': None}
        self.setup_connections()

    def setup_connections(self):
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def zoom(self, event):
        if event.inaxes != self.ax: return
        
        base_scale = 1.2
        if event.button == 'up':    scale_factor = 1 / base_scale
        elif event.button == 'down': scale_factor = base_scale
        else: return

        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        xdata, ydata = event.xdata, event.ydata

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax or event.button != 1: return
        self.pan_state['is_panning'] = True
        self.pan_state['start_x'] = event.x
        self.pan_state['start_y'] = event.y
        self.pan_state['xlim'] = self.ax.get_xlim()
        self.pan_state['ylim'] = self.ax.get_ylim()

    def on_motion(self, event):
        if not self.pan_state['is_panning'] or event.inaxes != self.ax: return
        
        inv = self.ax.transData.inverted()
        start_data = inv.transform((self.pan_state['start_x'], self.pan_state['start_y']))
        current_data = inv.transform((event.x, event.y))

        dx = current_data[0] - start_data[0]
        dy = current_data[1] - start_data[1]

        self.ax.set_xlim(self.pan_state['xlim'][0] - dx, self.pan_state['xlim'][1] - dx)
        self.ax.set_ylim(self.pan_state['ylim'][0] - dy, self.pan_state['ylim'][1] - dy)
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        if event.button == 1:
            self.pan_state['is_panning'] = False