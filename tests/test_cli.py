from pyudskit.cli import main


def test_cli_encode_runs(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["pyudskit", "encode", "Read the VIN"])
    try:
        main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert out.strip() != ""
