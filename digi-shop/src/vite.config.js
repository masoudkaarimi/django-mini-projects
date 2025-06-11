// https://github.com/Niicck/django-vite-examples/blob/main/examples/new_settings/vite.config.js
import {resolve, join} from 'path';
import {defineConfig, loadEnv} from 'vite'
import {djangoVitePlugin} from 'django-vite-plugin'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(config => {
    const env = loadEnv(config.mode, process.cwd(), '');

    const INPUT_DIR = './static/assets';
    const OUTPUT_DIR = './staticfiles/build';

    return {
        resolve: {
            alias: {
                '@': resolve(INPUT_DIR),
            },
        },
        // css: {},
        server: {
            host: '127.0.0.1',
            // host: env.DJANGO_VITE_DEV_SERVER_HOST,
            // port: env.DJANGO_VITE_DEV_SERVER_PORT,
            // cors: {
            //     origin: '127.0.0.1',
            // },
        },
        plugins: [
            djangoVitePlugin({
                input: [
                    join(INPUT_DIR, '/js/script.js'),
                    join(INPUT_DIR, '/css/style.css'),
                ],
                // root: '.',
            }),
            tailwindcss(),
        ],
    }
});
