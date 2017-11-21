import os
from lxml import etree

# find the MTGO path.
def find_mtgo():
    mtgo_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Apps','2.0','Data')
    for _ in range(0, 2):
        mtgo_dir = os.path.join(mtgo_dir, os.listdir(mtgo_dir)[0])
    versions = [os.path.join(mtgo_dir, folder) for folder in os.listdir(mtgo_dir) if ('mtgo..tion' in folder)]
    if len(versions) > 1:
        latest_version = max(versions, key=os.path.getmtime)
        mtgo_dir = latest_version
    elif versions:
        mtgo_dir = versions[0]
    else:
        print("Could not find MTGO data directory.")
        print("Please run MTGO at least once before using this tool.")
        exit()
    return os.path.join(mtgo_dir, 'Data','CardDataSource')

def defoil(filename):
    i = 0
    doc = etree.parse(filename)
    if not os.path.exists(filename + '.bak'):
        doc.write(filename + '.bak')
    DOs = doc.findall('DigitalObject')
    for do in DOs:
        for c in do.getchildren():
            if c.tag == 'IS_FOIL':
                i += 1
                do.remove(c)
    doc.write(filename)
    print("Removed {n} foils from {f}".format(n=i, f=filename))

def main():
    mtgo_dir = find_mtgo()

    for fn in os.listdir(mtgo_dir):
        if not fn.startswith('client_'): 
            continue
        if fn.endswith('.bak'):
            continue
        defoil(os.path.join(mtgo_dir, fn))

if __name__ == "__main__":
    main()
