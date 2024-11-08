from src.main import is_image_file

def test_is_image_file():
    assert is_image_file('test.jpg') == True
    assert is_image_file('test.png') == True
    assert is_image_file('test.txt') == False
    assert is_image_file('test') == False
