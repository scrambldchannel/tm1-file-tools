from tm1filetools.tools.filetool import TM1FileTool


def test_orphan_rules(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_rules()

    assert "foo" not in [o.stem for o in orphans]
    assert "giraffe" in [o.stem for o in orphans]
