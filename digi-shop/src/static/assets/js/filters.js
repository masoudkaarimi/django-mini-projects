import noUiSlider from 'nouislider';
import 'nouislider/dist/nouislider.css';

document.addEventListener('DOMContentLoaded', () => {
    const sliderElement = document.querySelector('.price-range-slider');
    if (sliderElement) {
        const minPrice = parseInt(sliderElement.dataset.minPrice);
        const maxPrice = parseInt(sliderElement.dataset.maxPrice);
        const startMin = parseInt(document.getElementById('price_min_input').value || minPrice);
        const startMax = parseInt(document.getElementById('price_max_input').value || maxPrice);

        noUiSlider.create(sliderElement, {
            start: [startMin, startMax],
            tooltips: [
                {
                    to: (value) => '$' + Math.round(value).toString(),
                    from: (value) => Number(value.replace('$', ''))
                },
                {
                    to: (value) => '$' + Math.round(value).toString(),
                    from: (value) => Number(value.replace('$', ''))
                }
            ],
            range: {
                'min': minPrice,
                'max': maxPrice
            },
            connect: true,
            step: 1
        });
        sliderElement.noUiSlider.on('update', function (values, handle) {
            document.getElementById('price_min_input').value = Math.round(values[0]);
            document.getElementById('price_max_input').value = Math.round(values[1]);
        });
    }
})

window.resetFilters = (formSelector = '#filter-form') => {
    const form = document.querySelector(formSelector);
    if (!form) return;

    form.reset();
    window.location.href = window.location.pathname;
}