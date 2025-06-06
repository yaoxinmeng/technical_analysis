import adapter from '@sveltejs/adapter-node';
import { preprocessMeltUI, sequence } from '@melt-ui/pp';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: sequence([
		vitePreprocess(),
		preprocessMeltUI()
	]),

	kit: {
		adapter: adapter(),
		alias: {
			$db: './src/db',
			$components: './src/components',
			$lib: './src/lib',
		}
	}
};

export default config;
