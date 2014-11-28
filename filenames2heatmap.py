#!/usr/bin/env python3

heatmap_skeleton = '''$(function () {
    $('#container').highcharts({
        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 40
        },
        title: {
            text: null
        },
        xAxis: {
            categories: [%s],
            title: 'k'
        },
        yAxis: {
            categories: [%s],
            title: 'm'
        },
        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[1]
        },
        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 320
        },
        series: [{
            name: null,
            borderWidth: 1,
            data: [%s],
            dataLabels: {
                enabled: false,
                color: 'black',
                style: {
                    textShadow: 'none',
                    HcTextStroke: null
                }
            }
        }]
    });
});'''
heatmap_skeleton = ' '.join(s.strip() for s in heatmap_skeleton.split('\n'))

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

            # if k == 2:
            #     continue

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

            serie = list()
            for (k, m, n), avg in table.items():
                serie.append((kCategories.index(k), mCategories.index(m), avg))

            strKCategories = ', '.join(map(str, kCategories))
            strMCategories = ', '.join(map(str, mCategories))
            strSerie = ', '.join('[%s, %s, %s]' % e for e in serie)
            print(type_, name)
            print(heatmap_skeleton % (strKCategories, strMCategories, strSerie))
