import pytest

def exec_loader_tree(url:str):
    from loader.loader_tree_b4 import LoaderTreeB4
    loader = LoaderTreeB4()
    return loader.load_tree(url)

test_url = [
    ("https://www.techtarget.com/searchenterpriseai/definition/generative-AI",1)
]
@pytest.mark.parametrize("url,expect", test_url)
def test_loader_tree_childs(url, expect):
    tree = exec_loader_tree(url)
    assert len(tree.childs)==0
