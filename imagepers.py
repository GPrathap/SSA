#!/usr/bin/python2

"""A simple implementation of persistent homology on 2D images."""

__author__ = "Stefan Huber <shuber@sthu.org>"


import union_find


def get(im, p):
    return im[p[0]][p[1]]


def iter_neighbors(p, w, h):
    y, x = p
    neigh = []
    # 8-neighborship
    filter = [-1, 0, 1]
    for i in filter:
        for j in filter:
            neigh.append((y+j, x+i))

    #neigh = [(y+j, x+i) for i in  for j in [-1, 0, 1]]
    # 4-neighborship
    # neigh = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
    result = []
    for j, i in neigh:
        if j < 0 or j >= h:
            continue
        if i < 0 or i >= w:
            continue
        if j == y and i == x:
            continue
        result.append((j, i))

    return result


def persistence(im):
    h, w = im.shape

    # Get indices orderd by value from high to low
    indices = [(i, j) for i in range(h) for j in range(w)]
    indices.sort(key=lambda p: get(im, p), reverse=True)
   # print indices
    # Maintains the growing sets
    uf = union_find.UnionFind()

    groups0 = {}

    def get_comp_birth(p):
        return get(im, uf[p])

    # Process pixels from high to low
    for i, p in enumerate(indices):
        v = get(im, p)
        ni = []
        ff = iter_neighbors(p, w, h)

        print "------"
        for q in ff:
            if q in uf:
                print q
                ni.append(uf[q])
        print "------"
        nc = sorted([(get_comp_birth(q), q) for q in set(ni)], reverse=True)

        if i == 0:
            groups0[p] = (v, v, None)

        uf.add(p, -i)

        if len(nc) > 0:
            oldp = nc[0][1]
            uf.union(oldp, p)

            # Merge all others with oldp
            for bl, q in nc[1:]:
                if uf[q] not in groups0:
                    #print(i, ": Merge", uf[q], "with", oldp, "via", p)
                    groups0[uf[q]] = (bl, bl-v, p)
                uf.union(oldp, q)


    # groups1 = [(k, groups0[k][0], groups0[k][1], groups0[k][2]) for k in groups0]
    # groups1.sort(key=lambda g: g[2], reverse=True)
    groups1 = []
    for k in groups0:
        groups1.append((k, groups0[k][0], groups0[k][1], groups0[k][2]))
    groups1.sort(key=lambda g: g[2], reverse=True)

    print groups1
    return groups1
