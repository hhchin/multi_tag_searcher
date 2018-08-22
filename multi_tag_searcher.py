import sublime, sublime_plugin
from .mtsearch import MultiTokenSearcher

class MultiSearchCommand(sublime_plugin.WindowCommand):

  def run(self, mode=0):
    if mode == 0:
      self.on_start()
      self.window.show_input_panel("Tokens:", "", self.on_done, None, None)
    else:
      if mode == -1:
        self.ind = (self.ind-1) % len(self.pos_arr)
      if mode == 1:
        self.ind = (self.ind+1) % len(self.pos_arr)        
      pt = self.pos_arr[self.ind]
      print(pt)
      #self.window.active_view().sel().clear()
      #self.window.active_view().sel().add(sublime.Region(pt))
      self.window.active_view().show(pt)

  def on_start(self):
    self.window.active_view().erase_regions("mts_tokens")
    text_content = self.window.active_view().substr(sublime.Region(0, self.window.active_view().size()))
    self.mts = MultiTokenSearcher(text_content.split('\n'))
    

  def on_change(self, text):
    # to be implemented in a later version
    pass

  def on_done(self, text):
    try:
      if self.window.active_view():
        tokens = [t.strip() for t in text.split(',')]
        if tokens[-1] == '': # if only 1 token
          tokens = tokens[:-1]

        result, all_pos = self.mts.search(tokens) 

        #highlight the tokens
        region_arr = []
        for p in all_pos:
          start = self.window.active_view().text_point(p[0], p[1])
          end = self.window.active_view().text_point(p[2], p[3])
          reg = sublime.Region(start, end)
          region_arr.append(reg)
        self.window.active_view().add_regions("mts_tokens", region_arr, "comment", "", sublime.DRAW_NO_FILL)

        self.ind = 0
        self.pos_arr = [] 
        print(result)
        for res in result:
          pt = self.window.active_view().text_point(res[1][0], res[1][1])
          self.pos_arr.append(pt)
        pt = self.pos_arr[0]
        self.window.active_view().sel().clear()
        self.window.active_view().sel().add(sublime.Region(pt))
        self.window.active_view().show(pt)
        
    except ValueError:
      pass





