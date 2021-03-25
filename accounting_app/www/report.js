frappe.require('/assets/css/charts.css');

frappe.require('/assets/js/charts.js').then(() => {
    window.chart = new frappe.Chart("#my-chart", {
        'data': {
            'title': 'My Awesome Data Analytics',
            'labels': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            'datasets': [
                {
                    'name': 'One',
                    'values': [10.0, 2, 3, 4],
                },
                {
                    'name': 'Two',
                    'values': [43.5, 6, 31, 14],
                }
            ]
        },
        'type': 'bar',
        'barOptions': {
            'stacked': true
        }
    });

    console.log(chart);
});
