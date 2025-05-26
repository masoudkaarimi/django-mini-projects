from django.shortcuts import render


def index(request):
    context = {
        "banners": [
            {
                "image_url": "/static/images/banner1.jpg",
                "link": "/collections/new-arrivals",
                "alt_text": "New Arrivals"
            },
            {
                "image_url": "/static/images/banner2.jpg",
                "link": "/collections/sale",
                "alt_text": "Sale"
            },
        ],
        "categories": [
            {
                "name": "Notebooks",
                "image": "laptop",
                "product_count": 12,
                "link": "#"
            },
            {
                "name": "Smartphones",
                "image": "smartphone",
                "product_count": 22,
                "link": "#"
            },
            {
                "name": "Smartwatches",
                "image": "watch",
                "product_count": 35,
                "link": "#"
            },
            {
                "name": "TV/Audio",
                "image": "tv",
                "product_count": 76,
                "link": "#"
            },
            {
                "name": "Gaming",
                "image": "gamepad",
                "product_count": 41,
                "link": "#"
            },
            {
                "name": "Accessories",
                "image": "headphones",
                "product_count": 75,
                "link": "#"
            },
        ],
        "featured_products": [
            {
                "name": "Premium WordPress Theme",
                "price": "$59.99",
                "image_url": "/static/images/wordpress-theme.jpg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "$19.99",
                "image_url": "/static/images/ebook.jpg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "$29.99",
                "image_url": "/static/images/brushes.jpg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "$89.99",
                "image_url": "/static/images/video-course.jpg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/home/index.html', context)


def product_archive(request):
    context = {
        "categories": [
            {
                "name": "Notebooks",
                "image": "laptop",
                "product_count": 12,
                "link": "#"
            },
            {
                "name": "Smartphones",
                "image": "smartphone",
                "product_count": 22,
                "link": "#"
            },
            {
                "name": "Smartwatches",
                "image": "watch",
                "product_count": 35,
                "link": "#"
            },
            {
                "name": "TV/Audio",
                "image": "tv",
                "product_count": 76,
                "link": "#"
            },
            {
                "name": "Gaming",
                "image": "gamepad",
                "product_count": 41,
                "link": "#"
            },
            {
                "name": "Accessories",
                "image": "headphones",
                "product_count": 75,
                "link": "#"
            },
        ],
        "brands": [
            {
                "name": "Apple",
                "logo": "apple",
                "product_count": 15,
                "link": "#"
            },
            {
                "name": "Samsung",
                "logo": "samsung",
                "product_count": 20,
                "link": "#"
            },
            {
                "name": "Sony",
                "logo": "sony",
                "product_count": 10,
                "link": "#"
            },
            {
                "name": "LG",
                "logo": "lg",
                "product_count": 8,
                "link": "#"
            },
        ],
        "products": [
            {
                "name": "Premium WordPress Theme",
                "price": "$59.99",
                "image_url": "/static/images/wordpress-theme.jpg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "$19.99",
                "image_url": "/static/images/ebook.jpg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "$29.99",
                "image_url": "/static/images/brushes.jpg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "$89.99",
                "image_url": "/static/images/video-course.jpg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/product/archive.html', context)


def category_archive(request):
    context = {
        "categories": [
            {
                "name": "Notebooks",
                "image": "laptop",
                "product_count": 12,
                "link": "#"
            },
            {
                "name": "Smartphones",
                "image": "smartphone",
                "product_count": 22,
                "link": "#"
            },
            {
                "name": "Smartwatches",
                "image": "watch",
                "product_count": 35,
                "link": "#"
            },
            {
                "name": "TV/Audio",
                "image": "tv",
                "product_count": 76,
                "link": "#"
            },
            {
                "name": "Gaming",
                "image": "gamepad",
                "product_count": 41,
                "link": "#"
            },
            {
                "name": "Accessories",
                "image": "headphones",
                "product_count": 75,
                "link": "#"
            },
        ],
    }

    return render(request, 'shop/category/archive.html', context)


def category_single(request, category_slug):
    context = {
        "category": {
            "name": category_slug.capitalize(),
            "image": "electronics",
            "description": "Latest gadgets and devices",
            "slug": category_slug,
        },
        "categories": [
            {
                "name": "Notebooks",
                "image": "laptop",
                "product_count": 12,
                "link": "#"
            },
            {
                "name": "Smartphones",
                "image": "smartphone",
                "product_count": 22,
                "link": "#"
            },
            {
                "name": "Smartwatches",
                "image": "watch",
                "product_count": 35,
                "link": "#"
            },
            {
                "name": "TV/Audio",
                "image": "tv",
                "product_count": 76,
                "link": "#"
            },
            {
                "name": "Gaming",
                "image": "gamepad",
                "product_count": 41,
                "link": "#"
            },
            {
                "name": "Accessories",
                "image": "headphones",
                "product_count": 75,
                "link": "#"
            },
        ],
        "brands": [
            {
                "name": "Apple",
                "logo": "apple",
                "product_count": 15,
                "link": "#"
            },
            {
                "name": "Samsung",
                "logo": "samsung",
                "product_count": 20,
                "link": "#"
            },
            {
                "name": "Sony",
                "logo": "sony",
                "product_count": 10,
                "link": "#"
            },
            {
                "name": "LG",
                "logo": "lg",
                "product_count": 8,
                "link": "#"
            },
        ],
        "products": [
            {
                "name": "Premium WordPress Theme",
                "price": "$59.99",
                "image_url": "/static/images/wordpress-theme.jpg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "$19.99",
                "image_url": "/static/images/ebook.jpg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "$29.99",
                "image_url": "/static/images/brushes.jpg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "$89.99",
                "image_url": "/static/images/video-course.jpg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/category/single.html', context)


def brand_archive(request):
    context = {
        "brands": [
            {
                "name": "Apple",
                "logo": "apple",
                "product_count": 15,
                "link": "#"
            },
            {
                "name": "Samsung",
                "logo": "samsung",
                "product_count": 20,
                "link": "#"
            },
            {
                "name": "Sony",
                "logo": "sony",
                "product_count": 10,
                "link": "#"
            },
            {
                "name": "LG",
                "logo": "lg",
                "product_count": 8,
                "link": "#"
            },
        ],
    }

    return render(request, 'shop/brand/archive.html', context)


def brand_single(request, brand_slug):
    context = {
        "brand": {
            "name": brand_slug.capitalize(),
            "logo": "electronics",
            "description": "Latest gadgets and devices",
            "slug": brand_slug,
        },
        "categories": [
            {
                "name": "Notebooks",
                "image": "laptop",
                "product_count": 12,
                "link": "#"
            },
            {
                "name": "Smartphones",
                "image": "smartphone",
                "product_count": 22,
                "link": "#"
            },
            {
                "name": "Smartwatches",
                "image": "watch",
                "product_count": 35,
                "link": "#"
            },
            {
                "name": "TV/Audio",
                "image": "tv",
                "product_count": 76,
                "link": "#"
            },
            {
                "name": "Gaming",
                "image": "gamepad",
                "product_count": 41,
                "link": "#"
            },
            {
                "name": "Accessories",
                "image": "headphones",
                "product_count": 75,
                "link": "#"
            },
        ],
        "products": [
            {
                "name": "Premium WordPress Theme",
                "price": "$59.99",
                "image_url": "/static/images/wordpress-theme.jpg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "$19.99",
                "image_url": "/static/images/ebook.jpg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "$29.99",
                "image_url": "/static/images/brushes.jpg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "$89.99",
                "image_url": "/static/images/video-course.jpg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/brand/single.html', context)
