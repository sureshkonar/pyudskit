import json

from pyudskit.cli import main


def test_cli_encode_runs(monkeypatch, capsys):
    monkeypatch.setattr("pyudskit.cli.UDS.encode", lambda self, text: "22 F1 90")
    monkeypatch.setattr("sys.argv", ["pyudskit", "encode", "Read the VIN"])
    try:
        main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert out.strip() != ""


def test_cli_profile_validate_and_show(monkeypatch, capsys, tmp_path):
    profile = {"name": "demo", "dids": {"0xF190": {"name": "VIN", "length_bytes": 17}}}
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile))

    monkeypatch.setattr("sys.argv", ["pyudskit", "profile", "validate", str(path)])
    try:
        main()
    except SystemExit:
        pass
    assert "OK" in capsys.readouterr().out

    monkeypatch.setattr("sys.argv", ["pyudskit", "profile", "show", str(path)])
    try:
        main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert "name:" in out
