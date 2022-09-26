from tm1filetools.files.general import (  # get_sub_files,; get_vue_files,
    attr_prefix,
    get_attribute_cub_files,
    get_attribute_dim_files,
    get_blb_files,
    get_cub_files,
    get_dim_files,
    get_files_by_ext,
    get_rux_files,
)


def test_get_files_by_ext(artifact_files):
    dims = get_files_by_ext(artifact_files, ext="dim")

    assert len(dims) > 0


def test_get_blb(artifact_files, artifact_files_mixed_case):

    blbs = get_blb_files(artifact_files)

    assert blbs.count("foo") == 0
    assert blbs.count("emu") == 1

    blbs = get_blb_files(artifact_files_mixed_case)

    assert blbs.count("foo") == 0
    assert blbs.count("emu") == 1


def test_get_cub(artifact_files, artifact_files_mixed_case):

    cubs = get_cub_files(artifact_files)

    assert cubs.count("basilisk") == 0
    assert cubs.count("dog") == 1

    cubs = get_cub_files(artifact_files_mixed_case)

    assert cubs.count("basilisk") == 0
    assert cubs.count("cat") == 1


def test_get_dim(artifact_files, artifact_files_mixed_case):

    dims = get_dim_files(artifact_files)

    assert dims.count("bunyip") == 0
    assert dims.count("possum") == 1

    dims = get_dim_files(artifact_files_mixed_case)

    assert dims.count("bunyip") == 0
    assert dims.count("possum") == 1


def test_get_rux(artifact_files, artifact_files_mixed_case):

    ruxes = get_rux_files(artifact_files)

    assert ruxes.count("cockatoo") == 0
    assert ruxes.count("giraffe") == 1

    ruxes = get_rux_files(artifact_files_mixed_case)

    assert ruxes.count("cockatoo") == 0
    assert ruxes.count("giraffe") == 1


def test_get_attribute_dims(artifact_files, artifact_files_mixed_case):

    attr_dims = get_attribute_dim_files(artifact_files)

    assert attr_dims.count(attr_prefix + "cockatoo") == 0
    assert attr_dims.count(attr_prefix + "kangaroo") == 1

    attr_dims = get_attribute_dim_files(artifact_files_mixed_case)

    assert attr_dims.count(attr_prefix + "cockatoo") == 0
    assert attr_dims.count(attr_prefix + "kangaroo") == 1


def test_get_attribute_cubes(artifact_files, artifact_files_mixed_case):

    attr_cubs = get_attribute_cub_files(artifact_files)

    assert attr_cubs.count(attr_prefix + "cockatoo") == 0
    assert attr_cubs.count(attr_prefix + "humphrey") == 1

    attr_cubs = get_attribute_cub_files(artifact_files_mixed_case)

    assert attr_cubs.count(attr_prefix + "cockatoo") == 0
    assert attr_cubs.count(attr_prefix + "humphrey") == 1


# def test_get_vue(artifact_files, artifact_files_mixed_case):

#     vues = get_vue_files(artifact_files)

#     assert vues.count("cockatoo") == 0
#     assert vues.count("giraffe") == 1

#     # vues = get_vue_files(artifact_files_mixed_case)

#     # assert vues.count("cockatoo") == 0
#     # assert vues.count("giraffe") == 1
