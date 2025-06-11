from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def home_view(request):
    context = {
        "banners": [
            {
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/collections/new-arrivals",
                "alt_text": "New Arrivals"
            },
            {
                "image_url": "/static/assets/images/placeholder.svg",
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
                "price": "59.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "19.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "29.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "89.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/home/index.html', context)


def product_archive_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Products'), 'url': None},
        ],
        "heading": {
            "title": _("All Products"),
            "subtitle": _("Discover our collection of high-quality products"),
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
                "price": "59.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "19.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "29.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "89.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/product/archive.html', context)


def product_single_view(request, product_slug):
    product = {
        "name": "Samsung Galaxy S24 Ultra Smartphone",
        "price": "1299.99",
        "image": "/static/assets/images/placeholder.svg",
        "description": "The Samsung Galaxy S24 Ultra represents the pinnacle of smartphone technology, featuring cutting-edge AI capabilities, professional-grade camera system, and the powerful S Pen for ultimate productivity.",
        "slug": product_slug,
        "sku": "SAM-GAL-S24-ULT-256",
        "stock_count": 25,
        "brand": {
            "name": "Samsung",
            "logo": "samsung"
        },
        "original_price": "1499.99",
        "discount_amount": "200.00",
        "special_offer": True,
        "specifications": [
            {"name": "Display Size", "value": "6.8 inches"},
            {"name": "Resolution", "value": "3088 x 1440 pixels"},
            {"name": "Processor", "value": "Snapdragon 8 Gen 3"},
            {"name": "RAM", "value": "12GB"},
            {"name": "Storage", "value": "256GB"},
            {"name": "Main Camera", "value": "200MP + 12MP + 10MP + 10MP"},
            {"name": "Selfie Camera", "value": "12MP"},
            {"name": "Battery", "value": "5000mAh"},
            {"name": "Operating System", "value": "Android 14"},
            {"name": "Connectivity", "value": "5G, Wi-Fi 6E, Bluetooth 5.3"},
            {"name": "Special Features", "value": "S Pen included, IP68 water resistance"},
            {"name": "Dimensions", "value": "6.43 x 3.11 x 0.35 inches"},
            {"name": "Weight", "value": "8.22 ounces"},
            {"name": "Color Options", "value": "Titanium Black, Titanium Gray, Titanium Violet, Titanium Yellow"},
            {"name": "Warranty", "value": "1-year manufacturer warranty"},
            {"name": "Included Accessories", "value": "S Pen, USB-C cable, ejection pin"},
        ],
        "images": [
            {
                "url": "/static/assets/images/placeholder.svg",
                "alt_text": "Samsung Galaxy S24 Ultra Smartphone - Front View"
            },
            {
                "url": "/static/assets/images/placeholder.svg",
                "alt_text": "Samsung Galaxy S24 Ultra Smartphone - Back View"
            },
            {
                "url": "/static/assets/images/placeholder.svg",
                "alt_text": "Samsung Galaxy S24 Ultra Smartphone - Side View"
            }
        ]
    }

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Products'), 'url': reverse('shop:product_archive')},
            {'title': product["name"], 'url': None},
        ],
        "similar_products": [
            {
                "name": "iPhone 15 Pro Max",
                "price": "1199.99",
                "original_price": "1299.99",
                "discount_amount": "100.00",
                "brand": {
                    "name": "Apple"
                }
            },
            {
                "name": "Google Pixel 8 Pro",
                "price": "899.99",
                "brand": {
                    "name": "Google"
                }
            },
            {
                "name": "Samsung Galaxy S24+",
                "price": "999.99",
                "original_price": "1099.99",
                "discount_amount": "100.00",
                "brand": {
                    "name": "Samsung"
                }
            },
            {
                "name": "OnePlus 11 Pro",
                "price": "799.99",
                "brand": {
                    "name": "OnePlus"
                }
            },
            {
                "name": "Xiaomi 13 Pro",
                "price": "899.99",
                "brand": {
                    "name": "Xiaomi"
                }
            },
            {
                "name": "Sony Xperia 1 V",
                "price": "1099.99",
                "brand": {
                    "name": "Sony"
                }
            }
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
                'link': '#'
            },
        ],
    }

    return render(request, 'shop/product/single.html', context)


def category_archive_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Categories'), 'url': None},
        ],
        "heading": {
            "title": _("All Categories"),
            "subtitle": _("Browse through our categories to find what you need."),
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
    }

    return render(request, 'shop/category/archive.html', context)


