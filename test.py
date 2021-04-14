import importlib_metadata


def get_packages_distributions():
    packages = importlib_metadata.packages_distributions()
    packages = list(x for x in packages)
    packages = list(filter(lambda x: not x[:1].isdigit(), packages))
    packages = list(filter(lambda x: not x.startswith('_'), packages))
    packages = list(filter(lambda x: not any(e in x for e in r'\/'), packages))
    packages = sorted(packages, key=lambda x: x.lower())
    return packages


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def fill_chunks_equally_with_empty_values(cells):
    output = list()
    maxlength = max(list(len(col) for col in cells))
    for col in cells:
        length = len(col)
        if length < maxlength:
            for _ in range(maxlength - length):
                col.append('')
        output.append(col)
    return output


packages = get_packages_distributions()
chunks = 6
cells = chunkify(packages, chunks)
for c in cells:
    print(len(c))

cells = fill_chunks_equally_with_empty_values(cells)
print('-------------')
# print(cells)
for c in cells:
    print(len(c))
