from pycodb.utils import where_params, where_condition


def test_where_params():
    assert where_params({ 'Id': 666 }) == '(Id,eq,666)'
    assert where_params({ 'Id': 666, 'name': 'foo.pdf'}) == '(Id,eq,666)~and(name,eq,foo.pdf)'
    assert where_params({ 'Id': 666, 'name': { 'in': ['foo.pdf', 'bar.pdf'] } }) == '(Id,eq,666)~and(name,in,foo.pdf,bar.pdf)'


def test_where_condition():
    assert where_condition('Id', 666) == '(Id,eq,666)'
    assert where_condition('Id', [666, 777], 'in') == '(Id,in,666,777)'
