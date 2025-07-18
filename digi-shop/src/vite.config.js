// https://github.com/Niicck/django-vite-examples/blob/main/examples/new_settings/vite.config.js
import {resolve, join} from 'path';
import {defineConfig, loadEnv} from 'vite'
import {djangoVitePlugin} from 'django-vite-plugin'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(config => {
    const env = loadEnv(config.mode, process.cwd(), '');

    const INPUT_DIR = './static/assets';
    const OUTPUT_DIR = './static/assets/build';

    return {
        resolve: {
            alias: {
                '@': resolve(INPUT_DIR),
            },
        },
        build: {
            outDir: OUTPUT_DIR,
            emptyOutDir: true,
            rollupOptions: {
                input: [
                    join(INPUT_DIR, 'js/script.js'),
                    join(INPUT_DIR, 'css/style.css'),
                    join(INPUT_DIR, 'js/cart.js'),
                    join(INPUT_DIR, 'js/filters.js'),
                ],
            },
        },
        server: {
            host: '127.0.0.1',
            port: 5173,
        },
        plugins: [
            djangoVitePlugin({
                root: '.',
                input: [
                    join(INPUT_DIR, '/js/script.js'),
                    join(INPUT_DIR, '/css/style.css'),
                    join(INPUT_DIR, '/js/cart.js'),
                    join(INPUT_DIR, '/js/filters.js'),
                ],
            }),
            tailwindcss(),
        ],
    }
});
