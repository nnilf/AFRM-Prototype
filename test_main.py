import main

HEADER = "flight,aircraft,fuel_kg,fuel_flow_kg_h,distance_km,groundspeed_kmh,protected_kg\n"


def run_csv(rows, tmp_path, capsys, header=HEADER):
    csv_file = tmp_path / "flights.csv"
    csv_file.write_text(header + rows)
    main.run(csv_file)
    return capsys.readouterr().out


def test_fr05_critical_warning(tmp_path, capsys):
    # 4500 - 2400 x 1.5 = 900, ratio 0.9
    output = run_csv("FLT001,Test,4500,2400,1200,800,1000\n", tmp_path, capsys)
    assert "CRITICAL" in output
    assert "Arrival fuel is below protected fuel" in output


def test_fr05_caution_warning(tmp_path, capsys):
    # 4700 - 2400 x 1.5 = 1100, ratio 1.1
    output = run_csv("FLT001,Test,4700,2400,1200,800,1000\n", tmp_path, capsys)
    assert "CAUTION" in output
    assert "Arrival fuel is less than 25% above protected fuel" in output


def test_fr05_normal_has_no_warning(tmp_path, capsys):
    # 6000 - 2400 x 1.5 = 2400, ratio 2.4
    output = run_csv("FLT001,Test,6000,2400,1200,800,1000\n", tmp_path, capsys)
    assert "NORMAL" in output
    assert "Arrival fuel is" not in output


def test_fr05_invalid_row_does_not_stop_later_rows(tmp_path, capsys):
    rows = "FLT001,Test,abc,2400,1200,800,1000\nFLT002,Test,6000,2400,1200,800,1000\n"
    output = run_csv(rows, tmp_path, capsys)
    assert "INVALID: fuel must be a number" in output
    assert "FLT002" in output
    assert "NORMAL" in output


def test_fr05_disclaimer_before_and_after_table(tmp_path, capsys):
    output = run_csv("FLT001,Test,6000,2400,1200,800,1000\n", tmp_path, capsys)
    lines = output.splitlines()
    assert lines[0] == "Prototype"
    assert lines[-1] == "Prototype"


def test_fr05_missing_column_gives_clear_error(tmp_path, capsys):
    header = HEADER.replace("fuel_flow_kg_h,", "")
    output = run_csv("FLT001,Test,6000,1200,800,1000\n", tmp_path, capsys, header)
    assert "INVALID FILE: missing columns: fuel_flow_kg_h" in output
    assert "FLT001" not in output
    assert output.splitlines()[-1] == "Prototype"


def test_fr05_renamed_column_gives_clear_error(tmp_path, capsys):
    header = HEADER.replace("fuel_kg", "fuel_lb")
    output = run_csv("FLT001,Test,6000,2400,1200,800,1000\n", tmp_path, capsys, header)
    assert "INVALID FILE: missing columns: fuel_kg" in output
    assert "FLT001" not in output
    assert output.splitlines()[-1] == "Prototype"