def category_single_view(request, category_slug):
    category = {
        "name": category_slug.capitalize(),
        "image": "electronics",
        "description": "Latest gadgets and devices",
        "slug": category_slug,
    }

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Categories'), 'url': reverse('shop:category_archive')},
            {'title': category["name"], 'url': None},
        ],
        "heading": {
            "title": category["name"],
            "subtitle": _("Explore our collection of %(category)s products") % {"category": category["name"]},
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
                "price": "59.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "19.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "29.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "89.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/category/single.html', context)


def brand_archive_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Brands'), 'url': None},
        ],
        "heading": {
            "title": _("All Brands"),
            "subtitle": _("Browse through our extensive collection of brands."),
        },
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


def brand_single_view(request, brand_slug):
    brand = {
        "name": brand_slug.capitalize(),
        "logo": "electronics",
        "description": "Latest gadgets and devices",
        "slug": brand_slug,
    }

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Categories'), 'url': reverse('shop:category_archive')},
            {'title': brand["name"], 'url': None},
        ],
        "heading": {
            "title": brand["name"],
            "subtitle": _("Explore products from %(brand)s") % {"brand": brand["name"]},
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
                "price": "59.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/premium-wordpress-theme",
            },
            {
                "name": "Digital Marketing eBook",
                "price": "19.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/digital-marketing-ebook",
            },
            {
                "name": "Photoshop Brushes Pack",
                "price": "29.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/photoshop-brushes",
            },
            {
                "name": "Video Editing Course",
                "price": "89.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/video-editing-course",
            },
        ],
    }

    return render(request, 'shop/brand/single.html', context)


def cart_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Cart'), 'url': None},
        ],
        "heading": {
            "title": _("Shopping Cart"),
            "subtitle": _("Review your items before proceeding to checkout."),
        },
        "cart_items": [
            {
                "name": "Samsung Galaxy S24 Ultra Smartphone",
                "price": "1299.99",
                "quantity": 1,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/samsung-galaxy-s24-ultra-smartphone",
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "price": "1199.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
            {
                "name": "Google Pixel 8 Pro",
                "price": "899.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            }, {
                "name": "Samsung Galaxy S24 Ultra Smartphone",
                "price": "1299.99",
                "quantity": 1,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/samsung-galaxy-s24-ultra-smartphone",
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "price": "1199.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
            {
                "name": "Google Pixel 8 Pro",
                "price": "899.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            }, {
                "name": "Samsung Galaxy S24 Ultra Smartphone",
                "price": "1299.99",
                "quantity": 1,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/samsung-galaxy-s24-ultra-smartphone",
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "price": "1199.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
            {
                "name": "Google Pixel 8 Pro",
                "price": "899.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
        ],
        "total_price": "3699.97"
    }

    return render(request, 'shop/cart/index.html', context)


def checkout_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Checkout'), 'url': None},
        ],
        "heading": {
            "title": _("Checkout"),
            "subtitle": _("Review your order details before completing your purchase."),
        },
        "cart_items": [
            {
                "name": "Samsung Galaxy S24 Ultra Smartphone",
                "price": "1299.99",
                "quantity": 1,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/samsung-galaxy-s24-ultra-smartphone",
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "price": "1199.99",
                "quantity": 2,
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
        ],
        "subtotal": "3699.97",
        "shipping": "0.00",
        "tax": "295.99",
        "total": "3995.96",
        "shipping_address": {
            "name": "John Doe",
            "address": "123 Main Street, Apt 4B",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "United States"
        },
        "payment": {
            "card_name": "John Doe",
            "card_type": "Visa",
            "card_last4": "4242"
        }
    }

    return render(request, 'shop/checkout/index.html', context)


def wishlist_view(request):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Wishlist'), 'url': None},
        ],
        "heading": {
            "title": _("My Wishlist"),
            "subtitle": _("Items you've saved for later"),
        },
        "wishlist_items": [
            {
                "name": "Samsung Galaxy S24 Ultra Smartphone",
                "price": "1299.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/samsung-galaxy-s24-ultra-smartphone",
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "price": "1199.99",
                "image_url": "/static/assets/images/placeholder.svg",
                "link": "/products/apple-iphone-15-pro-max",
            },
        ]
    }

    return render(request, 'shop/wishlist/index.html', context)
