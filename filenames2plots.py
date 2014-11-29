#!/usr/bin/env python3

plots_skeleton = '''$(function () {
    $('#container').highcharts({
        title: {
            text: null,
            x: -20
        },
        xAxis: {
            categories: [%s],
            title: {
                text: 'Paramètre %s'
            }
        },
        yAxis: {
            title: {
                text: "%s"
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: ''
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [%s]
    });
});'''

plots_skeleton = ' '.join(s.strip() for s in plots_skeleton.split('\n'))

if __name__ == '__main__':
    import sys
    import re

    filename_reg = re.compile(r'^(time|count)-(.+)-(\d+)-(\d+)-(\d+)$')

    data = {'time': {}, 'count': {}}
    for line in sys.stdin.readlines():
        line = line.strip()
        match = filename_reg.match(line)
        if match:
            type_ = match.group(1)
            name = match.group(2)
            k = int(match.group(3))
            m = int(match.group(4))
            n = int(match.group(5))

            if type_ == 'count' and k <= 3:
                continue

            try:
                ls = list(map(float, open(match.group(0)).readlines()))
            except ValueError:
                print('File %s is malformated' % match.group(0), file=sys.stderr)
                continue
            if not ls:
                continue

            avg = sum(ls) / len(ls)

            data[type_].setdefault(name, {})
            data[type_][name][k, m, n] = avg

    for type_, element in data.items():
        for name, table in element.items():
            kCategories = set()
            mCategories = set()
            for (k, m, n), avg in table.items():
                kCategories.add(k)
                mCategories.add(m)

            kCategories = sorted(kCategories)
            mCategories = sorted(mCategories)

            kSerie = dict()
            mSerie = dict()
            for (k, m, n), avg in list(table.items()):
                if len(kSerie) < 5 and m >= mCategories[-5]:
                    kSerie[m] = [avg for (_, m2, _), avg in table.items() if m2 == m]
                if len(mSerie) < 5 and k >= kCategories[-5]:
                    mSerie[k] = [avg for (k2, _, _), avg in table.items() if k2 == k]

            strKCategories = ', '.join(map(str, kCategories))
            strMCategories = ', '.join(map(str, mCategories))
            strKSerie = ', '.join('{name: "m=%sK", data: [%s]}' % (int(m / 1000.0), ', '.join(map(str, ks))) for m, ks in kSerie.items())
            strMSerie = ', '.join('{name: "k=%s", data: [%s]}' % (k, ', '.join(map(str, ms))) for k, ms in mSerie.items())
            strType = 'Temps d\'exécution (s)' if type_ == 'time' else 'count3'
            print(type_, name, 'k')
            print(plots_skeleton % (strKCategories, 'k', strType, strKSerie))
            print(type_, name, 'm')
            print(plots_skeleton % (strMCategories, 'm', strType, strMSerie))
            print()
