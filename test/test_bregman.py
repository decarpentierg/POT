

import ot
import numpy as np

# import pytest


def test_sinkhorn():
    # test sinkhorn
    n = 100
    np.random.seed(0)

    x = np.random.randn(n, 2)
    u = ot.utils.unif(n)

    M = ot.dist(x, x)

    G = ot.sinkhorn(u, u, M, 1, stopThr=1e-10)

    # check constratints
    assert np.allclose(u, G.sum(1), atol=1e-05)  # cf convergence sinkhorn
    assert np.allclose(u, G.sum(0), atol=1e-05)  # cf convergence sinkhorn


def test_sinkhorn_empty():
    # test sinkhorn
    n = 100
    np.random.seed(0)

    x = np.random.randn(n, 2)
    u = ot.utils.unif(n)

    M = ot.dist(x, x)

    G, log = ot.sinkhorn([], [], M, 1, stopThr=1e-10, verbose=True, log=True)
    # check constratints
    assert np.allclose(u, G.sum(1), atol=1e-05)  # cf convergence sinkhorn
    assert np.allclose(u, G.sum(0), atol=1e-05)  # cf convergence sinkhorn

    G, log = ot.sinkhorn([], [], M, 1, stopThr=1e-10,
                         method='sinkhorn_stabilized', verbose=True, log=True)
    # check constratints
    assert np.allclose(u, G.sum(1), atol=1e-05)  # cf convergence sinkhorn
    assert np.allclose(u, G.sum(0), atol=1e-05)  # cf convergence sinkhorn

    G, log = ot.sinkhorn(
        [], [], M, 1, stopThr=1e-10, method='sinkhorn_epsilon_scaling',
        verbose=True, log=True)
    # check constratints
    assert np.allclose(u, G.sum(1), atol=1e-05)  # cf convergence sinkhorn
    assert np.allclose(u, G.sum(0), atol=1e-05)  # cf convergence sinkhorn


def test_sinkhorn_variants():
    # test sinkhorn
    n = 100
    np.random.seed(0)

    x = np.random.randn(n, 2)
    u = ot.utils.unif(n)

    M = ot.dist(x, x)

    G0 = ot.sinkhorn(u, u, M, 1, method='sinkhorn', stopThr=1e-10)
    Gs = ot.sinkhorn(u, u, M, 1, method='sinkhorn_stabilized', stopThr=1e-10)
    Ges = ot.sinkhorn(
        u, u, M, 1, method='sinkhorn_epsilon_scaling', stopThr=1e-10)
    Gerr = ot.sinkhorn(u, u, M, 1, method='do_not_exists', stopThr=1e-10)

    # check values
    assert np.allclose(G0, Gs, atol=1e-05)
    assert np.allclose(G0, Ges, atol=1e-05)
    assert np.allclose(G0, Gerr)


def test_bary():

    n = 100  # nb bins

    # Gaussian distributions
    a1 = ot.datasets.get_1D_gauss(n, m=30, s=10)  # m= mean, s= std
    a2 = ot.datasets.get_1D_gauss(n, m=40, s=10)

    # creating matrix A containing all distributions
    A = np.vstack((a1, a2)).T

    # loss matrix + normalization
    M = ot.utils.dist0(n)
    M /= M.max()

    alpha = 0.5  # 0<=alpha<=1
    weights = np.array([1 - alpha, alpha])

    # wasserstein
    reg = 1e-3
    bary_wass = ot.bregman.barycenter(A, M, reg, weights)

    assert np.allclose(1, np.sum(bary_wass))
