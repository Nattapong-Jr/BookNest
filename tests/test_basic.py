def calculate_total(price, quantity):
    return price * quantity

def test_calculate():
    result = calculate_total(299, 2)

    assert result == 598