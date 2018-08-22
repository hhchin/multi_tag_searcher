from patricia import trie
from union_find import disjoint_sets
from collections import defaultdict
import bisect

class GroupSearcher(object):

  def __init__(self, string_arr):
    #use a trie to map words to (row, col) pairs
    self.trie = trie()
    for row_index, row in enumerate(string_arr):
      word_pos_arr = self.split_line(row)
      for word, col_index in word_pos_arr:
        if word in self.trie:
          self.trie[word].append((row_index, col_index))
        else:
          self.trie[word]=[(row_index, col_index)]

  #split on white space an return index. ignore trailing space
  def split_line(self, line):
    s = 0
    arr = []
    line = line.rstrip()
    for t in range(len(line)):
      #print(t)
      if line[t]==' ':
        arr.append([line[s:t],s])
        s=t+1 
    arr.append([line[s:t+1],s])
    return arr

  #average english word length is 5 characters
  def search(self, token_group, col_win=20, row_win=3, row_penalty=5):
    temp_match_table = defaultdict(list)
    for token in token_group:
      if not self.trie.isPrefix(token):
        continue
      for valid in self.trie.iter(token):
        for pos in self.trie[valid]:
          temp_match_table[pos[0]].append(pos[1])

    # sort the match positions
    row_keys = sorted(temp_match_table.keys())
    match_table = {}
    for k in row_keys:
      match_table[k] = sorted(temp_match_table[k])

    #determine if 2 position are close
    def is_close(can_row, can_col, cur_row, cur_col):
      return (cur_row-can_row)*row_penalty+(can_col-cur_col) <= col_win

    match_edges = []
    for cur_row_ind, cur_row in enumerate(row_keys):
      for cur_col_ind, cur_col in enumerate(match_table[cur_row]): #first row is the same row
        for can_col in match_table[cur_row][cur_col_ind+1:]:
          print(can_col, cur_col)
          if (can_col-cur_col) <= col_win:
            match_edges.append( ((cur_row,cur_col),(cur_row, can_col)) )
          else: #cur col is too far away
            break

        for can_row in row_keys[cur_row_ind+1:]:
          if (can_row-cur_row)*row_penalty > col_win:
            break
          for can_col in match_table[can_row]:
            if (can_row-cur_row)*row_penalty+(can_col-cur_col) <= col_win:
              match_edges.append( ((cur_row,cur_col),(can_row, can_col)) )
            else:
              break
        
    #find cluster using union find
    cluster_list = disjoint_sets(match_edges)
    result = []
    for cluster in cluster_list:
      row = [r for r,_ in cluster]
      col = [c for _,c in cluster]
      top_row, top_col, btm_row, btm_col = min(row), min(col), max(row), max(col)
      result.append([len(cluster), (top_row, top_col, btm_row, btm_col)])
    
    return result


  def print_result(self, text, result):
    for res in result:
      tr, tc, br, bc = res[1]
      print(res[0],'@ position ',tr,tc,'to',br,bc)
      bc+=8
      for r in range(tr, br+1):
        line = text[r]
        mask_line = '*'*(tc-1)+line[tc:bc]+'*'*(len(line)-bc)
        print(mask_line)
      print()

  def search_and_print(self, text, token_group):
    result = self.search(token_group)
    self.print_result(text, result)

def main():
  with open('1.txt') as fd:
    lines = fd.readlines()
  gs = GroupSearcher(lines)
  gs.search_and_print(lines, ['parade', 'Squadron'])


if __name__ == '__main__':
  main()
