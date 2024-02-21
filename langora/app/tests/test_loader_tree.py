import pytest

def exec_loader_tree(url:str):
    from loader.loader_tree_b4 import LoaderTreeB4
    loader = LoaderTreeB4()
    return loader.load_tree(url)

test_url = [
    ("https://www.techtarget.com/searchenterpriseai/definition/generative-AI",[0,0,16]),
    ("https://www.sciencedirect.com/science/article/pii/S0268401223000233", [0,12]),
    ("https://www.gartner.com/en/topics/generative-ai", [18]),
    ("https://hbr.org/2023/06/managing-the-risks-of-generative-ai", [5, 5]),
    ("https://www.bcg.com/capabilities/artificial-intelligence/generative-ai", [17]),
    ("https://www.linkedin.com/pulse/two-case-studies-applying-generative-ai-qualitative-data-friese", 9),
    ("https://www.forbes.com/sites/zendesk/2023/08/09/3-areas-customers-see-the-most-potential-for-generative-ai/", [2]),
    ("https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier", 18),
    ("https://medium.com/swlh/a-practical-guide-to-ai-product-management-part-1-5b629da25131", [5]),
    ("https://www.eweek.com/artificial-intelligence/generative-ai-enterprise-use-cases/", [4]),
    ("https://mitsloan.mit.edu/ideas-made-to-matter/machine-learning-explained", [0, 7]),
]
@pytest.mark.parametrize("url,expect", test_url)
def test_loader_tree_childs(url, expect):
    tree = exec_loader_tree(url)
    nb_childs = len(tree.childs)    
    if isinstance(expect, int):
        assert nb_childs==expect
        return    
    assert nb_childs==len(expect)
    for ic in range(nb_childs):
        assert len(tree.childs[ic].childs) == expect[ic]

