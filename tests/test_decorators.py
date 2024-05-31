from src.decorators import log


def test_log(capsys):

    @log()
    def square(x):
        """DocString test description"""
        return x * x

    print(square("as"))
    captured = capsys.readouterr()
    assert captured.out == (
        "======================ERROR=======================\n"
        "square error: <class 'TypeError'> Inputs: ('as',), {}\n"
        "can't multiply sequence by non-int of type 'str'\n"
        "================END ERROR MESSAGE=================\n\n"
    )
    print(square(3))
    captured = capsys.readouterr()
    assert captured.out == "square Inputs: (3,), {} - ok\n9\n"
    assert square.__doc__ == "DocString test description"
