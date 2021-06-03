from suffix_tree import SuffixTree


def full_text_search_engine(text: str, pattern: str):
    tree = SuffixTree(text+'$')
    tree.build_suffix_tree()
    current_node = tree.root
    current_symb = 0
    res = True
    while current_symb < len(pattern):
        if pattern[current_symb] in current_node.children:
            current_node = current_node.children[pattern[current_symb]]
            len_edge = current_node.end - current_node.start + 1
            diff = len(pattern) - current_symb
            if len_edge >= diff:
                if pattern[current_symb:] != text[current_node.start:current_node.start+diff]:
                    res = False
                break
            else:
                if pattern[current_symb:current_symb+len_edge] == text[current_node.start:current_node.end+1]:
                    current_symb += len_edge
                else:
                    res = False
                    break
        else:
            res = False
            break
    if res:
        stack = [current_node]
        beginnings_of_pattern = []
        while stack:
            new_el = stack.pop()
            if new_el.leaf:
                beginnings_of_pattern.append(new_el.suffix_index)
            for child in new_el.children:
                stack.append(new_el.children[child])
        res = beginnings_of_pattern

    return res
