from tm1filetools.orphans import (  # attr_prefix,
    attr_prefix,
    get_orphan_attribute_cube_files,
    get_orphan_attribute_dim_files,
    get_orphan_rux_files,
)


def test_orphan_rux(artifact_files):

    orphans = get_orphan_rux_files(artifact_files)

    assert orphans.count("foo") == 0
    assert orphans.count("giraffe") == 1


def test_orphan_rux_mixed_case(artifact_files_mixed_case):

    orphans = get_orphan_rux_files(artifact_files_mixed_case)

    assert orphans.count("foo") == 0
    assert orphans.count("giraffe") == 1


def test_orphan_attr_dim(artifact_files):

    orphans = get_orphan_attribute_dim_files(artifact_files, strip_prefix=True)

    assert len(orphans) > 0

    assert orphans.count("koala") == 0

    assert orphans.count("kangaroo") == 1

    orphans = get_orphan_attribute_dim_files(artifact_files)

    assert len(orphans) > 0

    assert orphans.count(attr_prefix + "koala") == 0

    assert orphans.count(attr_prefix + "kangaroo") == 1


def test_orphan_attr_cube(artifact_files):

    orphans = get_orphan_attribute_cube_files(artifact_files, strip_prefix=True)

    assert len(orphans) > 0

    assert orphans.count("foo") == 0

    assert orphans.count("humphrey") == 1

    orphans = get_orphan_attribute_cube_files(artifact_files)

    assert len(orphans) > 0

    assert orphans.count(attr_prefix + "foo") == 0

    assert orphans.count(attr_prefix + "humphrey") == 1
